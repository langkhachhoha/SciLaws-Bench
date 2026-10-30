"""Teach the `<experiment>` request format on multi-input Parallel tasks.

The simulator pairs input arrays by position, but the frozen prompt only shows a
one-input example and the simulator's error names no fix. Models then send lists
of different lengths, meaning a grid or a held-fixed input, and small models
repeat that for the rest of the task (179 of the 861 turns in the Qwen3 Coder
reference run). See notes/trang_thai_va_buoc_tiep_theo.md.

`install_experiment_guidance` wraps one task in place, which leaves `harness/`,
`baseline_agent/agent.py` and `SimulatorTask` unchanged. A request is still
accepted or rejected exactly as before, under the same caps, and a rejected one
still costs no experiment; only the text the agent reads differs.
"""
from __future__ import annotations

import itertools
import json
import math
from typing import Any, Dict, List, Sequence

import numpy as np


EQUAL_LENGTH_ERROR = "all input arrays must have equal length"
# A corrected request is echoed into the chat, which every later turn resends.
MAX_CORRECTED_POINTS = 64


def _rounded(value: float) -> float:
    return float(f"{value:.4g}")


def experiment_format_note(input_cols: Sequence[str], support: Dict[str, Any]) -> str:
    """The rule plus two examples in the task's own columns and public ranges."""
    low = {c: _rounded(support[c]["min"]) for c in input_cols}
    high = {c: _rounded(support[c]["max"]) for c in input_cols}
    mid = {c: _rounded((support[c]["min"] + support[c]["max"]) / 2) for c in input_cols}
    first, second, *rest = input_cols

    sweep = {first: [low[first], mid[first], high[first]],
             **{c: [mid[c]] * 3 for c in input_cols[1:]}}
    cross = {first: [low[first], low[first], high[first], high[first]],
             second: [low[second], high[second], low[second], high[second]],
             **{c: [mid[c]] * 4 for c in rest}}
    names = ", ".join(f"`{c}`" for c in input_cols)
    return (
        "How `<experiment>` reads a request: input arrays are paired by position, so "
        f"row i of every array is one input point. Every call must list all of {names}, "
        "and all arrays must have the same length. There is no grid expansion and no "
        "broadcasting: a one-element list is not repeated, and arrays of different "
        "lengths are rejected without returning data.\n\n"
        f"To vary `{first}` with the other inputs held fixed, repeat the fixed values:\n"
        f"<experiment>{json.dumps({**sweep, 'n_samples': 3, 'seed': 0})}</experiment>\n\n"
        "To cross inputs, write out every combination:\n"
        f"<experiment>{json.dumps({**cross, 'n_samples': 3, 'seed': 0})}</experiment>\n\n"
        "These two calls only show the format; choose your own input values."
    )


def equal_length_help(request: Dict[str, Any], input_cols: Sequence[str],
                      max_points: int) -> Dict[str, Any]:
    """Fields explaining a rejected request, with a valid one built from it.

    A corrected request crosses the inputs, which covers both intents behind this
    error: lists meant as a grid, and one-element lists meant as a fixed input.
    Above the cap it sweeps the longest input and holds the others at their first
    value, so the agent always gets something it can send.
    """
    arrays: Dict[str, List[Any]] = {c: np.ravel(request[c]).tolist() for c in input_cols}
    lengths = {c: len(a) for c, a in arrays.items()}
    limit = min(max_points, MAX_CORRECTED_POINTS)
    n_grid = math.prod(lengths.values())
    longest = max(arrays, key=lengths.__getitem__)

    corrected = None
    if 0 < n_grid <= limit:
        rows = list(itertools.product(*arrays.values()))
        corrected = {c: [r[i] for r in rows] for i, c in enumerate(arrays)}
        shape = f"every combination of your values ({n_grid} points)"
    elif min(lengths.values()) > 0 and lengths[longest] <= limit:
        n = lengths[longest]
        corrected = {c: a if c == longest else [a[0]] * n for c, a in arrays.items()}
        shape = (f"a sweep of `{longest}` with the other inputs held fixed; every "
                 f"combination would be {n_grid} points, over the limit of {limit}")

    fix = ("Arrays are paired by position: row i of every array is one input point, "
           "so all arrays must have the same length. A one-element list is not "
           "repeated and arrays of different lengths are not expanded into a grid. "
           "No data was returned and this call did not count as an experiment.")
    help_fields: Dict[str, Any] = {"lengths": lengths}
    if corrected is None:
        help_fields["how_to_fix"] = fix + " Resend with every array the same length."
        return help_fields
    help_fields["how_to_fix"] = (
        f"{fix} `corrected_request` below is valid as written: {shape}. Send it inside "
        "`<experiment>`, or write your own request with every array the same length."
    )
    extras = {k: request[k] for k in ("n_samples", "seed") if k in request}
    help_fields["corrected_request"] = {**corrected, **extras}
    return help_fields


def install_experiment_guidance(task: Any) -> None:
    """Wrap one Type I simulator task in place; other tasks are left as they were.

    A one-input task has no arrays to pair, and Type II requests carry `group_id`,
    which this format does not describe.
    """
    if task.has_group_id or len(task.input_cols) < 2:
        return
    base_prompt = task.get_task_prompt
    base_run = task.run_experiment
    support = task.sim_state.get("support") or task.sim_state.get("train_support") or {}

    def get_task_prompt(max_turns: int = 30) -> str:
        return (base_prompt(max_turns=max_turns) + "\n\n"
                + experiment_format_note(task.input_cols, support))

    def run_experiment(**request: Any) -> Dict[str, Any]:
        result = base_run(**request)
        if result.get("error") == EQUAL_LENGTH_ERROR:
            max_points = task.experiment_caps()["max_input_points_per_call"]
            return {**result, **equal_length_help(request, task.input_cols, max_points)}
        return result

    task.get_task_prompt = get_task_prompt
    task.run_experiment = run_experiment
