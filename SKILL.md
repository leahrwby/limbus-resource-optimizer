---
name: limbus-resource-optimizer
description: Optimize Limbus Company Enkephalin, Modules, Free and Paid Lunacy, monthly cards, refill spending, reset-aware Normal and Hard Mirror Dungeon bonuses, Season 7 Pass rewards, recurring Egoshard Crates, and expected Egoshards. Use when a user asks about daily refills, current-week timing, weekly reset, maintenance compensation, how many Hard runs remain, monthly-card value, Paid Lunacy reserves, single-versus-triple Hard claims, Pass rewards, or maximum farming returns under resource and time constraints.
---

# Limbus Resource Optimizer

Use the bundled calculator for arithmetic and optimization. Do not estimate multi-day totals mentally.

## Workflow

1. Read `references/game-data.md` for current constants and terminology.
2. Read `references/season-7-pass-rewards.json` when the user is below Pass level 120, asks about a specific level, or wants exact fixed-track rewards. Use `references/season-7-pass-rewards.md` for a human-readable table.
3. Read `references/lunacy-and-monthly-packs.md` when Paid/Free Lunacy, the large monthly card, the small monthly card, daily paid extraction, or Pass purchasing affects the answer.
4. Read `references/optimization-model.md` when the request asks what is "best", "worthwhile", or "maximum".
5. Read the Season 8 transition section in `references/game-data.md` whenever the planning horizon reaches September 17, 2026, or the user asks about season-end shard/crate handling.
6. Collect known inputs. Ask only for missing values that materially change the answer; otherwise use defaults and label them.
7. Read the current date, weekday, time, and timezone when the user asks what can still be farmed this week. Default to KST rules and convert the reset time to the user's timezone when known.
8. Assume Hard is unlocked unless the user explicitly says it is not. Allocate available Weekly Bonus charges to Hard first; use Normal only when Hard is unavailable or the user requests it.
9. Run `scripts/optimize_resources.py` with the user's constraints. Let it derive bonus periods from the current time unless the user explicitly supplies `--hard-weeks`.
10. For Pass progress below level 120, apply earned XP level by level and list the exact fixed rewards crossed from the Season 7 reward data. Apply paid rewards in addition to free rewards only when the user owns the paid pass.
11. Convert only XP beyond level 120 into recurring crates: 1 free crate plus 2 additional paid crates per EX level.
12. Report the recommended plan plus at least two nearby alternatives.
13. Separate deterministic quantities from expected values. A Nominable Egoshard Crate produces 1-3 shards; use 2 only as an expectation.

## Required inputs

Prefer these inputs:

- planning days;
- Enkephalin cap;
- current Free Lunacy, Paid Lunacy, total reserve, and Paid Lunacy reserve;
- remaining large- and small-monthly-card login days during the planning horizon;
- whether a new monthly-card purchase's upfront Paid Lunacy should be included;
- current Enkephalin, Modules, and Enkephalin Boxes;
- free or paid Limbus Pass;
- Pass XP remaining to level 120, or zero if level 120 is complete;
- current Season 7 Pass level and XP progress when exact pre-120 rewards are requested;
- expected weekly bonus claims in the planning window;
- current datetime/timezone and how many of this week's three Weekly Bonus charges are already used;
- whether Hard is unlocked (default yes unless the user says otherwise);
- number and amount of announced scheduled-maintenance compensations to include; never assume exceptional compensation;
- number of weeks in which Hard weekly rewards will be claimed;
- Hard strategy: one triple-charge run, three separate single-charge runs, or automatic comparison;
- daily Modules reserved for Luxcavation or other content;
- maximum Mirror Dungeon runs the user has time to complete.

Use 100% natural-regeneration utilization only when the user avoids capping. Otherwise request or estimate a utilization percentage.

## Run the calculator

```bash
python scripts/optimize_resources.py \
  --days 30 \
  --enkephalin-cap 150 \
  --free-lunacy 5000 \
  --paid-lunacy 1500 \
  --lunacy-reserve 2600 \
  --paid-lunacy-reserve 1300 \
  --large-monthly-days 30 \
  --small-monthly-days 30 \
  --natural-utilization 0.85 \
  --paid-pass \
  --xp-to-pass-cap 0 \
  --weekly-bonus-charges-used 0 \
  --hard-weekly-strategy auto
```

Use `--help` for all inputs. Add `--json` when structured output is useful.

List exact fixed rewards for a Season 7 level range:

```bash
python scripts/pass_rewards.py --from-level 61 --to-level 80 --paid-pass
```

Omit `--paid-pass` for the free track only. Paid results include both free and paid rewards.

## Interpret the result

- Treat the optimizer's recommendation as maximum recurring crate output under the supplied constraints.
- Always report Hard rewards separately from Normal farming. State whether the plan uses one triple-charge Hard run or three separate single-charge Hard runs.
- Explain that separate Hard claims grant 25 more Pass XP per week at the same 18-Module and 750-Lunacy total, but require two more Hard runs.
- Explain the opportunity cost in Lunacy and gacha pulls: 130 Lunacy is one standard extraction and 1300 is one decaextraction.
- Keep Free and Paid Lunacy separate. Spend Free Lunacy first for refills. Never count Free Lunacy toward a Paid-only purchase.
- Treat monthly-card daily rewards as Free Lunacy and upfront purchase rewards as Paid Lunacy. Count only login days the user expects to claim.
- State the next weekly reset in both KST and the user's timezone. Weekly reset is Thursday 06:00 KST (Thursday 05:00 in Hong Kong/Beijing).
- Treat the common 300-Lunacy maintenance gift as optional forecast income, not a guaranteed weekly reward. Include it only with `--maintenance-compensations` or an explicit announced amount.
- Treat September 17, 2026 as the current target date for Season 8, not a guaranteed exact start time. When a plan crosses it, report the warning, stop applying Season 7 fixed-track rewards after the boundary, and verify the latest official update notice.
- Prefer spreading refills across days because the refill price resets daily and rises by 26 Lunacy per use.
- Do not silently assume 100% natural regeneration. Use 1.0 only when the user reliably avoids the Enkephalin cap; otherwise request an estimate or use a labeled conservative scenario such as 0.85 plus nearby sensitivity cases.
- Warn when the plan consumes Enkephalin Boxes, dips below the requested reserve, assumes uncapped regeneration, or requires more Mirror Dungeon runs than the user can play.
- Do not claim that maximum crates equal maximum account value. Story progress, Luxcavation materials, limited events, and time can dominate crate farming.

## Data maintenance

Before giving a current-version answer, compare the verification dates in `references/game-data.md` and `references/season-7-pass-rewards.json` with the current date. If data may be stale, verify the affected constants against the linked sources and update the Markdown and JSON pair together. Do not silently merge conflicting values.
