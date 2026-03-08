---
title: Synchronize State Model with Interaction
impact: HIGH
tags: epic, story, domain_concept
---

## State Model With Intertactions — Synchronize the state model with interactions ina slice before comlpeting a run

**DO** when updating interactions during a run: (1) interactions, then (2) derive concepts from interactions, (3) model concepts in OOAD style (State Model), (4) add inline Concepts blocks under Epics with compact definitions (properties, operations). When editing interactions, also update or add concepts as needed.
- Example (right): Epic "Make Checks" has inline Concepts: `Check: targetNumber, roll(dice): Result`; `DifficultyClass: value`; `Modifier: source, value`. State Model has full definitions. After revising an interaction that touches CheckResult, you add CheckResult to both.

**DO NOT** edit only the Interaction Tree and skip the State Model or inline Concepts. Do not assume concepts are "done" — interaction changes often imply concept changes.
- Example (wrong): You add interaction "Resolve opposed check" but the Epic has no Concepts block and the State Model has no OpposedCheck. Right: Add OpposedCheck to State Model, add Concepts block under Epic with OpposedCheck, AttackerRoll, DefenderRoll.
