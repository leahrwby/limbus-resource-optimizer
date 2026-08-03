# Optimization model

## Objective

Maximize recurring Nominable Egoshard Crates earned from full Normal and weekly Hard Mirror Dungeon reward claims within the supplied horizon and constraints. Use expected shards only as a secondary display value.

## Resource flow

Before allocating rewards, derive all Weekly Bonus periods intersecting the planning window from Thursday 06:00 KST. The current period contributes `3 - charges_used_this_week`; each reset inside the window contributes three new charges. Unless overridden, assign these charges to Hard first when Hard is unlocked.

1. Add current Enkephalin, captured natural regeneration, Enkephalin Boxes selected for use, and Enkephalin obtained from Lunacy refills.
2. Convert available Enkephalin to Modules at 20:1, retaining the remainder.
3. Reserve Modules for Luxcavation or other user-specified activities.
4. Reserve 18 Modules per selected Hard week.
5. For `triple`, award 225 Pass XP and 750 Lunacy for one Hard run per week.
6. For `separate`, award 250 Pass XP and 750 Lunacy for three Hard runs per week.
7. Spend 5 remaining Modules per Normal reward claim. Award 30 Pass XP and add 15 XP plus 250 Lunacy to explicitly supplied Normal Weekly Bonus claims.
8. Apply Pass XP to the distance remaining before level 120. Convert only XP beyond that point into recurring EX levels.
9. Award 1 crate per EX level on free pass or 3 total on paid pass.

## Lunacy accounting

1. Track Free Lunacy and Paid Lunacy separately.
2. Add Mirror Dungeon rewards, ordinary income, and monthly-card daily claims to Free Lunacy.
3. Add monthly-card upfront rewards and explicitly paid income to Paid Lunacy.
4. Add maintenance compensation only when explicitly requested. Use 300 Free Lunacy per ordinary scheduled maintenance as a forecast default, but allow an announced amount to override it.
5. Pay Enkephalin refill costs from Free Lunacy first, then Paid Lunacy.
6. Enforce both the combined Lunacy reserve and the Paid Lunacy reserve.
7. Do not count Free Lunacy toward the Pass, daily paid extraction, Announcers, or other paid-only purchases.

Do not overlap Hard-consumed Weekly Bonus charges with `--weekly-bonus-claims`. That argument represents Normal bonus claims remaining outside the Hard weeks.

## Refill selection

The nth refill in a day costs `26n`, so the cheapest allocation for a fixed number of refills spreads them across days. For `R` refills over `D` days:

- `q = floor(R / D)`
- `r = R mod D`
- perform `q + 1` refills on `r` days and `q` on the other days;
- total cost is `D × 26q(q+1)/2 + r × 26(q+1)`.

Enumerate `R = 0..10D` and the requested Hard strategy. With `--hard-weekly-strategy auto`, compare triple and separate claims. Reject plans that violate Module, Lunacy reserve, or total-run limits, and select the feasible plan with the most crates. Break ties by expected shards, then lower Lunacy spend, fewer runs, and fewer refills.

## Important limitations

- The model treats resources and Weekly Bonus Lunacy as available within the horizon; it does not simulate the exact day on which each reward arrives.
- Natural regeneration utilization must be reduced if the player often reaches the Enkephalin cap.
- The model spends all selected Enkephalin Boxes. Set the count to zero to preserve them.
- The model does not value event shops, Thread, Identity EXP, Manager level-ups, time enjoyment, or gacha exclusivity.
- A plan crossing a season boundary requires manual adjustment for shard/crate conversion and the new Pass track.
- Maximizing boxes is not identical to maximizing total account value. Present the result as a constrained farming optimum.
