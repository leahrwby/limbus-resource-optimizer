# Limbus Company resource data

Verified: 2026-08-04  
Game context: Season 7, Mirror of Names and Spiders  
Scope: repeatable resource conversion; event rewards and maintenance compensation are excluded unless entered manually.

## Reset schedule and update compensation

- Daily reset: every day at 06:00 KST (UTC+9).
- Weekly reset: every Thursday at 06:00 KST. This refreshes the three Mirror Dungeon Weekly Bonus charges.
- Monthly reset: the first day of each month at 06:00 KST.
- Hong Kong/Beijing time: weekly reset is Thursday 05:00 (UTC+8).
- Scheduled updates and maintenance are commonly held on Thursday, but their exact times are announcement-specific and are not the Weekly Reset itself.
- A normal scheduled maintenance notice commonly grants 300 Free Lunacy through the mailbox. Do not treat this as guaranteed weekly income: a week can have no maintenance, and extensions, bugs, or special notices can change the amount and eligibility.
- Model ordinary maintenance compensation only when the user opts in or supplies the announced number/amount. Keep exceptional bug compensation separate.

Primary reset reference: https://faq.limbuscompany.site/  
Mirror weekly-charge reference: https://limbuscompany.wiki.gg/wiki/Mirror_Dungeons  
Representative scheduled-maintenance notice: https://dotgg.gg/limbus-company/march-23th-kst-scheduled-update-notice/

## Enkephalin

- Natural regeneration: 1 Enkephalin per 6 minutes = 10/hour = 240/day if regeneration never caps.
- Module conversion: 20 Enkephalin = 1 Enkephalin Module. Conversion is irreversible.
- Enkephalin Box: restores 60 Enkephalin.
- Lunacy refill: daily refill number `n` costs `26 × n` Lunacy, for `n = 1..10`.
- Each Lunacy refill restores Enkephalin equal to the account's current Enkephalin cap and may exceed the cap.
- Daily refill costs: 26, 52, 78, 104, 130, 156, 182, 208, 234, 260.

Primary reference: https://limbuscompany.wiki.gg/wiki/Enkephalin  
Lunacy reference: https://limbuscompany.wiki.gg/wiki/Lunacy

## Mirror Dungeon normal rewards

- Entering is free; claiming a full Normal clear costs 5 Modules.
- A full clear without a Weekly Bonus grants 30 Limbus Pass XP and 100 Manager XP.
- A full Normal clear using one Weekly Bonus grants 45 Pass XP, 250 Free Lunacy, and 100 Manager XP.
- Three Weekly Bonus charges refresh each week.
- A Floor 5 clear is required for the full Weekly Bonus Lunacy and Pass XP.
- The calculator models Normal full clears. Do not substitute Hard rewards without updating the model.

References:

- https://limbuscompany.wiki.gg/wiki/Mirror_Dungeons
- https://limbuscompany.wiki.gg/wiki/Mirror_of_Names_and_Spiders
- https://faq.limbuscompany.site/

## Mirror Dungeon Hard weekly rewards

For a full five-floor Hard clear with all Floors set to Hard:

- Each Weekly Bonus charge costs 6 Modules when claimed in Hard.
- Claiming all three charges in one Hard run costs 18 Modules and grants 750 Free Lunacy, 225 Pass XP, and 360 Manager XP.
- Claiming one charge in each of three Hard runs costs 18 Modules total and grants 750 Free Lunacy plus `75 + 80 + 95 = 250` Pass XP.
- Three separate single-charge claims therefore grant 25 more Pass XP than one triple-charge claim, but require two additional Hard runs.
- A Hard run without a Weekly Bonus grants the same 30 Pass XP and uses the same 5-Module reward cost as Normal; use Normal in the optimizer for such repeat farming.
- Do not count the same Weekly Bonus charges again as Normal bonus claims.

Other supported splits, documented for reference but not optimized in this version:

- `2 + 1`: 230 Pass XP total.
- `1 + 2`: 235 Pass XP total.

Reference: https://limbuscompany.wiki.gg/wiki/Mirror_of_Names_and_Spiders

## Limbus Pass and crates

- Each Pass level requires 10 Pass XP.
- Season 7's planned reward track ends at level 120.
- After the planned reward track, each completed EX level grants 1 Nominable Egoshard Crate on the free track.
- The paid Limbus Pass adds 2 crates per EX level, for 3 total crates per completed EX level.
- Pre-120 levels have fixed track rewards and must not be treated as recurring crate levels.
- The complete Season 7 level 1-120 table is stored in `season-7-pass-rewards.json`; use `season-7-pass-rewards.md` for manual inspection.

References:

- https://limbuscompany.wiki.gg/wiki/Limbus_Pass
- https://limbuscompany.wiki.gg/wiki/Season_7
- https://limbuscompany.wiki.gg/wiki/Egoshard

## Egoshards and dispensing

- A Nominable Egoshard Crate gives 1–3 shards for a chosen Sinner.
- Expected value convention: 2 shards per crate. This is an expectation, not a guarantee.
- A 3-star Identity costs 400 matching Egoshards.
- A 2-star Identity costs 150 matching Egoshards.
- An E.G.O costs 400 matching Egoshards.
- At a season change, half of seasonal shards and crates carry forward and the other half converts to Thread or Thread Crates, with the documented rounding behavior. Flag plans crossing a season boundary.

References:

- https://limbuscompany.wiki.gg/wiki/Egoshard
- https://limbuscompany.wiki.gg/wiki/Dispenser
- https://limbuscompany.wiki.gg/wiki/Seasons

## Lunacy opportunity cost

- Standard single extraction: 130 Lunacy.
- Standard decaextraction: 1300 Lunacy.
- Daily paid single extraction: 13 Paid Lunacy; do not value Free Lunacy as Paid Lunacy.
- Weekly Normal Mirror Dungeon bonuses can provide up to 750 Free Lunacy across three claims.
- Monthly Lunacy Supply is optional paid context: 650 Paid Lunacy immediately plus 65 Free Lunacy daily for 30 days. Do not assume ownership unless specified.
- Monthly Lunacy Batch gives 130 Paid Lunacy immediately plus 39 Free Lunacy daily for 30 login days.
- See `lunacy-and-monthly-packs.md` and `lunacy-and-monthly-packs.json` for currency restrictions, combined totals, login rules, and duration extensions.

References:

- https://limbuscompany.wiki.gg/wiki/Lunacy
- https://limbuscompany.huijiwiki.com/wiki/%E5%85%85%E5%80%BC%E7%B3%BB%E7%BB%9F

## Derived conversions

After Pass level 120, for a full Normal clear without Weekly Bonus:

- 5 Modules → 30 Pass XP → 3 EX levels.
- Free track: 3 crates, expected 6 shards.
- Paid pass: 9 crates, expected 18 shards.

With one Normal Weekly Bonus:

- 5 Modules → 45 Pass XP → 4.5 levels on average.
- Free track: 4.5 crates as a long-run average.
- Paid pass: 13.5 crates as a long-run average.

Actual crates are awarded only when a whole level completes; preserve partial Pass XP between calculations.

After Pass level 120, the weekly Hard choices convert as follows:

- One triple-charge Hard run: 18 Modules -> 225 XP -> 22.5 EX levels on average -> 22.5 free-track crates or 67.5 paid-pass crates on average.
- Three separate single-charge Hard runs: 18 Modules -> 250 XP -> 25 EX levels -> 25 free-track crates or 75 paid-pass crates.
- Separate claims gain 2.5 additional EX levels: 2.5 more free-track crates or 7.5 more paid-pass crates on average, at the cost of two extra Hard runs.
