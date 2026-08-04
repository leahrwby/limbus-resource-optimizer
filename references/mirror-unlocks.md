# Mirror Dungeon unlock and route comparison

Verified: 2026-08-04  
Current dungeon: Mirror of Names and Spiders

## Unlock conditions

- Normal: clear Canto II.
- Hard: clear Canto VIII and complete Mirror of Names and Spiders once in Normal.
- Clearing the Normal run is a gameplay prerequisite. Reward claiming costs Modules, but entering and clearing the dungeon does not itself require paying the reward-claim cost.

Source: https://limbuscompany.wiki.gg/wiki/Mirror_of_Names_and_Spiders

## Interpretation rules

- If the user gives no story progress, default to Hard unlocked.
- If the user gives a Canto or node, never apply that default. Infer the unlocked modes.
- “In Canto II” means Normal may still be locked. If no node or percentage is supplied, show a range: 0 to the full remaining Canto II cost for Normal, and the corresponding range to the end of Canto VIII for Hard.
- A percentage is only an estimate because stage costs are not uniform. Label it as proportional-cost interpolation.
- Interpret a supplied stage such as `3-5` as uncleared. Use `story-stage-costs.json`; include that stage's entry cost and all later mandatory paid entries through the target gate.

## Fair comparison

Compare two plans over the same user-specified horizon:

1. Normal-first: finish Canto II, claim this week's available bonuses in Normal, and farm Normal until the horizon ends.
2. Hard-rush: reserve story costs through Canto VIII, clear Normal once, then direct only bonus charges available after the unlock to Hard.

Do not count Hard rewards before the estimated unlock date. If the user gives no horizon, report the resource thresholds and weekly marginal advantage, then ask for or illustrate 7-, 30-, and 90-day horizons instead of naming an absolute winner.

Against three weekly Normal bonus claims (15 Modules, 135 XP, 750 Lunacy), Hard costs 18 Modules and yields:

- one triple-charge run: 225 XP and 750 Lunacy; incremental +90 XP for +3 Modules;
- three separate single-charge runs: 250 XP and 750 Lunacy; incremental +115 XP for +3 Modules.

After Pass level 120, the incremental weekly crates are 9/27 (free/paid) for triple-charge and 11.5/34.5 for separate claims, before accounting for partial XP levels. Story progression also unlocks permanent content and first-clear rewards, so a crate-only break-even is not total account value.
