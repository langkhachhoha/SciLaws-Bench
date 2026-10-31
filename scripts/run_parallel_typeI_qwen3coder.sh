#!/usr/bin/env bash
# SciLaws-Parallel, Type I only (66 single-group tasks): the agent on
# Qwen3 Coder 30B via Amazon Bedrock, a small model with no thinking mode at
# gpt-4o-mini's price. Paper defaults: 30 turns and the experiment caps in
# baseline_agent/task.py; temperature 0.4 and 16384 output tokens, see
# _call_bedrock_openweight in call_llm_api.py. Start it inside tmux:
#
#   tmux new -s qwen                                  # reattach: tmux attach -t qwen
#   bash scripts/run_parallel_typeI_qwen3coder.sh
#
# Rerun the same command to resume after a crash, Ctrl-C, a dropped session or
# a reboot. Tasks with a submission, and tasks whose agent used all its turns
# without one, are kept. Interrupted tasks restart from turn 0 (a Parallel task
# cannot resume mid-trajectory); the interrupted attempt is kept beside the new
# one as *.aborted-<UTC stamp>. Each invocation makes up to MAX_PASSES batch
# passes, so a task that fails on a transient API error is retried on its own.
# Once all 66 tasks are finished it stages the submissions, judges them on
# Bedrock (judge results are kept across reruns) and prints S_S over 66 tasks.
# Judge every run you compare with the same JUDGE_MODEL.
#
# The agent is taught the <experiment> format (guided_agent/experiment_guidance.py)
# and the run dir ends in _guided. EXPERIMENT_GUIDANCE=0 runs the upstream reference
# agent without it, in a dir without that suffix.
#
# Overrides (env): RUN_NAME, WORKERS, MAX_PASSES, RETRY_SLEEP, TASK_TIMEOUT,
#                  SKIP_SCORE=1, JUDGE_MODEL, AWS_PROFILE, AWS_REGION,
#                  EXPERIMENT_GUIDANCE=0.
set -euo pipefail

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$REPO"

MODEL=br-qwen3-coder-30b
TASK_TYPE=typeI
N_TASKS=66
MAX_TURNS=30
EXPERIMENT_GUIDANCE=${EXPERIMENT_GUIDANCE:-1}
if [[ $EXPERIMENT_GUIDANCE == 0 ]]; then
    GUIDANCE_SUFFIX= GUIDANCE_FLAG=--no-experiment-guidance
else
    GUIDANCE_SUFFIX=_guided GUIDANCE_FLAG=--experiment-guidance
fi
RUN_NAME=${RUN_NAME:-parallel_${TASK_TYPE}_${MODEL}${GUIDANCE_SUFFIX}}
RUN_DIR=$REPO/experiments/$RUN_NAME
WORKERS=${WORKERS:-8}
MAX_PASSES=${MAX_PASSES:-3}
RETRY_SLEEP=${RETRY_SLEEP:-120}
TASK_TIMEOUT=${TASK_TIMEOUT:-7200}   # seconds; a killed task counts as interrupted
PY=$REPO/.venv/bin/python

export AWS_PROFILE=${AWS_PROFILE:-reddy-research}
export AWS_REGION=${AWS_REGION:-us-east-1}
export PYTHONUNBUFFERED=1
# Not read for non-reasoning aliases; cleared so the run does not depend on the shell.
unset REASONING_EFFORT OPENAI_REASONING_EFFORT

die() { echo "ERROR: $*" >&2; exit 1; }
stamp() { date -u +%Y%m%d_%H%M%S; }

# --- preflight ---------------------------------------------------------------
[[ -x $PY ]] || die "$PY missing; create the venv first (see CLAUDE.md, Setup)"
n=$(find "tasks/$TASK_TYPE" -mindepth 2 -maxdepth 2 -name metadata.yaml | wc -l)
[[ $n -eq $N_TASKS ]] || die "tasks/$TASK_TYPE has $n tasks, expected $N_TASKS; re-run hf download"
"$PY" -c "import boto3; boto3.client('sts').get_caller_identity()" 2>/dev/null \
    || die "no AWS credentials for profile $AWS_PROFILE"
[[ -n ${TMUX:-} ]] || echo "WARNING: not inside tmux; a dropped SSH session will stop the run (rerun to resume)."

mkdir -p "$RUN_DIR/batch_logs"
exec 9>"$RUN_DIR/.lock"
flock -n 9 || die "another run is using $RUN_DIR (lock $RUN_DIR/.lock)"
trap 'echo; echo "Interrupted. Rerun the same command to resume."; exit 130' INT TERM

# Tasks still to run: no submission and not ended by max_turns_reached. This is
# the rule run_batch.py applies with --skip-existing --skip-finished.
count_unfinished() {
    "$PY" - "$REPO" "$RUN_DIR" "$MODEL" "$TASK_TYPE" <<'EOF'
import json, sys
from pathlib import Path
repo, run, model, ttype = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
left = 0
for meta in (repo / "tasks" / ttype).glob("*/metadata.yaml"):
    task = meta.parent.name
    sub = run / "parallel" / "submissions" / model / ttype / f"{task}.py"
    if sub.exists() and sub.read_text(errors="replace").strip():
        continue
    traj = run / "parallel" / "trajectories" / model / ttype / f"{task}.traj.json"
    try:
        status = json.loads(traj.read_text())["trial"]["status"]
    except Exception:
        status = ""
    left += status != "max_turns_reached"
print(left)
EOF
}

