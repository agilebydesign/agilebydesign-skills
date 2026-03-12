---
title: State Model — Decompose Mechanically Distinct Variants
impact: HIGH
tags: [discovery, domain]
---

## Decompose Variants by Mechanical Distinction

**DO** when subtypes have fundamentally different properties, operations, or resolution mechanics, decompose into an inheritance hierarchy with invariant examples per subtype. Conversely, when operations differ only by a type discriminator with the same logic, consolidate into a single parameterized operation with a type property.

- Example (right — decompose): Maneuver subtypes have different mechanics — CombatManeuver uses opposed checks and applies Conditions, TradeManeuver adjusts character stats, DefensiveManeuver consumes standard action for defense bonus. Each gets its own class with distinct properties and operations. Variant rules captured as invariant examples (Grab, Trip, Disarm on CombatManeuver; Power Attack, All-out on TradeManeuver).
- Example (right — consolidate): Two operations `from_effect_rank(rank)` and `from_damage_rank(rank)` that differ only in base value → one operation `from_rank(rank, effect_type)` with type property and invariant: `base = 15 when damage, 10 otherwise`.

**DO NOT** collapse mechanically distinct behaviors into a flat class with a type enum when subtypes need different properties and operations. Don't create duplicate operations that differ only by a hardcoded value.

- Example (wrong): `Maneuver` with `ManeuverType {grab, trip, disarm, power_attack, defend}` — five mechanically different things in one class.
