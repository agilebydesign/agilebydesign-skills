---
title: Domain scaffold uses real concepts
impact: HIGH
tags: [discovery, domain]
---

## Domain scaffold uses real concepts

The domain model first cut (`domain-model.md`) must contain real domain concepts with properties, operations, collaborating concepts, and module groupings. It is not a summary or restatement of the variation analysis — it is the actual domain model at version 1.

**DO** write each concept with typed properties, operations with parameters and return types, collaborating concepts, and module assignment. Use `Dictionary<K,V>` for named collections accessed by key; `List<T>` only when order matters.
- Example (right):
  ```
  Character
  - String name
  - Dictionary<String, AbilityScore> abilities (composition, keyed by type)
  - Dictionary<String, Power> powers (aggregation, keyed by name)
  - calculateTotalCost() → Number
        AbilityScore, Power
  - validatePowerLevel() → List<Violation>
        PowerLevel, Defense
  ```

**DO NOT** produce a domain section that is just bullet points restating analysis findings, listing concept names without properties, or describing relationships in prose without defining the concepts.
- Example (wrong):
  ```
  Character Module:
  - Character has AbilityScores, Skills, Advantages, Powers, Equipment
  - AbilityScore — 8 types, rank-based
  - Power — has effects with extras/flaws
  ```
  This is analysis, not a domain model. It names concepts but doesn't define them.
