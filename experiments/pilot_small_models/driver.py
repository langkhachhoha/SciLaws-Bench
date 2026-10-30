"""Pilot driver: the reference agent on one Parallel task with a Converse-backed
non-reasoning model. Swaps only the LLM call (agent.call_llm_api); prompts,
protocol, simulator and caps are the repo's. Usage: driver.py MODEL_ID TASK OUT_DIR"""
import json
import re
import sys
import time
from pathlib import Path

import boto3
from botocore.config import Config

REPO = str(Path(__file__).resolve().parents[2])
sys.path[:0] = [f"{REPO}/baseline_agent", f"{REPO}/harness"]
import agent  # noqa: E402
from call_llm_api import _cut_after_first_tool, _heal_close_tag  # noqa: E402
from task import load_task  # noqa: E402

model_id, task_name, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
rt = boto3.client("bedrock-runtime", region_name="us-east-1",
                  config=Config(read_timeout=600, retries={"mode": "standard", "max_attempts": 4}))
MAX_TOKENS = [8192]


def converse_call(messages, model_name=None, trial_info=None, **_):
    system = messages[0]["content"] if messages[0]["role"] == "system" else ""
    conv = [{"role": m["role"], "content": [{"text": m["content"] or "(no output)"}]}
            for m in messages if m["role"] != "system"]
    for _attempt in range(2):
        try:
            r = rt.converse(modelId=model_id, system=[{"text": system}], messages=conv,
                            inferenceConfig={"maxTokens": MAX_TOKENS[0], "temperature": 0.4})
            break
        except rt.exceptions.ValidationException as e:
            if "token" in str(e).lower() and MAX_TOKENS[0] > 4096:
                MAX_TOKENS[0] = 4096
                continue
            raise
    blocks = r["output"]["message"]["content"]
    text = "".join(b.get("text", "") for b in blocks)
    reasoning = "".join(b.get("reasoningContent", {}).get("reasoningText", {}).get("text", "") for b in blocks)
    think = re.findall(r"<think>(.*?)</think>", text, flags=re.S)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text, dropped = _cut_after_first_tool(text)
    u = r["usage"]
    return _heal_close_tag(text), (reasoning + "".join(think)) or None, {
        "prompt_tokens": u["inputTokens"], "prompt_cached_tokens": u.get("cacheReadInputTokens", 0),
        "completion_tokens": u["outputTokens"], "reasoning_tokens": 0,
        "total_tokens": u["inputTokens"] + u["outputTokens"],
        "finish_reason": r["stopReason"] + ("+cut" if dropped else ""), "model": model_id, "api_source": "pilot"}


agent.call_llm_api = converse_call
task = load_task(f"{REPO}/tasks/typeI/{task_name}", simulator="simulator", show_test_range=False)
t0 = time.time()
trial = agent.conduct_exploration(task, model_name=model_id, max_turns=30)
trial["elapsed_s"] = time.time() - t0
(out / f"{task_name}.traj.json").write_text(json.dumps(trial, default=str))
if (trial.get("submitted_equation") or "").strip():
    (out / f"{task_name}.py").write_text(trial["submitted_equation"])
print(task_name, model_id, trial["status"], trial["rounds"], f"{trial['elapsed_s']:.0f}s")
