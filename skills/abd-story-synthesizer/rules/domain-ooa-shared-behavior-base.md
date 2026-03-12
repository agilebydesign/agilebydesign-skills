---
title: State Model — Extract Shared Behavior into Base Concepts
impact: HIGH
tags: [discovery, domain]
---

## Shared Behavior and Structure in Base Concepts

**DO** when multiple concepts share the same behavioral pattern or structural pattern, extract a base concept. Place it in the system that owns the behavior, not the system that owns the data. Separate orthogonal concerns into independent bases.

- Example (right): Multiple concepts can "roll a check" → extract `Rollable` in Resolution System with `modifier` and `perform_check()`. Multiple concepts have "rank, cost, power-level limit" → extract `Trait` with shared properties and invariants. Ability combines both: `Ability : Trait, Rollable`. Advantage has rank but isn't rollable: `Advantage : Trait`.

**DO NOT** duplicate behavioral or structural patterns across concepts without a shared base. Do not conflate orthogonal concerns into a single base (e.g., "has rank" and "can be rolled" are separate concerns).

- Example (wrong): Ability, Defense, and Skill each independently declare `Number modifier` and `perform_check()` with no shared base. Or: everything extends `Rollable` even when some concepts (Advantage, Effect) have ranks but can't be rolled.
