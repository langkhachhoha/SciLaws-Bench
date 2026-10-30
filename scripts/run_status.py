#!/usr/bin/env python3
"""Progress of a Parallel batch run, read from its trajectory checkpoints.

    .venv/bin/python scripts/run_status.py [RUN_DIR]
    watch -n 20 .venv/bin/python scripts/run_status.py      # live, Ctrl-C to quit

run_batch.py prints a line only when a task finishes; this shows the turns of
tasks still in flight. Read-only: safe while the run is going.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# on-demand, us-east-1, AWS Price List 2026-10-30, $ per 1M tokens (in, out)
PRICE = {"br-glm-5": (1.00, 3.20), "br-qwen3-coder-30b": (0.15, 0.60)}


def main() -> int:
    run = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "experiments" / "parallel_typeI_br-glm-5"
    meta = json.loads((run / "run_meta.json").read_text())
    now = time.time()
    rows, tokens = [], [0, 0]
    looping = 0
    for model in meta["models"]:
        for ttype in meta["task_types"]:
            n_tasks = len(list((REPO / "tasks" / ttype).glob("*/metadata.yaml")))
            traj_dir = run / "parallel" / "trajectories" / model / ttype
            sub_dir = run / "parallel" / "submissions" / model / ttype
            counts = {"submitted": 0, "no formula": 0, "running": 0}
            for traj in sorted(traj_dir.glob("*.traj.json")):
                try:
                    trial = json.loads(traj.read_text())["trial"]
                except Exception:  # caught mid-write; next refresh reads it
                    continue
                task = traj.name[: -len(".traj.json")]
                sub = sub_dir / f"{task}.py"
                usage = trial.get("usage_total") or {}
                tokens[0] += int(usage.get("prompt_tokens") or 0)
                tokens[1] += int(usage.get("completion_tokens") or 0)
                # Byte-identical consecutive replies: a stuck model uses up its
                # turns without learning anything, which turn counts alone hide.
                replies = [m["content"] for m in trial.get("chat_history") or []
                           if m["role"] == "assistant"]
                repeats = sum(bool(a) and a == b for a, b in zip(replies, replies[1:]))
                looping += repeats >= 3
                if sub.exists() and sub.read_text(errors="replace").strip():
                    counts["submitted"] += 1
                elif trial.get("status") == "max_turns_reached":
                    counts["no formula"] += 1
                else:
                    counts["running"] += 1
                    rows.append((task, len(trial.get("usage_per_turn") or []),
                                 trial.get("n_experiments", 0), trial.get("n_python_calls", 0),
                                 repeats, now - traj.stat().st_mtime))
            started = sum(counts.values())
            print(f"{model} {ttype}: {counts['submitted']} submitted, {counts['no formula']} "
                  f"ended without formula, {counts['running']} running or interrupted, "
                  f"{n_tasks - started} not started  (of {n_tasks})")
    price = PRICE.get(meta["models"][0])
    cost = f"  ~${(tokens[0] * price[0] + tokens[1] * price[1]) / 1e6:.2f}" if price else ""
    print(f"agent tokens so far: {tokens[0]:,} in / {tokens[1]:,} out{cost}")
    print(f"tasks repeating a reply 3+ times: {looping}\n")
    if rows:
        print(f"{'task':58} {'turn':>4} {'exp':>3} {'py':>3} {'rep':>3} {'idle':>6}")
        for task, turns, exp, py, repeats, idle in rows:
            # a checkpoint idle for many minutes with no live process = interrupted
            print(f"{task[:58]:58} {turns:>4} {exp:>3} {py:>3} {repeats:>3} {idle:>5.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
