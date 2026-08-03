#!/usr/bin/env python3
"""Optimize Limbus Company Normal Mirror Dungeon crate farming."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "game-data.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
ENK = DATA["enkephalin"]
MD = DATA["mirror_normal"]
PASS = DATA["battle_pass"]
SHARD = DATA["egoshard"]


@dataclass
class Plan:
    total_refills: int
    refill_distribution: str
    lunacy_spent: int
    lunacy_earned: int
    ending_lunacy: int
    total_enkephalin: int
    modules_created: int
    modules_available_for_md: int
    md_runs: int
    weekly_bonus_claims: int
    pass_xp_earned: int
    ex_levels_earned: int
    crates_earned: int
    expected_shards: float
    leftover_modules: int
    leftover_enkephalin: int


def refill_cost_and_distribution(refills: int, days: int) -> tuple[int, str]:
    q, r = divmod(refills, days)
    max_daily = ENK["max_daily_refills"]
    if q > max_daily or (q == max_daily and r):
        raise ValueError("Refills exceed the daily limit")
    step = ENK["refill_cost_step"]
    cost = days * step * q * (q + 1) // 2 + r * step * (q + 1)
    if r == 0:
        distribution = f"{q}/day for {days} days"
    else:
        distribution = f"{q + 1}/day for {r} days; {q}/day for {days - r} days"
    return cost, distribution


def evaluate(args: argparse.Namespace, total_refills: int) -> Plan | None:
    cost, distribution = refill_cost_and_distribution(total_refills, args.days)
    natural = math.floor(ENK["natural_per_day"] * args.days * args.natural_utilization)
    total_energy = (
        args.current_enkephalin
        + natural
        + args.enkephalin_boxes * ENK["per_box"]
        + total_refills * args.enkephalin_cap
    )
    modules_created, energy_remainder = divmod(total_energy, ENK["per_module"])
    reserved = args.daily_reserved_modules * args.days
    available = max(0, args.modules + modules_created - reserved)
    possible_runs = available // MD["module_cost"]
    runs = min(possible_runs, args.max_md_runs)
    bonus_claims = min(runs, args.weekly_bonus_claims)
    lunacy_earned = bonus_claims * MD["weekly_bonus_lunacy"] + args.other_lunacy_income
    ending_lunacy = args.lunacy + lunacy_earned - cost
    if ending_lunacy < args.lunacy_reserve:
        return None

    pass_xp = (runs * MD["base_pass_xp"]
               + bonus_claims * MD["weekly_bonus_extra_pass_xp"]
               + args.other_pass_xp)
    excess_xp = max(0, pass_xp - args.xp_to_pass_cap)
    ex_levels = (args.post_cap_xp_progress + excess_xp) // PASS["xp_per_level"]
    crates_per_level = PASS["free_crates_per_ex_level"]
    if args.paid_pass:
        crates_per_level += PASS["paid_extra_crates_per_ex_level"]
    crates = ex_levels * crates_per_level
    modules_used = runs * MD["module_cost"]

    return Plan(
        total_refills=total_refills,
        refill_distribution=distribution,
        lunacy_spent=cost,
        lunacy_earned=lunacy_earned,
        ending_lunacy=ending_lunacy,
        total_enkephalin=total_energy,
        modules_created=modules_created,
        modules_available_for_md=available,
        md_runs=runs,
        weekly_bonus_claims=bonus_claims,
        pass_xp_earned=pass_xp,
        ex_levels_earned=ex_levels,
        crates_earned=crates,
        expected_shards=crates * SHARD["crate_expected"],
        leftover_modules=available - modules_used,
        leftover_enkephalin=energy_remainder,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--days", type=int, required=True)
    p.add_argument("--enkephalin-cap", type=int, required=True)
    p.add_argument("--lunacy", type=int, default=0)
    p.add_argument("--lunacy-reserve", type=int, default=0)
    p.add_argument("--current-enkephalin", type=int, default=0)
    p.add_argument("--modules", type=int, default=0)
    p.add_argument("--enkephalin-boxes", type=int, default=0)
    p.add_argument("--natural-utilization", type=float, default=1.0,
                   help="Fraction of natural regeneration captured, from 0 to 1")
    p.add_argument("--daily-reserved-modules", type=int, default=0)
    p.add_argument("--max-md-runs", type=int, default=10**9)
    p.add_argument("--weekly-bonus-claims", type=int, default=0)
    p.add_argument("--other-lunacy-income", type=int, default=0)
    p.add_argument("--other-pass-xp", type=int, default=0)
    p.add_argument("--xp-to-pass-cap", type=int, default=0,
                   help="Pass XP still needed to finish level 120")
    p.add_argument("--post-cap-xp-progress", type=int, default=0,
                   help="Current XP progress within the next EX level, 0-9")
    p.add_argument("--paid-pass", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if args.days <= 0 or args.enkephalin_cap <= 0:
        p.error("days and enkephalin-cap must be positive")
    if not 0 <= args.natural_utilization <= 1:
        p.error("natural-utilization must be between 0 and 1")
    if not 0 <= args.post_cap_xp_progress <= 9:
        p.error("post-cap-xp-progress must be between 0 and 9")
    for name in ("lunacy", "lunacy_reserve", "current_enkephalin", "modules",
                 "enkephalin_boxes", "daily_reserved_modules", "max_md_runs",
                 "weekly_bonus_claims", "other_lunacy_income", "other_pass_xp",
                 "xp_to_pass_cap"):
        if getattr(args, name) < 0:
            p.error(f"{name.replace('_', '-')} cannot be negative")
    return args


def main() -> None:
    args = parse_args()
    crates_per_level = PASS["free_crates_per_ex_level"]
    if args.paid_pass:
        crates_per_level += PASS["paid_extra_crates_per_ex_level"]
    max_refills = args.days * ENK["max_daily_refills"]
    plans = [evaluate(args, r) for r in range(max_refills + 1)]
    feasible = [p for p in plans if p is not None]
    if not feasible:
        raise SystemExit("No feasible plan preserves the requested Lunacy reserve.")
    feasible.sort(key=lambda p: (-p.crates_earned, -p.expected_shards,
                                 p.lunacy_spent, p.md_runs, p.total_refills))
    best = feasible[0]

    alternatives = []
    seen = {best.total_refills}
    for delta in (-1, 1, -args.days, args.days):
        target = best.total_refills + delta
        if 0 <= target <= max_refills and target not in seen:
            candidate = evaluate(args, target)
            if candidate is not None:
                alternatives.append(candidate)
                seen.add(target)
        if len(alternatives) == 2:
            break

    result = {
        "objective": "maximize recurring nominable Egoshard crates from Normal Mirror Dungeon",
        "recommended": asdict(best),
        "alternatives": [asdict(p) for p in alternatives],
        "assumptions": {
            "data_verified_date": DATA["verified_date"],
            "natural_enkephalin_per_day": ENK["natural_per_day"],
            "enkephalin_per_module": ENK["per_module"],
            "enkephalin_per_box": ENK["per_box"],
            "normal_md_module_cost": MD["module_cost"],
            "normal_md_base_pass_xp": MD["base_pass_xp"],
            "weekly_bonus_extra_pass_xp": MD["weekly_bonus_extra_pass_xp"],
            "weekly_bonus_lunacy": MD["weekly_bonus_lunacy"],
            "pass_xp_per_level": PASS["xp_per_level"],
            "crates_per_ex_level": crates_per_level,
            "expected_shards_per_crate": SHARD["crate_expected"],
        },
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Recommended plan")
    for key, value in asdict(best).items():
        print(f"  {key}: {value}")
    if alternatives:
        print("Alternatives")
        for plan in alternatives:
            print(f"  refills={plan.total_refills}, cost={plan.lunacy_spent}, "
                  f"runs={plan.md_runs}, crates={plan.crates_earned}, "
                  f"ending_lunacy={plan.ending_lunacy}")


if __name__ == "__main__":
    main()
