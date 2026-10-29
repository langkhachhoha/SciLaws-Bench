# CLAUDE.md

Fork of SciLaws-Bench used to build and evaluate a new **agent harness for
active-experiment law discovery**, scored on **SciLaws-Parallel** only. The
upstream reference agent (`baseline_agent/`) is the baseline to beat. A
Vietnamese walkthrough of the run pipeline and the first smoke-test result is in
`notes/phan_tich_cau_truc_va_ket_qua.md`.

## Setup

```bash
/home/hieuhm19/miniconda3/envs/dev/bin/python3.11 -m venv .venv   # system python3.10 has no ensurepip
.venv/bin/pip install -r requirements-agent.txt                       # includes anthropic[bedrock]
.venv/bin/hf download RealSR/SciLaws-Bench --repo-type dataset --local-dir . --include 'tasks/*'
ls tasks/typeI | wc -l; ls tasks/typeII | wc -l                        # must be 66 and 52
export AWS_PROFILE=reddy-research AWS_REGION=us-east-1                 # Bedrock credentials
```

`hf download` has exited 0 after fetching only part of `tasks/`; re-run it until
the counts match (it skips files already present).

## Commands

```bash
# One Parallel task, reference agent, paper defaults (30 turns, effort=medium)
.venv/bin/python baseline_agent/run_baseline.py tasks/typeI/<task> br-claude-sonnet-4-6 --simulator --out <dir>

# Many tasks (writes summary.tsv/json, per-task logs, trajectories, submissions)
.venv/bin/python baseline_agent/run_batch.py --models br-claude-sonnet-4-6 --modes parallel \
    --task-types typeI typeII --workers 4 --run-dir experiments/<run_name>

# Score S_S: stage with the official scorer, then judge on Bedrock (no Codex here)
.venv/bin/python harness/evaluate_parallel.py --tasks-dir tasks \
    --submissions experiments/<run>/parallel/submissions/<model> \
    --stage-dir experiments/<run>/parallel_stage --output-dir experiments/<run>/parallel_out \
    --method-name <model> --overwrite
.venv/bin/python scripts/judge_parallel_bedrock.py --manifest experiments/<run>/parallel_stage/manifest.json
```

The official `--dispatch codex` path needs the `codex` CLI and an OpenAI key;
neither exists on this machine. `scripts/judge_parallel_bedrock.py` reuses the
verbatim judge prompt and the official aggregation, but the judge model differs
from the paper's (GPT-5.4-mini), so report it as such.

## Models on Bedrock

Use the `br-*` aliases in `baseline_agent/call_llm_api.py`. They turn on adaptive
thinking at `effort=medium` (paper Appendix B.1; override with
`REASONING_EFFORT`) and always send stop sequences at the tool close tags. Without
the stop sequences, Claude with interleaved thinking writes dozens of imagined
`<experiment>`/`<python>` blocks per turn (42k output tokens on turn 1, kept in
history); see `experiments/aborted_nostop_br-claude-sonnet-4-6/`. The upstream
`an` provider sends no `thinking` field, so Claude runs without reasoning there —
do not use it for paper-comparable runs.

Access on account `reddy-research` (probed 2026-10-29): callable — Claude Opus
4.6, Sonnet 4.6, Sonnet 4.5, Haiku 4.5, DeepSeek R1 / V3.2, GLM-5. Denied —
Claude Opus 4.7 / 4.8, Opus 5 / 5.5, Sonnet 5 / 5.5, GPT-5.4 / 5.5, GLM-5.3. None
of the paper's nine models is callable, so no run here is a like-for-like
reproduction of a paper row. The Mantle endpoint (`AnthropicBedrockMantle`)
serves none of these models to this account (403 for Opus 4.8, 404 for Sonnet
4.6), so the `br` provider uses `AnthropicBedrock` with `us.` inference profiles.

- `anthropic>=2` sends API version `2026-10-21`; Bedrock rejects it for models
  older than Claude 4.7 (`400 Invalid API version`). The `br` provider and the
  judge script send `anthropic_version: bedrock-2023-05-31` for those models
  instead. Pinning `anthropic<2` is the alternative; PyPI was unreachable here.
- Daily token quotas are small and not listed by `service-quotas`: Sonnet 4.6
  returned `429 Too many tokens per day` after ~580k tokens in one day (≈450k
  input + 130k output across two 20-turn runs and a few tests).
  One Parallel task costs ~250k input tokens; budget full-benchmark runs per
  model per day accordingly, and note `global.*` profiles throttle separately.

## Layout and boundaries

- `harness/` — the frozen interface shared by every solver: prompts
  (`prompts.py`), tool protocol + `<python>` sandbox (`agent_protocol.py`),
  simulator runtime (`sim_runtime.py`), scorers. Changing anything here makes
  results incomparable with the paper; build a new harness beside it instead.
- `baseline_agent/` — the reference ReAct loop (`agent.py`), task loaders
  (`task.py`), LLM client (`call_llm_api.py`), batch / resume / salvage runners.
- `scripts/judge_parallel_bedrock.py` — Bedrock stand-in for the Codex judge.
- `experiments/` — tracked run outputs. `batch_runs/`, `results/`,
  `submissions/`, `parallel_stage/`, `parallel_out/` at the repo root are
  gitignored.
- `tasks/` — downloaded data, gitignored.

## Parallel-mode facts that are easy to get wrong

- The experiment budget is enforced in `baseline_agent/task.py`
  (`SimulatorTask.run_experiment`, constants at the top: ≤10 calls,
  ≤max(10, ⌊0.1·n_train⌋) points per call, ≤3 samples per point), not in
  `harness/`. A new harness must reuse `SimulatorTask` or replicate these caps
  exactly to stay comparable.
- The simulator varies only `state["used_inputs"]`, often a subset of
  `metadata.yaml: inputs`; the agent prompt and `predict` columns follow that
  subset.
- `tasks/*/eval/` and `tasks/*/simulator/` are answer keys
  (`simulator/formula.py` and `state.joblib["formula_source"]` hold the hidden
  law). Never put them in an agent's context; reach the simulator only through
  `SimulatorTask.run_experiment`.
- Simulator output is `F(X) + noise_scale · kNN-resampled real residual`, with
  inputs silently clipped to the support box (`n_clipped` reports it).
- A submission must call `<experiment>` at least once; turn 30 is a forced
  `<final_formula>` turn with one retry. Strict aggregation: no submission,
  contract failure or missing judge result scores 0.
- `step()` runs the first-appearing tag *type* but extracts the *last* block of
  that type (`_last_block` uses `rfind`), so multi-block replies execute their
  last `<experiment>`, not their first.
- `<python>` calls are stateless and import-whitelisted (numpy, scipy, pandas,
  sklearn, math, …); `open`, `os`, `getattr`, file reads are rejected.
- An LLM API exception is not caught by `agent.py`: the task process exits, the
  trajectory checkpoint stays `running*`. `resume_baseline.py` reloads the task
  with `simulator=None` (Real mode), so it cannot resume a Parallel run — rerun
  it, or salvage with `force_final_from_traj.py`. The `br` provider retries a
  stream dropped mid-response once; the SDK's own retry does not cover that.
- Per-task paper scores for every model: `baseline_agent/model_task_scores.json`.
- Summaries and trajectories record absolute paths of this machine.
