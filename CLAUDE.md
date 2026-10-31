# CLAUDE.md

Fork of SciLaws-Bench used to build and evaluate a new **agent harness for
active-experiment law discovery**, scored on **SciLaws-Parallel** only. The
upstream reference agent (`baseline_agent/` with `--no-experiment-guidance`) is
the baseline to beat. A Vietnamese walkthrough of the run pipeline and the first smoke-test result is in
`notes/phan_tich_cau_truc_va_ket_qua.md`. Current results, findings and next
steps: `notes/trang_thai_va_buoc_tiep_theo.md` — read it first when resuming.

**Scope since 2026-10-30: Type I (single-group) tasks only — the 66 tasks in
`tasks/typeI/`.** Run, score and compare on that split (`--task-types typeI`),
dividing by 66. The paper's per-split numbers are in
`baseline_agent/all_results.md` ("Parallel typeI" column; GLM-5.2 0.5644,
Claude Opus 4.8 0.5303). Type II stays downloaded but is not run.

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
# Main runs: all 66 Type I tasks, <experiment> format taught (guided_agent/, the
# default), 30 turns, then judge and S_S over 66. Meant for tmux; rerun the same
# command to resume. Each writes experiments/parallel_typeI_<model>_guided/.
bash scripts/run_parallel_typeI_minimax.sh       # MiniMax M2.5, the cheap reasoning model
bash scripts/run_parallel_typeI_glm5.sh          # GLM-5
bash scripts/run_parallel_typeI_qwen3coder.sh    # Qwen3 Coder 30B, the small non-reasoning model
# The reference agent without guidance, in a dir without _guided (GLM-5's is
# experiments/parallel_typeI_br-glm-5/):
EXPERIMENT_GUIDANCE=0 bash scripts/run_parallel_typeI_minimax.sh
# Their screen stays silent until a task finishes (~10-15 min); per-turn progress:
watch -n 20 .venv/bin/python scripts/run_status.py [<run_dir>]

# Read runs turn by turn in the browser: input, reasoning, each call and its output,
# the submission and the judge's verdict. Every run under experiments/ loads on its
# own; paste any other run's path into the page. Refresh to pick up new results.
.venv/bin/python viewer/serve.py                 # http://127.0.0.1:8765

# One Parallel task, 30 turns; add --no-experiment-guidance for the reference agent
.venv/bin/python baseline_agent/run_baseline.py tasks/typeI/<task> br-glm-5 --simulator --out <dir>

# Many tasks (writes summary.tsv/json, per-task logs, trajectories, submissions).
# --skip-existing --skip-finished --merge-existing-summary resumes a run dir.
.venv/bin/python baseline_agent/run_batch.py --models br-glm-5 --modes parallel \
    --task-types typeI --workers 8 --run-dir experiments/<run_name>

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
from the paper's (GPT-5.4-mini; here Opus 4.6 by default), so report it as such.

The official `strict_mean` in `parallel_summary.json` averages over *staged
submissions*, not over all tasks: tasks without a submission are absent from the
manifest. S_S as the paper reports it divides by 66; the run script writes it to
`experiments/<run>/score_typeI.json`. Restaging with `--overwrite` deletes the
output dir, judge results included.

## Models on Bedrock

Use the `br-*` aliases in `baseline_agent/call_llm_api.py`. The Claude ones turn
on adaptive thinking at `effort=medium` (paper Appendix B.1; override with
`REASONING_EFFORT`) and always send stop sequences at the tool close tags. Without
the stop sequences, Claude with interleaved thinking writes dozens of imagined
`<experiment>`/`<python>` blocks per turn (42k output tokens on turn 1, kept in
history); that run is `experiments/aborted_nostop_br-claude-sonnet-4-6/` at
commit `240e29b`. The upstream
`an` provider sends no `thinking` field, so Claude runs without reasoning there —
do not use it for paper-comparable runs.

**GLM-5** (`br-glm-5`, provider `bo`, model `zai.glm-5`) is the working model:
≈$0.7 per Parallel task against ≈$4.2 for Opus 4.6, and a 100M tokens/minute
on-demand quota. It goes through `InvokeModel` with an OpenAI chat-completions
body, because what works for Claude does not work here (probed 2026-10-30):
- Thinking turns on only with `reasoning_effort: "high"`; `low`/`medium` (and
  `thinking`/`enable_thinking` fields) produce no reasoning at all. GLM thinking
  is on/off, so "high" is the thinking-on setting, not a higher tier than the
  paper's. Do not export `REASONING_EFFORT=medium` for it.
- The reasoning comes back inside `content` as `<reasoning>…</reasoning>`,
  sometimes followed by a stray tail ending in `</think>`; the provider moves
  both to `reasoning_content`, which `agent.py` never feeds back.
