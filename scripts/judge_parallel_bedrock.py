#!/usr/bin/env python3
"""Run the SciLaws-Parallel structure judge on Amazon Bedrock instead of Codex.

`harness/evaluate_parallel.py --dispatch codex` shells out to `codex exec`. When
only Bedrock access is available, stage with the official scorer, judge here,
and the official aggregation (contract gate + strict mean) runs at the end:

    python harness/evaluate_parallel.py --tasks-dir tasks --submissions <subs> \
        --stage-dir <stage> --output-dir <out> --method-name <model> --overwrite
    python scripts/judge_parallel_bedrock.py --manifest <stage>/manifest.json

The judge prompt is the verbatim one `evaluate_parallel.py` writes for Codex
(paper Appendix C.5), one staged task per call, with the three staged files
inlined: this judge is a single model call, not a file-reading code agent. The
paper's judge is GPT-5.4-mini running as a code agent, so these scores share the
protocol but not the judge.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "harness"))

from evaluate_parallel import _build_prompt, aggregate_parallel_outputs  # noqa: E402

DEFAULT_JUDGE_MODEL = "us.anthropic.claude-opus-4-6-v1"

INLINE_NOTE = """
You cannot read or write files in this setting. The three staged files are
inlined verbatim below. Instead of writing OUTPUT_DIR/<stage_id>.json, reply with
that single JSON object inside <result_json>...</result_json> and nothing after it.
"""


def _judge_prompt(stage_dir: Path, output_dir: Path, stage_id: str) -> str:
    task_dir = stage_dir / stage_id
    files = "\n".join(
        f"===== {task_dir / name} =====\n{(task_dir / name).read_text(encoding='utf-8')}"
        for name in ("metadata.yaml", "formula.py", "submission.py")
    )
    return _build_prompt(stage_dir, output_dir, [stage_id]) + INLINE_NOTE + "\n" + files


def _parse_result(text: str) -> dict:
    m = re.search(r"<result_json>(.*?)</result_json>", text, re.DOTALL)
    body = m.group(1) if m else text[text.find("{"):text.rfind("}") + 1]
    return json.loads(body)


def _judge_one(client, args: argparse.Namespace, stage_dir: Path, output_dir: Path,
               stage_id: str) -> str:
    result_path = output_dir / f"{stage_id}.json"
    if result_path.exists() and not args.overwrite:
        return f"{stage_id} skipped (exists)"
    if args.budget_tokens:
        # Sonnet 4.5 / Haiku 4.5 predate adaptive thinking and effort.
        thinking_kwargs = {"thinking": {"type": "enabled", "budget_tokens": args.budget_tokens}}
    else:
        thinking_kwargs = {"thinking": {"type": "adaptive"},
                           "output_config": {"effort": args.effort}}
    with client.messages.stream(
        model=args.model,
        max_tokens=32000,
        messages=[{"role": "user", "content": _judge_prompt(stage_dir, output_dir, stage_id)}],
        # anthropic>=2 defaults to API version 2026-10-21, which Bedrock rejects
        # for models older than Claude 4.7; the classic body version works on all.
        extra_body={"anthropic_version": "bedrock-2023-05-31"},
        **thinking_kwargs,
    ) as stream:
        resp = stream.get_final_message()
    text = "".join(b.text for b in resp.content if b.type == "text")
    log_dir = output_dir / "agent_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / f"{stage_id}.judge.txt").write_text(text, encoding="utf-8")
    try:
        result = _parse_result(text)
    except Exception as exc:
        # No JSON written -> aggregation records missing_result (strict score 0).
        return f"{stage_id} unparseable judge reply: {type(exc).__name__}: {exc}"
    result["task"] = stage_id
    result["judge_model"] = args.model
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return f"{stage_id} structure={result.get('structure_score')}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--manifest", type=Path, required=True,
                    help="manifest.json written by evaluate_parallel.py staging")
    ap.add_argument("--model", default=DEFAULT_JUDGE_MODEL,
                    help="Bedrock model / inference-profile id of the judge")
    ap.add_argument("--region", default=os.getenv("AWS_REGION") or "us-east-1")
    ap.add_argument("--effort", default="medium",
                    help="adaptive-thinking effort (Claude 4.6+ judges)")
    ap.add_argument("--budget-tokens", type=int, default=0,
                    help="fixed thinking budget instead of adaptive+effort, for "
                         "judges without adaptive thinking (Sonnet/Haiku 4.5)")
    ap.add_argument("--max-workers", type=int, default=4)
    ap.add_argument("--overwrite", action="store_true",
                    help="re-judge stage ids that already have a result JSON")
    args = ap.parse_args()

    import anthropic

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    stage_dir = Path(manifest["stage_dir"])
    output_dir = Path(manifest["output_dir"])
    client = anthropic.AnthropicBedrock(aws_region=args.region)
    stage_ids = [item["stage_id"] for item in manifest["staged"]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.max_workers)) as pool:
        futs = [pool.submit(_judge_one, client, args, stage_dir, output_dir, sid)
                for sid in stage_ids]
        for fut in concurrent.futures.as_completed(futs):
            print(fut.result(), flush=True)
    aggregate_parallel_outputs(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
