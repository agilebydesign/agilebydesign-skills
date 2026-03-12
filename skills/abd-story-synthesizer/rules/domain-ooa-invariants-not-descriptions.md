---
title: State Model — Invariants for Rules, Derived Properties Not Getters
impact: HIGH
tags: [discovery, domain]
scanner: domain_invariants
---

## Rules and Formulas in Invariants, Not Descriptions

**DO** express domain rules, formulas, value mappings, and constraints as explicit invariants. Properties declare type and name only. Operations declare signature only. Model computed/derived values as properties with invariants, not as getter operations.

- Example (right): Property: `Number cost`. Invariant: `cost = rank × 2`. Property: `Number defense_class`. Invariant: `defense_class = 10 + total_bonus`. Property: `Boolean is_natural_20`. Invariant: `is_natural_20 when natural_roll is 20`.

**DO NOT** embed formulas or hardcoded values in property descriptions or operation signatures. Do not model simple derived values as getter operations.

- Example (wrong): `Number value (+2 minor, -2 penalty, +5 major)` — values in description. `Number cost_per_rank (2 power points)` — formula in property. `get_defense_class() → Number` — getter for a derived value. `calculate_cost() → Number (rank × 2)` — formula in operation signature.
