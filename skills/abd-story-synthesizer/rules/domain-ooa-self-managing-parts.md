---
title: State Model — Parts Manage Their Own State
impact: HIGH
tags: [discovery, domain]
---

## Parts Manage Their Own State

**DO** let each concept manage its own properties through its own invariants. A container holds references to its parts (composition/aggregation) but does not orchestrate their configuration. Each part knows its own rules.

- Example (right): Character has `Dictionary abilities` (composition). Ability has `Number rank` with invariant `cost = rank × 2`. PowerLevel has `validate_pair(a, b) → Boolean`. Each concept owns its rules — Character just holds references.

**DO NOT** put `configure_X()`, `set_X()`, or orchestration methods on the container that delegate to owned objects. If Ability knows how to compute its cost from its rank, that's Ability's concern.

- Example (wrong): Character has `configure_ability(name, rank) → Ability`, `configure_defense(name, ranks) → Defense`, `validate_power_level() → Boolean`. Character is orchestrating what each part should do instead of letting parts manage themselves.