- Converse rejects `stopSequences` for this model, and InvokeModel's `stop`
  can fire inside the inline reasoning. The provider sends no stop and cuts the
  visible text after the first tool close tag instead (logged when it drops
  anything), which leaves one block per turn as the `br` stop does. The paper's
  OpenAI-compatible providers sent no stop at all (`_USE_STOP = False`).

**Qwen3 Coder 30B** (`br-qwen3-coder-30b`, same `bo` provider,
`qwen.qwen3-coder-30b-a3b-v1:0`) is the small non-reasoning model: it has no
thinking mode (no switch produces reasoning), costs what gpt-4o-mini does
($0.15 / $0.60 per 1M tokens), and its Bedrock context takes a 240k-token prompt.
It is left out of `_REASONING_MODELS`, so it runs at temperature 0.4 with 16384
output tokens, gpt-4o-mini's own ceiling (the `oa` branch that ran it sets no
cap; 8192 cut long `<python>` bodies on another model).

**MiniMax M2.5** (`br-minimax-m2-5`, same `bo` provider, `minimax.minimax-m2.5`) is
the cheap reasoning model: $0.30 / $1.20 per 1M tokens, a 196k context and a 100M
tokens/minute quota. It reasons at every `reasoning_effort`, none included, at
about the same length, so the "medium" the provider sends changes nothing. The
reasoning comes back inline as on GLM-5. Prefer `medium`; use `high` only when a
model has no other way to reason.

`reasoning_effort` on the cheap Bedrock models (probed 2026-10-31):
- Reason only at `high`: DeepSeek V3.2, Kimi K2.5, GLM-4.7, Nemotron 3 Super/Nano,
  Qwen3 Next. At `medium` they answer without reasoning.
- Reason at every setting: MiniMax M2.5, Kimi K2 Thinking ($0.60 / $2.50),
  gpt-oss-120b. Only gpt-oss-120b clearly reasons longer at `high`.
- Magistral Small writes its reasoning in the visible text, which goes into history.

gpt-oss-120b at `medium` was piloted against MiniMax M2.5 and dropped (2026-10-31,
6 tasks picked for a large GLM-5/Qwen3 Coder gap, guidance on). It had the empty
replies of gpt-oss-20b, 4 of 78 turns, and stopped early with 2.2 experiments and a
median of 11.5 turns. MiniMax M2.5 had no empty reply, 5.2 experiments and a median
of 19 turns. Scored on the same tasks with the same judge: MiniMax M2.5 0.583,
gpt-oss-120b 0.375, against GLM-5 0.750 and guided Qwen3 Coder 0.292; the task pick
favours GLM-5, so this ranks the two cheap models and does not estimate S_S.