# --- agent runs ----------------------------------------------------------------
echo "RUN_DIR=$RUN_DIR  model=$MODEL  type=$TASK_TYPE  turns=$MAX_TURNS  workers=$WORKERS"
for pass in $(seq 1 "$MAX_PASSES"); do
    left=$(count_unfinished)
    [[ $left -eq 0 ]] && break
    echo "== pass $pass/$MAX_PASSES: $left of $N_TASKS tasks to run ($(date -u '+%F %T') UTC)"
    "$PY" baseline_agent/run_batch.py \
        --models "$MODEL" --modes parallel --task-types "$TASK_TYPE" \
        --max-turns "$MAX_TURNS" --workers "$WORKERS" \
        --task-timeout-seconds "$TASK_TIMEOUT" \
        --run-dir "$RUN_DIR" --run-id "$RUN_NAME" \
        --skip-existing --skip-finished --merge-existing-summary \
        "$GUIDANCE_FLAG" \
        2>&1 | tee "$RUN_DIR/batch_logs/batch_$(stamp).log" || true
    left=$(count_unfinished)
    if [[ $left -gt 0 && $pass -lt $MAX_PASSES ]]; then
        echo "== $left tasks interrupted or failed; retrying in ${RETRY_SLEEP}s"
        sleep "$RETRY_SLEEP"
    fi
done

left=$(count_unfinished)
if [[ $left -gt 0 ]]; then
    echo "== $left tasks still unfinished after $MAX_PASSES passes; see the logs under"
    echo "   $RUN_DIR/parallel/logs/$MODEL/$TASK_TYPE, then rerun this script."
    exit 1
fi
echo "== all $N_TASKS tasks finished"

# --- scoring -----------------------------------------------------------------------
[[ ${SKIP_SCORE:-0} == 1 ]] && { echo "SKIP_SCORE=1: not scoring"; exit 0; }
SUBS=$RUN_DIR/parallel/submissions/$MODEL
STAGE=$RUN_DIR/parallel_stage
OUT=$RUN_DIR/parallel_out
# Staging wipes $OUT, so stage only once; delete $STAGE to restage.
if [[ ! -f $STAGE/manifest.json ]]; then
    "$PY" harness/evaluate_parallel.py --tasks-dir tasks --submissions "$SUBS" \
        --stage-dir "$STAGE" --output-dir "$OUT" --method-name "$MODEL" --overwrite
fi
"$PY" scripts/judge_parallel_bedrock.py --manifest "$STAGE/manifest.json" \
    ${JUDGE_MODEL:+--model "$JUDGE_MODEL"}

# The official summary averages over staged submissions only; S_S counts every
# task, with no submission, a contract failure or no judge result scoring 0.
"$PY" - "$RUN_DIR" "$MODEL" "$TASK_TYPE" "$N_TASKS" <<'EOF'
import csv, json, sys
from pathlib import Path
run, model, ttype, n = Path(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4])
rows = list(csv.DictReader((run / "parallel_out" / "parallel_summary.csv").open()))
scores = [float(r["structure_score"]) if r["structure_score"] not in ("", "None") else 0.0 for r in rows]
tokens = {"prompt_tokens": 0, "completion_tokens": 0}
looping = 0
for traj in (run / "parallel" / "trajectories" / model / ttype).glob("*.traj.json"):
    trial = json.loads(traj.read_text())["trial"]
    usage = trial.get("usage_total") or {}
    for k in tokens:
        tokens[k] += int(usage.get(k) or 0)
    replies = [m["content"] for m in trial["chat_history"] if m["role"] == "assistant"]
    looping += sum(bool(a) and a == b for a, b in zip(replies, replies[1:])) >= 3
# qwen.qwen3-coder-30b-a3b-v1:0 on-demand, us-east-1, AWS Price List 2026-10-30: $0.15 / $0.60 per 1M tokens
cost = tokens["prompt_tokens"] * 0.15e-6 + tokens["completion_tokens"] * 0.60e-6
judges = sorted({json.loads(p.read_text()).get("judge_model", "")
                 for p in (run / "parallel_out").glob("*.json") if p.name != "parallel_summary.json"})
result = {"model": model, "type": ttype, "n_tasks": n, "submitted": len(rows),
          "S_S_strict": sum(scores) / n, "mean_over_submitted": sum(scores) / len(scores) if scores else None,
          "tasks_with_3plus_repeated_replies": looping,
          "agent_tokens": tokens, "agent_cost_usd_est": round(cost, 2), "judge_models": judges,
          "judge": "Bedrock stand-in (scripts/judge_parallel_bedrock.py), not the paper's GPT-5.4-mini"}
(run / f"score_{ttype}.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
EOF
