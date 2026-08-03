#!/usr/bin/env python3
"""List or sum minimum Limbus Company story progression costs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "story-progression-costs.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
CHAPTERS = DATA["chapters"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--from-id", help="First included chapter id; defaults to the first chapter")
    p.add_argument("--to-id", help="Last included chapter id; defaults to the final listed chapter")
    p.add_argument("--type", choices=("all", "canto", "intervallo"), default="all")
    p.add_argument("--list", action="store_true", help="List all known chapter ids and costs")
    p.add_argument("--json", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    by_id = {row["id"]: row for row in CHAPTERS}
    if args.from_id and args.from_id not in by_id:
        raise SystemExit(f"Unknown --from-id: {args.from_id}")
    if args.to_id and args.to_id not in by_id:
        raise SystemExit(f"Unknown --to-id: {args.to_id}")
    start = by_id[args.from_id]["order"] if args.from_id else CHAPTERS[0]["order"]
    end = by_id[args.to_id]["order"] if args.to_id else CHAPTERS[-1]["order"]
    if start > end:
        raise SystemExit("--from-id must not come after --to-id")
    selected = [r for r in CHAPTERS if start <= r["order"] <= end]
    if args.type != "all":
        selected = [r for r in selected if r["type"] == args.type]
    result = {
        "from_id": args.from_id or CHAPTERS[0]["id"],
        "to_id": args.to_id or CHAPTERS[-1]["id"],
        "filter": args.type,
        "chapters": selected,
        "totals": {
            "raw_enkephalin": sum(r["raw_enkephalin"] for r in selected),
            "modules": sum(r["modules"] for r in selected),
            "equivalent_enkephalin": sum(r["equivalent_enkephalin"] for r in selected),
        },
        "definition": DATA["definition"],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    for row in selected:
        print(f'{row["id"]}: {row["display"]} | {row["raw_enkephalin"]} Enkephalin '
              f'+ {row["modules"]} Modules = {row["equivalent_enkephalin"]} equivalent')
    print("Totals")
    for key, value in result["totals"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