GLM-4.7 Flash with thinking off was tried and dropped (2026-10-30): 46 of 66
Type I tasks repeated a byte-identical reply 3+ times (mean 16.9 per task; 2.1
experiments against GLM-5's 6.6), usually re-sending a call the tool had
rejected. It does the same through Converse, and GLM-5 never does through the
same provider, so this is the model, not the provider.

Small-model pilot (3 tasks, 2026-10-30): Nova Lite loops like Flash, Llama 4
Maverick submits after ~6 turns, and Qwen3 32B has a 32k context and crashed
mid-task. When piloting a model, count repeated replies and `n_experiments`
(`scripts/run_status.py` shows both): turns used alone hides a loop.

gpt-oss-20b on Bedrock was tried and dropped (2026-10-30): after its reasoning it
often returns no visible text (InvokeModel and Converse alike) — 22 of 31 turns
empty and no formula on `cepheid_period_luminosity__M_W`.

Access on account `reddy-research` (probed 2026-10-30 with one call to each of
the 96 Bedrock text models): callable Claude — Opus 4.6 / 4.5 / 4.1, Sonnet 4.6
/ 4.5, Haiku 4.5; callable open-weight — GLM-5 / 4.7, DeepSeek R1 / V3.2, Kimi
K2.5 / K2 Thinking / K3, Qwen3, MiniMax M2.x, gpt-oss, Llama, Mistral Large 3,
Nova, and more. Denied — every Claude 4.7+ (Opus 4.7 / 4.8 / 5 / 5.5, Sonnet 5 /
5.5, Haiku 5.5, Fable), GPT-5.4+ / GPT-6.x, GLM-5.3, Grok. None of the paper's
nine models is callable, so no run here is a like-for-like reproduction of a
paper row. The Mantle endpoint (`AnthropicBedrockMantle`) serves none of the
Claude models to this account (403 for Opus 4.8, 404 for Sonnet 4.6), so the
`br` provider uses `AnthropicBedrock` with `us.` inference profiles.

- `anthropic>=2` sends API version `2026-10-21`; Bedrock rejects it for models
  older than Claude 4.7 (`400 Invalid API version`). The `br` provider and the
  judge script send `anthropic_version: bedrock-2023-05-31` for those models
  instead. Pinning `anthropic<2` is the alternative; PyPI was unreachable here.
- Claude daily token quotas are small and not listed by `service-quotas`: Sonnet
  4.6 returned `429 Too many tokens per day` after ~580k tokens in one day
  (≈450k input + 130k output across two 20-turn runs and a few tests). A
  30-turn Parallel task used 652k input + 23k output tokens on Opus 4.6 (no
  prompt caching: every turn resends the whole history), so a full Claude run
  does not fit in a day's quota. `global.*` profiles throttle separately: on
  2026-10-30 the judge's default `us.` Opus 4.6 returned the daily 429 while
  `--model global.anthropic.claude-opus-4-6-v1` (same model) still worked.
- `us.*` profiles cost 10% more than `global.*` (Cost Explorer: Opus 4.6
  $5.50 / $27.50 vs $5 / $25 per 1M tokens).
- The account is shared and credit-funded: other users' GLM / Kimi / Qwen / EC2
  spend is most of the bill (~$10k in Oct 2026). No API reports the remaining
  credit; ask the account owner before large runs.

## Layout and boundaries

- `harness/` — the frozen interface shared by every solver: prompts
  (`prompts.py`), tool protocol + `<python>` sandbox (`agent_protocol.py`),
  simulator runtime (`sim_runtime.py`), scorers. Changing anything here makes
  results incomparable with the paper; build a new harness beside it instead.
- `baseline_agent/` — the reference ReAct loop (`agent.py`), task loaders
  (`task.py`), LLM client (`call_llm_api.py`), batch / resume / salvage runners.
- `guided_agent/` — wraps one task to teach the `<experiment>` format. This is the
  main agent since 2026-10-31: on by default in Parallel mode, off with
  `--no-experiment-guidance` or `EXPERIMENT_GUIDANCE=0`. Requests are accepted or
  rejected as before, under the same caps, so `harness/` and `SimulatorTask` stay
  unchanged, but the agent reads a different prompt, so a guided run is not a
  reference-agent run. Resuming an unguided run dir needs the off switch too.
- `scripts/judge_parallel_bedrock.py` — Bedrock stand-in for the Codex judge.
- `scripts/run_parallel_typeI_{minimax,glm5,qwen3coder}.sh` — resumable Type I run +
  scoring. `scripts/run_status.py` — live progress of a run.
- `viewer/` — local read-only page over a run dir (`serve.py` + `index.html`, no
  dependency beyond `harness/`). It parses turns with the agent's own tag parser and
  shows the hidden law (`simulator/formula.py`, the judge's `gt_summary`), so it is for
  people only: never feed its output to an agent.
- `experiments/` — tracked run outputs: the GLM-5 reference run and the guided
  Qwen3 Coder and MiniMax M2.5 runs. Older and failed runs, including the unguided Qwen3 Coder
  reference run, are in git at commit `240e29b`. `batch_runs/`, `results/`,
  `submissions/`, `parallel_stage/`, `parallel_out/` are gitignored anywhere,
  except `submissions/` and `parallel_out/` under `experiments/`.
  `parallel_stage/` stays ignored there: it copies the hidden `formula.py`.
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
- A submission must call `<experiment>` at least once, but the last-chance call
  after turn 30 (`agent.py`, end of `conduct_exploration`) accepts a formula with
  no successful experiment: `mincer_earnings_acs_pums__log_wage` on Qwen3 Coder
  submitted with 0 experiments and was judged 0.25. Turn 30 is a forced
  `<final_formula>` turn with one retry. Strict aggregation: no submission,
  contract failure or missing judge result scores 0.
- The contract check (`_sample_matrix` in `harness/evaluate_parallel.py`) runs
  `predict` on 8 rows spanning each input's metadata `range`, and an input with no
  `range` (9 of the 66 tasks have one) gets [0, 1]. A negative power or log of that
  input then fails with `predict returned non-finite values` and scores 0, even if
  it is finite on all real data: `her_hor_pt_acid_kucernak__current_density`, where
  `c_acid` lists only `values: [0.5, 4.0]`, on GLM-5 and MiniMax M2.5.
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
- Resuming a batch: `run_batch.py --skip-existing` alone also reruns tasks that
  ended `max_turns_reached` with no formula, which gives the model a second try
  at a task it already failed. Add `--skip-finished` so only interrupted
  (`running*`) or missing tasks rerun; they restart from turn 0, and the
  interrupted attempt's trajectory and log are kept as `*.aborted-<UTC stamp>`.
- Per-task paper scores for every model: `baseline_agent/model_task_scores.json`.
- Summaries and trajectories record absolute paths of this machine.
