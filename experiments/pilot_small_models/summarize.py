"""Summarize pilot trajectories per model (and judge scores if present)."""
import csv
import json
import sys
from pathlib import Path

P = Path(sys.argv[1])
PRICE = {  # $/1M in, out (AWS Price List, us-east-1, 2026-10-30)
    "qwen.qwen3-32b-v1_0": (0.15, 0.6), "qwen.qwen3-coder-30b-a3b-v1_0": (0.15, 0.6),
    "us.meta.llama4-maverick-17b-instruct-v1_0": (0.24, 0.97), "amazon.nova-lite-v1_0": (0.06, 0.24),
    "zai.glm-4.7-flash": (0.07, 0.4), "nvidia.nemotron-nano-3-30b": (0.06, 0.24),
}
judged = {}
summary = P / "judge_out" / "parallel_summary.csv"
if summary.exists():
    for r in csv.DictReader(summary.open()):
        judged[(r["method"], r["task"])] = r["structure_score"]
for mdir in sorted((P / "out").iterdir()):
    trajs = sorted(mdir.glob("*.traj.json"))
    sub = empty = turns = cut = 0
    tin = tout = 0
    scores = []
    for t in trajs:
        tr = json.loads(t.read_text())
        task = t.name[: -len(".traj.json")]
        asst = [m["content"] for m in tr["chat_history"] if m["role"] == "assistant"]
        empty += sum(not a.strip() for a in asst)
        turns += len(asst)
        cut += sum("+cut" in str(u.get("finish_reason")) for u in tr["usage_per_turn"])
        tin += tr["usage_total"]["prompt_tokens"]; tout += tr["usage_total"]["completion_tokens"]
        has = (mdir / f"{task}.py").exists()
        sub += has
        s = judged.get((mdir.name, task))
        scores.append(float(s) if s not in (None, "", "None") else 0.0)
    pi, po = PRICE.get(mdir.name, (0, 0))
    cost = (tin * pi + tout * po) / 1e6 / max(1, len(trajs))
    print(f"{mdir.name:44} submitted {sub}/{len(trajs)}  empty turns {empty}/{turns}  cut {cut}  "
          f"${cost:.3f}/task" + (f"  S_S {scores} mean {sum(scores)/len(scores):.3f}" if judged else ""))
