#!/usr/bin/env python3
"""Optimize Limbus Company Normal Mirror Dungeon crate farming."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "game-data.json"
LUNACY_DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "lunacy-and-monthly-packs.json"
STORY_DATA_PATH = Path(__file__).resolve().parent.parent / "references" / "story-progression-costs.json"
DATA = json.loads(DATA_PATH.read_text(encoding="utf-8"))
LUNACY_DATA = json.loads(LUNACY_DATA_PATH.read_text(encoding="utf-8"))
STORY_DATA = json.loads(STORY_DATA_PATH.read_text(encoding="utf-8"))
ENK = DATA["enkephalin"]
MD = DATA["mirror_normal"]
HARD = DATA["mirror_hard"]
PASS = DATA["battle_pass"]
SHARD = DATA["egoshard"]
MONTHLY = LUNACY_DATA["monthly_packs"]
RESETS = DATA["resets"]
SEASON_TRANSITION = DATA["season_transition"]
STORY_CHAPTERS = STORY_DATA["chapters"]


@dataclass
class Plan:
    hard_weekly_strategy: str
    total_refills: int
    refill_distribution: str
    lunacy_spent: int
    lunacy_earned: int
    free_lunacy_earned: int
    paid_lunacy_earned: int
    ending_lunacy: int
    ending_free_lunacy: int
    ending_paid_lunacy: int
    total_enkephalin: int
    story_raw_enkephalin_reserved: int
    story_modules_reserved: int
    story_equivalent_enkephalin: int
    modules_created: int
    modules_available_for_md: int
    normal_md_runs: int
    hard_md_runs: int
    hard_bonus_periods: int
    hard_bonus_charges: int
    md_runs: int
    weekly_bonus_claims: int
    pass_xp_earned: int
    ex_levels_earned: int
    crates_earned: int
    expected_shards: float
    leftover_modules: int
    leftover_enkephalin: int


def parse_start(value: str | None) -> datetime:
    if value is None:
        return datetime.now(ZoneInfo(RESETS["timezone"]))
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=ZoneInfo(RESETS["timezone"]))
    return parsed


def bonus_charge_periods(start: datetime, days: int, used_now: int) -> tuple[list[tuple[int, int]], datetime]:
    """Return (available charges, charges already used) for each weekly period."""
    kst = ZoneInfo(RESETS["timezone"])
    start_kst = start.astimezone(kst)
    end_kst = start_kst + timedelta(days=days)
    days_until_thursday = (3 - start_kst.weekday()) % 7
    next_reset = (start_kst + timedelta(days=days_until_thursday)).replace(
        hour=6, minute=0, second=0, microsecond=0)
    if next_reset <= start_kst:
        next_reset += timedelta(days=7)
    periods = [(3 - used_now, used_now)]
    reset = next_reset
    while reset < end_kst:
        periods.append((3, 0))
        reset += timedelta(days=7)
    return periods, next_reset


def season_transition_status(start: datetime, days: int) -> dict:
    kst = ZoneInfo(SEASON_TRANSITION["warning_boundary_timezone"])
    hour, minute = map(int, SEASON_TRANSITION["warning_boundary_time"].split(":"))
    target = datetime.fromisoformat(SEASON_TRANSITION["target_date"]).replace(
        hour=hour, minute=minute, tzinfo=kst)
    start_kst = start.astimezone(kst)
    end_kst = start_kst + timedelta(days=days)
    return {
        "season_8_target_date": SEASON_TRANSITION["target_date"],
        "official_exact_start_time": SEASON_TRANSITION["official_exact_start_time"],
        "status": SEASON_TRANSITION["status"],
        "warning_boundary_kst": target.isoformat(),
        "warning_boundary_is_official_start_time": False,
        "planning_horizon_crosses_target": start_kst < target < end_kst,
        "planning_starts_on_or_after_target": start_kst >= target,
    }


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


def selected_story_cost(args: argparse.Namespace) -> dict:
    if not args.story_from_id and not args.story_to_id:
        return {"raw_enkephalin": 0, "modules": 0, "equivalent_enkephalin": 0,
                "from_id": None, "to_id": None}
    by_id = {row["id"]: row for row in STORY_CHAPTERS}
    first = args.story_from_id or STORY_CHAPTERS[0]["id"]
    last = args.story_to_id or STORY_CHAPTERS[-1]["id"]
    if first not in by_id or last not in by_id:
        raise ValueError("Unknown story chapter id; run scripts/story_costs.py --list")
    start, end = by_id[first]["order"], by_id[last]["order"]
    if start > end:
        raise ValueError("story-from-id must not come after story-to-id")
    rows = [row for row in STORY_CHAPTERS if start <= row["order"] <= end]
    return {
        "raw_enkephalin": sum(row["raw_enkephalin"] for row in rows),
        "modules": sum(row["modules"] for row in rows),
        "equivalent_enkephalin": sum(row["equivalent_enkephalin"] for row in rows),
        "from_id": first,
        "to_id": last,
    }


def evaluate(args: argparse.Namespace, total_refills: int, hard_strategy: str,
             hard_periods: list[tuple[int, int]]) -> Plan | None:
    cost, distribution = refill_cost_and_distribution(total_refills, args.days)
    natural = math.floor(ENK["natural_per_day"] * args.days * args.natural_utilization)
    total_energy = (
        args.current_enkephalin
        + natural
        + args.enkephalin_boxes * ENK["per_box"]
        + total_refills * args.enkephalin_cap
    )
    story = args.story_cost
    if total_energy < story["raw_enkephalin"]:
        return None
    modules_created, energy_remainder = divmod(
        total_energy - story["raw_enkephalin"], ENK["per_module"])
    reserved = args.daily_reserved_modules * args.days
    available = max(0, args.modules + modules_created - reserved - story["modules"])
    hard_modules = hard_runs = hard_xp = hard_lunacy = hard_charges = 0
    sequence = HARD["separate_single_claims"]["pass_xp_sequence"]
    if hard_strategy != "none":
        for charges, already_used in hard_periods:
            if charges <= 0:
                continue
            hard_charges += charges
            hard_modules += charges * HARD["module_cost_per_bonus_charge"]
            hard_lunacy += charges * MD["weekly_bonus_lunacy"]
            if charges == 3 and already_used == 0 and hard_strategy == "triple":
                hard_runs += 1
                hard_xp += HARD["triple_claim"]["pass_xp"]
            else:
                hard_runs += charges
                hard_xp += sum(sequence[already_used:already_used + charges])
    if available < hard_modules or hard_runs > args.max_md_runs:
        return None
    remaining_modules = available - hard_modules
    remaining_run_slots = args.max_md_runs - hard_runs
    normal_runs = min(remaining_modules // MD["module_cost"], remaining_run_slots)
    runs = hard_runs + normal_runs
    bonus_claims = min(normal_runs, args.weekly_bonus_claims)
    free_lunacy_earned = (hard_lunacy
                          + bonus_claims * MD["weekly_bonus_lunacy"]
                          + args.maintenance_compensations * args.maintenance_compensation_amount
                          + args.other_lunacy_income
                          + args.large_monthly_days * MONTHLY["large"]["daily_free"]
                          + args.small_monthly_days * MONTHLY["small"]["daily_free"])
    paid_lunacy_earned = (args.other_paid_lunacy_income
                          + (MONTHLY["large"]["upfront_paid"] if args.include_large_monthly_upfront else 0)
                          + (MONTHLY["small"]["upfront_paid"] if args.include_small_monthly_upfront else 0))
    lunacy_earned = free_lunacy_earned + paid_lunacy_earned
    free_available = args.lunacy + args.free_lunacy + free_lunacy_earned
    paid_available = args.paid_lunacy + paid_lunacy_earned
    ending_free_lunacy = max(0, free_available - cost)
    paid_spent = max(0, cost - free_available)
    ending_paid_lunacy = paid_available - paid_spent
    ending_lunacy = ending_free_lunacy + ending_paid_lunacy
    if ending_lunacy < args.lunacy_reserve or ending_paid_lunacy < args.paid_lunacy_reserve:
        return None

    pass_xp = (normal_runs * MD["base_pass_xp"]
               + bonus_claims * MD["weekly_bonus_extra_pass_xp"]
               + hard_xp
               + args.other_pass_xp)
    excess_xp = max(0, pass_xp - args.xp_to_pass_cap)
    ex_levels = (args.post_cap_xp_progress + excess_xp) // PASS["xp_per_level"]
    crates_per_level = PASS["free_crates_per_ex_level"]
    if args.paid_pass:
        crates_per_level += PASS["paid_extra_crates_per_ex_level"]
    crates = ex_levels * crates_per_level
    modules_used = hard_modules + normal_runs * MD["module_cost"]

    return Plan(
        hard_weekly_strategy=hard_strategy,
        total_refills=total_refills,
        refill_distribution=distribution,
        lunacy_spent=cost,
        lunacy_earned=lunacy_earned,
        free_lunacy_earned=free_lunacy_earned,
        paid_lunacy_earned=paid_lunacy_earned,
        ending_lunacy=ending_lunacy,
        ending_free_lunacy=ending_free_lunacy,
        ending_paid_lunacy=ending_paid_lunacy,
        total_enkephalin=total_energy,
        story_raw_enkephalin_reserved=story["raw_enkephalin"],
        story_modules_reserved=story["modules"],
        story_equivalent_enkephalin=story["equivalent_enkephalin"],
        modules_created=modules_created,
        modules_available_for_md=available,
        normal_md_runs=normal_runs,
        hard_md_runs=hard_runs,
        hard_bonus_periods=(sum(1 for charges, _ in hard_periods if charges > 0)
                            if hard_strategy != "none" else 0),
        hard_bonus_charges=hard_charges,
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
    p.add_argument("--free-lunacy", type=int, default=0)
    p.add_argument("--paid-lunacy", type=int, default=0)
    p.add_argument("--lunacy-reserve", type=int, default=0)
    p.add_argument("--paid-lunacy-reserve", type=int, default=0,
                   help="Paid Lunacy protected for Pass or other paid-only purchases")
    p.add_argument("--current-enkephalin", type=int, default=0)
    p.add_argument("--modules", type=int, default=0)
    p.add_argument("--enkephalin-boxes", type=int, default=0)
    p.add_argument("--natural-utilization", type=float, default=1.0,
                   help="Fraction of natural regeneration captured, from 0 to 1")
    p.add_argument("--daily-reserved-modules", type=int, default=0)
    p.add_argument("--max-md-runs", type=int, default=10**9)
    p.add_argument("--weekly-bonus-claims", type=int, default=None,
                   help="Normal bonus claims outside Hard; defaults to 0 when Hard is unlocked")
    p.add_argument("--hard-weeks", type=int, default=None,
                   help="Weeks whose three Weekly Bonus charges are spent in Hard")
    p.add_argument("--start-datetime",
                   help="ISO datetime; defaults to the current time in Asia/Seoul")
    p.add_argument("--weekly-bonus-charges-used", type=int, default=0,
                   help="Charges already consumed in the current weekly period, 0-3")
    p.add_argument("--no-hard-unlocked", action="store_true",
                   help="Hard Mirror Dungeon is not unlocked; allocate bonuses to Normal")
    p.add_argument("--maintenance-compensations", type=int, default=0,
                   help="Number of announced ordinary maintenance gifts to include")
    p.add_argument("--maintenance-compensation-amount", type=int,
                   default=RESETS["scheduled_maintenance_compensation_typical_free_lunacy"],
                   help="Free Lunacy per included maintenance gift; default 300")
    p.add_argument("--story-from-id",
                   help="First story chapter to reserve; see scripts/story_costs.py --list")
    p.add_argument("--story-to-id",
                   help="Last story chapter to reserve; see scripts/story_costs.py --list")
    p.add_argument("--hard-weekly-strategy", choices=("none", "triple", "separate", "auto"),
                   default="auto", help="Triple in one run, three separate single claims, or compare both")
    p.add_argument("--other-lunacy-income", type=int, default=0)
    p.add_argument("--other-paid-lunacy-income", type=int, default=0)
    p.add_argument("--large-monthly-days", type=int, default=0,
                   help="Large monthly-card login rewards claimable during the horizon")
    p.add_argument("--small-monthly-days", type=int, default=0,
                   help="Small monthly-card login rewards claimable during the horizon")
    p.add_argument("--include-large-monthly-upfront", action="store_true",
                   help="Include 650 Paid Lunacy from a new large monthly-card purchase")
    p.add_argument("--include-small-monthly-upfront", action="store_true",
                   help="Include 130 Paid Lunacy from a new small monthly-card purchase")
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
    if args.large_monthly_days > args.days or args.small_monthly_days > args.days:
        p.error("monthly-card claim days cannot exceed planning days")
    if not 0 <= args.weekly_bonus_charges_used <= 3:
        p.error("weekly-bonus-charges-used must be between 0 and 3")
    for name in ("lunacy", "free_lunacy", "paid_lunacy", "lunacy_reserve",
                 "paid_lunacy_reserve", "current_enkephalin", "modules",
                 "enkephalin_boxes", "daily_reserved_modules", "max_md_runs",
                 "other_lunacy_income", "other_paid_lunacy_income",
                 "large_monthly_days", "small_monthly_days", "other_pass_xp",
                 "xp_to_pass_cap", "maintenance_compensations", "maintenance_compensation_amount"):
        if getattr(args, name) < 0:
            p.error(f"{name.replace('_', '-')} cannot be negative")
    if args.hard_weeks is not None and args.hard_weeks < 0:
        p.error("hard-weeks cannot be negative")
    if args.weekly_bonus_claims is not None and args.weekly_bonus_claims < 0:
        p.error("weekly-bonus-claims cannot be negative")
    return args


def main() -> None:
    args = parse_args()
    try:
        args.story_cost = selected_story_cost(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    start = parse_start(args.start_datetime)
    season_status = season_transition_status(start, args.days)
    derived_periods, next_reset = bonus_charge_periods(
        start, args.days, args.weekly_bonus_charges_used)
    if args.hard_weeks is not None:
        hard_periods = [(3, 0)] * args.hard_weeks
    elif args.no_hard_unlocked:
        hard_periods = []
    else:
        hard_periods = derived_periods
    if args.weekly_bonus_claims is None:
        args.weekly_bonus_claims = (sum(charges for charges, _ in derived_periods)
                                     if args.no_hard_unlocked else 0)
    crates_per_level = PASS["free_crates_per_ex_level"]
    if args.paid_pass:
        crates_per_level += PASS["paid_extra_crates_per_ex_level"]
    max_refills = args.days * ENK["max_daily_refills"]
    if not hard_periods or args.hard_weekly_strategy == "none":
        strategies = ["none"]
    elif args.hard_weekly_strategy == "auto":
        strategies = ["triple", "separate"]
    else:
        strategies = [args.hard_weekly_strategy]
    plans = [evaluate(args, r, strategy, hard_periods)
             for strategy in strategies for r in range(max_refills + 1)]
    feasible = [p for p in plans if p is not None]
    if not feasible:
        raise SystemExit("No feasible plan preserves the requested Lunacy reserve.")
    feasible.sort(key=lambda p: (-p.crates_earned, -p.expected_shards,
                                 p.lunacy_spent, p.md_runs, p.total_refills))
    best = feasible[0]

    alternatives = []
    for candidate in feasible[1:]:
        signature = (candidate.hard_weekly_strategy, candidate.total_refills)
        if signature != (best.hard_weekly_strategy, best.total_refills):
            alternatives.append(candidate)
        if len(alternatives) == 2:
            break

    result = {
        "objective": "maximize recurring nominable Egoshard crates from Normal and weekly Hard Mirror Dungeon",
        "recommended": asdict(best),
        "generic_identity_equivalent": {
            "default_shard_cost_per_identity": SHARD["default_identity_cost"],
            "expected_complete_identities": best.expected_shards // SHARD["default_identity_cost"],
            "expected_fractional_identities": best.expected_shards / SHARD["default_identity_cost"],
            "expected_shards_toward_next_identity": best.expected_shards % SHARD["default_identity_cost"],
            "note": "Generic Identities default to 400 shards unless the user explicitly specifies another cost.",
        },
        "schedule": {
            "start": start.isoformat(),
            "start_weekday": start.strftime("%A"),
            "next_weekly_reset_kst": next_reset.isoformat(),
            "next_weekly_reset_in_start_timezone": next_reset.astimezone(start.tzinfo).isoformat(),
            "weekly_reset_rule": "Thursday 06:00 Asia/Seoul",
            "bonus_periods_in_horizon": len(derived_periods),
            "bonus_charges_available_in_horizon": sum(c for c, _ in derived_periods),
            "hard_unlocked_assumed": not args.no_hard_unlocked,
            "maintenance_compensation_is_forecast_only": args.maintenance_compensations > 0,
            "season_transition": season_status,
        },
        "story_progression": args.story_cost,
        "alternatives": [asdict(p) for p in alternatives],
        "hard_weekly_comparison_per_week": {
            "one_triple_claim": {
                "runs": HARD["triple_claim"]["runs"],
                "modules": HARD["triple_claim"]["module_cost"],
                "pass_xp": HARD["triple_claim"]["pass_xp"],
                "lunacy": HARD["weekly_lunacy_total"],
            },
            "three_separate_single_claims": {
                "runs": HARD["separate_single_claims"]["runs"],
                "modules": HARD["separate_single_claims"]["module_cost"],
                "pass_xp_sequence": HARD["separate_single_claims"]["pass_xp_sequence"],
                "pass_xp": HARD["separate_single_claims"]["pass_xp"],
                "lunacy": HARD["weekly_lunacy_total"],
            },
            "separate_claim_advantage": {
                "extra_runs": 2,
                "extra_pass_xp": 25,
                "extra_ex_levels_average": 2.5,
                "extra_crates_average": 7.5 if args.paid_pass else 2.5,
            },
        },
        "assumptions": {
            "data_verified_date": DATA["verified_date"],
            "natural_enkephalin_per_day": ENK["natural_per_day"],
            "enkephalin_per_module": ENK["per_module"],
            "enkephalin_per_box": ENK["per_box"],
            "normal_md_module_cost": MD["module_cost"],
            "normal_md_base_pass_xp": MD["base_pass_xp"],
            "weekly_bonus_extra_pass_xp": MD["weekly_bonus_extra_pass_xp"],
            "weekly_bonus_lunacy": MD["weekly_bonus_lunacy"],
            "hard_triple_modules": HARD["triple_claim"]["module_cost"],
            "hard_triple_pass_xp": HARD["triple_claim"]["pass_xp"],
            "hard_separate_modules": HARD["separate_single_claims"]["module_cost"],
            "hard_separate_pass_xp": HARD["separate_single_claims"]["pass_xp"],
            "hard_weekly_lunacy": HARD["weekly_lunacy_total"],
            "pass_xp_per_level": PASS["xp_per_level"],
            "crates_per_ex_level": crates_per_level,
            "expected_shards_per_crate": SHARD["crate_expected"],
            "default_shards_per_identity": SHARD["default_identity_cost"],
            "large_monthly_upfront_paid": MONTHLY["large"]["upfront_paid"],
            "large_monthly_daily_free": MONTHLY["large"]["daily_free"],
            "small_monthly_upfront_paid": MONTHLY["small"]["upfront_paid"],
            "small_monthly_daily_free": MONTHLY["small"]["daily_free"],
            "refill_currency_priority": ["free_lunacy", "paid_lunacy"],
        },
        "warnings": ([
            "Planning horizon reaches the configured 2026-09-17 Season 8 boundary. "
            "Do not apply Season 7 fixed Pass rewards after the boundary; use Season 8 data."
        ] if (season_status["planning_horizon_crosses_target"]
              or season_status["planning_starts_on_or_after_target"]) else []),
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
            print(f"  hard={plan.hard_weekly_strategy}, refills={plan.total_refills}, cost={plan.lunacy_spent}, "
                  f"runs={plan.md_runs}, crates={plan.crates_earned}, "
                  f"ending_lunacy={plan.ending_lunacy}")


if __name__ == "__main__":
    main()
