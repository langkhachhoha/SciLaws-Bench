#!/usr/bin/env python3
"""Read a Parallel run turn by turn: what the agent got, thought, did and submitted.

    .venv/bin/python viewer/serve.py              # then open http://127.0.0.1:8765
    .venv/bin/python viewer/serve.py --port 9000

Every run under experiments/ shows up on its own. Any other run is added by pasting
its path into the page. Files are read on each request, so a new or still-running
run needs only a browser refresh. Read-only and bound to localhost.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "harness"))

# The agent's own parser, so a turn shows the block that really ran.
from agent_protocol import TOOL_TAGS, _last_block, first_tool_tag, parse_final_formula  # noqa: E402

TRAJECTORIES = Path("parallel") / "trajectories"
JUDGE_KEYS = ("structure_score", "level", "gt_summary", "submission_summary",
              "matched", "missed", "coefficient_assessment", "judge_model")
TOOL_BLOCK = re.compile(r"<({0})>.*?</\1>".format("|".join(TOOL_TAGS)), re.S)
FEEDBACK = re.compile(r"\s*<(experiment|python)_output>\n?(.*?)\n?</\1_output>(.*)", re.S)
PYTHON_FAILED = "Python execution failed"
CELL = {"experiment": "E", "python": "P", "final": "F"}


def find_runs(raw: str) -> List[Path]:
    """The run dirs a pasted path means: the run itself, the run holding a path
    inside it, or every run directly below a parent such as experiments/."""
    text = raw.strip().strip("'\"").removeprefix("file://")
    path = Path(text).expanduser()
    path = (path if path.is_absolute() else REPO / path).resolve()
    for candidate in (path, *path.parents):
        if (candidate / TRAJECTORIES).is_dir():
            return [candidate]
    if path.is_dir():
        return sorted(p.parent.parent for p in path.glob(f"*/{TRAJECTORIES}"))
    return []


def shown_path(run: Path) -> str:
    return str(run.relative_to(REPO)) if run.is_relative_to(REPO) else str(run)


def model_types(run: Path) -> Iterator[Tuple[str, str]]:
    for model_dir in sorted(p for p in (run / TRAJECTORIES).iterdir() if p.is_dir()):
        for type_dir in sorted(p for p in model_dir.iterdir() if p.is_dir()):
            yield model_dir.name, type_dir.name


def read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):  # absent, or caught mid-write by a live run
        return None


def official_rows(run: Path, model: str, ttype: str) -> Dict[str, Dict[str, str]]:
    """Scorer rows by task. A contract failure scores 0 whatever the judge said."""
    path = run / "parallel_out" / "parallel_summary.csv"
    if not path.exists():
        return {}
    with path.open(newline="") as f:
        return {r["task"]: r for r in csv.DictReader(f)
                if r["method"] == model and r["type"] == ttype}


def as_score(value: Any) -> Optional[float]:
    return None if value in (None, "", "None") else float(value)


def parse_feedback(text: str) -> Tuple[Optional[str], str, str]:
    """(tool that answered or None, its output, what the harness appended after it)."""
    match = FEEDBACK.match(text)
    return (match.group(1), match.group(2), match.group(3).strip()) if match else (None, text, "")


def parse_turns(trial: Dict[str, Any]) -> List[Dict[str, Any]]:
    """One entry per model reply, joined with the feedback it got. The kind comes
    from that feedback, because a tag the model wrote may not have been accepted."""
    history = trial.get("chat_history") or []
    usage = trial.get("usage_per_turn") or []
    turns: List[Dict[str, Any]] = []
    experiments = rows = 0
    for i, message in enumerate(history):
        if message["role"] != "assistant":
            continue
        reply = message["content"] or ""
        feedback = history[i + 1]["content"] if i + 1 < len(history) else None
        spent = usage[len(turns)] if len(turns) < len(usage) else {}
        tag = first_tool_tag(reply)
        tool, output, notice = parse_feedback(feedback) if feedback is not None else (None, "", "")
        turn: Dict[str, Any] = {
            "n": len(turns) + 1,
            "reasoning": (spent.get("reasoning_content") or "").strip(),
            "text": TOOL_BLOCK.sub("", reply).strip(),
            "body": _last_block(reply, f"<{tag}>", f"</{tag}>") if tag else None,
            "blocks": len(TOOL_BLOCK.findall(reply)),
            "tokens": [spent.get("prompt_tokens") or 0, spent.get("completion_tokens") or 0],
            "cut": spent.get("finish_reason") == "length",
            "output": output,
            "notice": notice,
            "ok": True,
        }
        if tool == "experiment":
            turn["kind"] = "experiment"
            turn["request"] = _json_or_none(turn["body"])
            turn["result"] = _json_or_none(output)
            turn["ok"] = turn["result"] is not None and "error" not in turn["result"]
            if turn["ok"]:
                experiments = turn["result"].get("experiment_calls_total", experiments + 1)
                rows = turn["result"].get("train_rows_total", rows)
        elif tool == "python":
            turn["kind"] = "python"
            turn["ok"] = not output.lstrip().startswith(PYTHON_FAILED)
        elif feedback is None and tag == "final_formula":
            turn["kind"] = "final"
            turn["ok"] = parse_final_formula(reply)[0]
        elif feedback is None:
            turn["kind"] = "pending"
        else:
            turn["kind"] = "invalid"
            turn["ok"] = False
        turn["experiments"], turn["rows"] = experiments, rows
        turns.append(turn)
    return turns


def _json_or_none(text: Optional[str]) -> Optional[Dict[str, Any]]:
    try:
        parsed = json.loads(text or "")
    except ValueError:
        return None
    return parsed if isinstance(parsed, dict) else None


def cells(turns: List[Dict[str, Any]]) -> str:
    """One letter per turn; lower case marks a call the harness rejected."""
    out = ""
    for turn in turns:
        if turn["kind"] != "pending":  # a live run's reply, its feedback still to come
            letter = CELL.get(turn["kind"], "?")
            out += letter if turn["ok"] else letter.lower()
    return out


def describe_series(run: Path, model: str, ttype: str) -> Dict[str, Any]:
    official = official_rows(run, model, ttype)
    meta = read_json(run / "run_meta.json") or {}
    tasks: Dict[str, Dict[str, Any]] = {}
    max_experiments = 10
    for path in sorted((run / TRAJECTORIES / model / ttype).glob("*.traj.json")):
        data = read_json(path)
        if data is None:
            continue
        task = path.name[: -len(".traj.json")]
        trial = data["trial"]
        max_experiments = (trial.get("experiment_caps") or {}).get("max_experiment_calls", max_experiments)
        row = official.get(task, {})
        tasks[task] = {
            "score": as_score(row.get("structure_score")),
            "cells": cells(parse_turns(trial)),
            "experiments": trial.get("n_experiments") or 0,
            "status": trial.get("status") or "",
        }
    scored = [t["score"] for t in tasks.values() if t["score"] is not None]
    summary = read_json(run / f"score_{ttype}.json") or {}
    label = run.name.removeprefix(f"parallel_{ttype}_").removeprefix("br-")
    if model.removeprefix("br-") not in label:
        label = f"{label} / {model.removeprefix('br-')}"
    return {
        "id": f"{shown_path(run)}|{model}|{ttype}",
        "path": shown_path(run),
        "model": model,
        "type": ttype,
        "label": label,
        "short": re.split(r"[-_/]", model.removeprefix("br-"))[0],
        "max_turns": meta.get("max_turns") or 30,
        "max_experiments": max_experiments,
        "s_s": summary.get("S_S_strict"),
        "mean_scored": sum(scored) / len(scored) if scored else None,
        "n_scored": len(scored),
        "n_tasks": len(tasks),
        "tasks": tasks,
    }


def read_truth(ttype: str, task: str) -> str:
    """The hidden simulator, the file the judge scores against. The rest of the
    answer key (state.joblib, eval/) is never read."""
    try:
        return (REPO / "tasks" / ttype / task / "simulator" / "formula.py").read_text()
    except OSError:  # tasks/ is not in git and may not be downloaded
        return ""


def describe_task(run: Path, model: str, ttype: str, task: str) -> Dict[str, Any]:
    for part in (model, ttype, task):
        if Path(part).name != part or part in ("", ".", ".."):
            raise ValueError(f"bad name {part!r}")
    data = read_json(run / TRAJECTORIES / model / ttype / f"{task}.traj.json")
    if data is None:
        raise FileNotFoundError(f"no trajectory for {task}")
    trial = data["trial"]
    history = trial.get("chat_history") or []
    prompts = {m["role"]: m["content"] for m in history[:2]}
    row = official_rows(run, model, ttype).get(task, {})
    judge = read_json(run / "parallel_out" / f"{model}__{task}.json")
    target = re.search(r"^Target: (.+)$", prompts.get("user", ""), re.M)
    return {
        "task": task,
        "status": trial.get("status") or "",
        "system": prompts.get("system", ""),
        "prompt": prompts.get("user", ""),
        "target": target.group(1) if target else "",
        "turns": parse_turns(trial),
        "truth": read_truth(ttype, task),
        "score": as_score(row.get("structure_score")),
        "judge_score": as_score(row.get("judge_structure_score")),
        "contract_error": row.get("error") or "",
        "judge": {k: judge.get(k) for k in JUDGE_KEYS} if judge else None,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (http.server's name)
        url = urlparse(self.path)
        query = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/":
                self._send(HTTPStatus.OK, "text/html; charset=utf-8",
                           (Path(__file__).parent / "index.html").read_bytes())
            elif url.path == "/api/runs":
                self._json(self._runs(query["path"]))
            elif url.path == "/api/task":
                run = find_runs(query["path"])
                if len(run) != 1:
                    raise FileNotFoundError(f"no run at {query['path']}")
                self._json(describe_task(run[0], query["model"], query["type"], query["task"]))
            else:
                self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
        except (FileNotFoundError, KeyError, ValueError) as err:
            self._json({"error": str(err)}, HTTPStatus.BAD_REQUEST)

    @staticmethod
    def _runs(path: str) -> Dict[str, Any]:
        runs = find_runs(path)
        if not runs:
            raise FileNotFoundError(
                f"Không thấy run nào ở {path}. Cần thư mục có {TRAJECTORIES}/ bên trong.")
        return {"series": [describe_series(run, model, ttype)
                           for run in runs for model, ttype in model_types(run)]}

    def _json(self, payload: Dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        self._send(status, "application/json; charset=utf-8",
                   json.dumps(payload, ensure_ascii=False).encode())

    def _send(self, status: HTTPStatus, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: Any) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Open http://127.0.0.1:{args.port}  (Ctrl-C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
