---
name: limbus-resource-optimizer
description: Optimize Limbus Company Enkephalin, Enkephalin Modules (boxes/pills), Lunacy refills, Mirror Dungeon runs, Limbus Pass XP, Nominable Egoshard Crates, and expected Egoshards. Use when a user asks how many daily stamina refills are worthwhile, how many Mirror Dungeons or pass levels they can obtain, how many crates or shards a resource budget yields, or how to maximize farming returns under Lunacy, time, stamina, module, pass-level, and reserve constraints.
---

# Limbus Resource Optimizer

Use the bundled calculator for arithmetic and optimization. Do not estimate multi-day totals mentally.

## Workflow

1. Read `references/game-data.md` for current constants and terminology.
2. Read `references/optimization-model.md` when the request asks what is "best", "worthwhile", or "maximum".
3. Collect known inputs. Ask only for missing values that materially change the answer; otherwise use defaults and label them.
4. Run `scripts/optimize_resources.py` with the user's constraints.
5. Report the recommended plan plus at least two nearby alternatives.
6. Separate deterministic quantities from expected values. A Nominable Egoshard Crate produces 1–3 shards; use 2 only as an expectation.
7. State whether the account has reached Pass level 120. Never convert pre-120 Pass levels directly into recurring crates.

## Required inputs

Prefer these inputs:

- planning days;
- Enkephalin cap;
- current Lunacy and minimum Lunacy reserve;
- current Enkephalin, Modules, and Enkephalin Boxes;
- free or paid Limbus Pass;
- Pass XP remaining to level 120, or zero if level 120 is complete;
- expected weekly bonus claims in the planning window;
- daily Modules reserved for Luxcavation or other content;
- maximum Mirror Dungeon runs the user has time to complete.

Use 100% natural-regeneration utilization only when the user avoids capping. Otherwise request or estimate a utilization percentage.

## Run the calculator

```bash
python scripts/optimize_resources.py \
  --days 30 \
  --enkephalin-cap 150 \
  --lunacy 6500 \
  --lunacy-reserve 2600 \
  --paid-pass \
  --xp-to-pass-cap 0 \
  --weekly-bonus-claims 12
```

Use `--help` for all inputs. Add `--json` when structured output is useful.

## Interpret the result

- Treat the optimizer's recommendation as maximum recurring crate output under the supplied constraints.
- Explain the opportunity cost in Lunacy and gacha pulls: 130 Lunacy is one standard extraction and 1300 is one decaextraction.
- Prefer spreading refills across days because the refill price resets daily and rises by 26 Lunacy per use.
- Warn when the plan consumes Enkephalin Boxes, dips below the requested reserve, assumes uncapped regeneration, or requires more Mirror Dungeon runs than the user can play.
- Do not claim that maximum crates equal maximum account value. Story progress, Luxcavation materials, limited events, and time can dominate crate farming.

## Data maintenance

Before giving a current-version answer, compare the verification date in `references/game-data.md` with the current date. If the data may be stale, verify the affected constants against the linked sources, then update both `references/game-data.md` and `references/game-data.json`. Do not silently merge conflicting values.
