"""Replay the moment a model hits the equal-length error, thinking on vs off.

Takes a Flash pilot trajectory, cuts the history right after the first error
(depth 1) or after 5 identical call/error pairs (depth 5), and resamples the next
reply. Temperature is varied too, so it cannot pass for the effect of thinking.
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
from botocore.config import Config

REPO = str(Path(__file__).resolve().parents[2])
sys.path[:0] = [f"{REPO}/baseline_agent"]
from call_llm_api import _cut_after_first_tool, _split_inline_reasoning  # noqa: E402

PILOT = sys.argv[1]
TASKS = ["cepheid_period_luminosity__M_W", "baseball_pythagorean_winpct_lahman__win_pct",
         "hea_hardness_lattice_distortion_couzinie__HV"]
MODELS = {"GLM-5": "zai.glm-5", "GLM-4.7 Flash": "zai.glm-4.7-flash"}
VARIANTS = {"thinking off, T=0.4": {"temperature": 0.4},
            "thinking off, default T": {},
            "thinking ON": {"reasoning_effort": "high"}}
N = 5
rt = boto3.client("bedrock-runtime", region_name="us-east-1",
                  config=Config(read_timeout=300, retries={"mode": "standard", "max_attempts": 4},
                                max_pool_connections=64))


def history(task, depth):
    h = json.load(open(f"{PILOT}/out/zai.glm-4.7-flash/{task}.traj.json"))["chat_history"]
    err = next(i for i, m in enumerate(h) if m["role"] == "user" and "must have equal length" in m["content"])
    return h[:err + 1] + [h[err - 1], h[err]] * (depth - 1), h[err - 1]["content"]


def verdict(reply, bad):
    if reply.strip() == bad.strip():
        return "same call"
    m = re.search(r"<experiment>(.*?)</experiment>", reply, re.S)
    if m:
        try:
            d = json.loads(m.group(1))
        except Exception:
            return "changed, bad json"
        lens = {len(v) for k, v in d.items() if isinstance(v, list)}
        return "fixed" if len(lens) == 1 else "changed, still unequal"
    return "fixed" if ("<python>" in reply or "<final_formula>" in reply) else "other"


def one(job):
    mname, vname, task, depth, _ = job
    msgs, bad = history(task, depth)
    body = {"messages": msgs, "max_tokens": 16384, **VARIANTS[vname]}
    try:
        out = json.loads(rt.invoke_model(modelId=MODELS[mname], body=json.dumps(body))["body"].read())
    except Exception as e:
        return job, f"ERR {type(e).__name__}"
    _, vis = _split_inline_reasoning(out["choices"][0]["message"].get("content") or "")
    return job, verdict(_cut_after_first_tool(vis)[0], bad)


jobs = [(m, v, t, d, i) for m in MODELS for v in VARIANTS for t in TASKS for d in (1, 5) for i in range(N)]
with ThreadPoolExecutor(24) as ex:
    res = list(ex.map(one, jobs))
print(f"{N} tries x {len(TASKS)} tasks = {N * len(TASKS)} replies per cell; 'fixed' = valid next step\n")
print(f"{'model':15} {'setting':25} {'depth':>5}  fixed  same  other")
for m in MODELS:
    for v in VARIANTS:
        for d in (1, 5):
            r = [x for j, x in res if j[0] == m and j[1] == v and j[3] == d]
            print(f"{m:15} {v:25} {d:5}  {r.count('fixed'):5} {r.count('same call'):5} "
                  f"{len(r) - r.count('fixed') - r.count('same call'):5}")
print("\nerrors/other kinds:", {k: sum(1 for _, x in res if x == k) for k in sorted({x for _, x in res}) if k not in ("fixed", "same call")})
