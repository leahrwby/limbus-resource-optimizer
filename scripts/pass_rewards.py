#!/usr/bin/env python3
"""List and total fixed Season 7 Limbus Pass rewards for a level range."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "season-7-pass-rewards.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-level", type=int, required=True, help="First reward level to include")
    parser.add_argument("--to-level", type=int, required=True, help="Last reward level to include")
    parser.add_argument("--paid-pass", action="store_true", help="Include paid rewards in addition to free rewards")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.from_level <= args.to_level <= 120:
        parser.error("level range must satisfy 1 <= from-level <= to-level <= 120")
    return args


def main() -> None:
    args = parse_args()
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    selected = [row for row in data["levels"] if args.from_level <= row["level"] <= args.to_level]
    totals: dict[str, int] = defaultdict(int)
    levels = []
    for row in selected:
        rewards = list(row["free"])
        if args.paid_pass:
            rewards += row["paid"]
        for reward in rewards:
            totals[reward["display"]] += reward["quantity"]
        levels.append({"level": row["level"], "rewards": rewards})
    result = {
        "season": data["season"],
        "from_level": args.from_level,
        "to_level": args.to_level,
        "paid_pass": args.paid_pass,
        "levels": levels,
        "totals": dict(sorted(totals.items())),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"Season 7 levels {args.from_level}-{args.to_level}")
    for row in levels:
        rewards = "; ".join(
            f'{x["display"]} x{x["quantity"]}' if x["quantity"] != 1 else x["display"]
            for x in row["rewards"]
        )
        print(f'  {row["level"]}: {rewards or "No reward"}')
    print("Totals")
    for name, quantity in result["totals"].items():
        print(f"  {name}: {quantity}")


if __name__ == "__main__":
    main()

