#!/usr/bin/env python3
"""Estimate story cost and weekly reward tradeoffs for Normal vs Hard Mirror Dungeon."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA = json.loads((Path(__file__).resolve().parent.parent / "references" / "story-progression-costs.json").read_text(encoding="utf-8"))
CHAPTERS = DATA["chapters"]
BY_ID = {row["id"]: row for row in CHAPTERS}
STAGE_DATA = json.loads((Path(__file__).resolve().parent.parent / "references" / "story-stage-costs.json").read_text(encoding="utf-8"))
STAGES = STAGE_DATA["stages"]


def cost_between(start_order: int, end_order: int) -> dict[str, float]:
    rows = [r for r in CHAPTERS if start_order <= r["order"] <= end_order]
    return {
        "raw_enkephalin": sum(r["raw_enkephalin"] for r in rows),
        "modules": sum(r["modules"] for r in rows),
        "equivalent_enkephalin": sum(r["equivalent_enkephalin"] for r in rows),
    }


def scale_first(cost: dict[str, float], chapter: dict, remaining_fraction: float) -> dict[str, float]:
    result = dict(cost)
    completed_fraction = 1 - remaining_fraction
    for key in ("raw_enkephalin", "modules", "equivalent_enkephalin"):
        result[key] -= chapter[key] * completed_fraction
        result[key] = round(result[key], 1)
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    current_group = p.add_mutually_exclusive_group(required=True)
    current_group.add_argument("--current-id", choices=[r["id"] for r in CHAPTERS])
    current_group.add_argument("--current-stage", help="First uncleared story stage, e.g. 3-5")
    p.add_argument("--chapter-progress", type=float, help="Estimated fraction completed, from 0 to 1")
    p.add_argument("--paid-pass", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if args.chapter_progress is not None and not 0 <= args.chapter_progress <= 1:
        p.error("--chapter-progress must be between 0 and 1")

    current = BY_ID[args.current_id] if args.current_id else None
    normal_gate = BY_ID["canto-2"]
    hard_gate = BY_ID["canto-8"]
    multiplier = 3 if args.paid_pass else 1

    def resolve_stage(stage_id: str) -> int:
        matches = [i for i, r in enumerate(STAGES) if r[0] == stage_id]
        if not matches:
            raise SystemExit(f"Unknown --current-stage: {stage_id}")
        if len(matches) > 1:
            choices = ", ".join(f"{STAGES[i][1]}:{stage_id}" for i in matches)
            raise SystemExit(f"Ambiguous stage {stage_id}; use story_costs.py with one of: {choices}")
        return matches[0]

    normal_gate_index = max(i for i, r in enumerate(STAGES) if r[1] == "canto-2")
    hard_gate_index = max(i for i, r in enumerate(STAGES) if r[1] == "canto-8")
    current_stage_index = resolve_stage(args.current_stage) if args.current_stage else None

    def stage_gate_cost(gate_index: int) -> dict[str, float]:
        if current_stage_index > gate_index:
            return {"raw_enkephalin": 0, "modules": 0, "equivalent_enkephalin": 0}
        rows = STAGES[current_stage_index:gate_index + 1]
        raw = sum(r[2] for r in rows)
        modules = sum(r[3] for r in rows)
        return {"raw_enkephalin": raw, "modules": modules, "equivalent_enkephalin": raw + 20 * modules}

    def gate_cost(gate: dict, gate_index: int) -> dict:
        if current_stage_index is not None:
            return stage_gate_cost(gate_index)
        if current["order"] > gate["order"]:
            return {"raw_enkephalin": 0, "modules": 0, "equivalent_enkephalin": 0}
        full = cost_between(current["order"], gate["order"])
        if args.chapter_progress is None:
            minimum = dict(full)
            for key in minimum:
                minimum[key] = round(minimum[key] - current[key], 1)
            return {"minimum_if_current_chapter_almost_clear": minimum, "maximum_if_at_chapter_start": full}
        return scale_first(full, current, 1 - args.chapter_progress)

    result = {
        "current": args.current_stage or current["display"],
        "current_stage_is_uncleared": bool(args.current_stage),
        "normal_unlocked": current_stage_index > normal_gate_index if current_stage_index is not None else current["order"] > normal_gate["order"],
        "hard_unlocked_by_story": current_stage_index > hard_gate_index if current_stage_index is not None else current["order"] > hard_gate["order"],
        "normal_unlock_story_cost": gate_cost(normal_gate, normal_gate_index),
        "hard_unlock_story_cost": gate_cost(hard_gate, hard_gate_index),
        "hard_additional_requirement": "Complete Mirror of Names and Spiders once in Normal.",
        "weekly_comparison_after_unlock": {
            "normal_three_claims": {"modules": 15, "pass_xp": 135, "lunacy": 750},
            "hard_triple": {"modules": 18, "pass_xp": 225, "lunacy": 750, "incremental_crates": 9 * multiplier},
            "hard_three_separate": {"modules": 18, "pass_xp": 250, "lunacy": 750, "incremental_crates": 11.5 * multiplier},
        },
        "warning": "A winner requires the same planning horizon and an estimate of when Canto VIII can be cleared; do not credit Hard bonuses before then.",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
