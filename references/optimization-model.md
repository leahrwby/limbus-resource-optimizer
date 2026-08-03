# Optimization model

## Objective

Maximize recurring Nominable Egoshard Crates earned from full Normal Mirror Dungeon reward claims within the supplied horizon and constraints. Use expected shards only as a secondary display value.

## Resource flow

1. Add current Enkephalin, captured natural regeneration, Enkephalin Boxes selected for use, and Enkephalin obtained from Lunacy refills.
2. Convert available Enkephalin to Modules at 20:1, retaining the remainder.
3. Reserve Modules for Luxcavation or other user-specified activities.
4. Spend 5 remaining Modules per Normal Mirror Dungeon reward claim.
5. Award 30 Pass XP per full run and add 15 XP plus 250 Free Lunacy to eligible Weekly Bonus claims.
6. Apply Pass XP to the distance remaining before level 120. Convert only XP beyond that point into recurring EX levels.
7. Award 1 crate per EX level on free pass or 3 total on paid pass.

## Refill selection

The nth refill in a day costs `26n`, so the cheapest allocation for a fixed number of refills spreads them across days. For `R` refills over `D` days:

- `q = floor(R / D)`
- `r = R mod D`
- perform `q + 1` refills on `r` days and `q` on the other days;
- total cost is `D × 26q(q+1)/2 + r × 26(q+1)`.

Enumerate `R = 0..10D`, reject plans that violate Lunacy reserve or run limits, and select the feasible plan with the most crates. Break ties by expected shards, then lower Lunacy spend, fewer runs, and fewer refills.

## Important limitations

- The model treats resources and Weekly Bonus Lunacy as available within the horizon; it does not simulate the exact day on which each reward arrives.
- Natural regeneration utilization must be reduced if the player often reaches the Enkephalin cap.
- The model spends all selected Enkephalin Boxes. Set the count to zero to preserve them.
- The model does not value event shops, Thread, Identity EXP, Manager level-ups, time enjoyment, or gacha exclusivity.
- A plan crossing a season boundary requires manual adjustment for shard/crate conversion and the new Pass track.
- Maximizing boxes is not identical to maximizing total account value. Present the result as a constrained farming optimum.

