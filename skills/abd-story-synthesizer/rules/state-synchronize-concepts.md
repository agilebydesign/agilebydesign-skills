---
title: Synchronize Domain Model with Interaction
impact: HIGH
tags: [discovery, domain]
---

## Domain Model With Interactions — Synchronize the Domain Model with interactions in a slice before completing a run

**DO** derive Properties and Operations from interactions and stories; do not invent collaborators or relationships not present in source material.

**DO** when updating interactions during a run: (1) interactions, then (2) derive concepts from interactions, (3) model concepts in OOAD style (Domain Model), (4) add inline Concepts blocks under Epics with compact definitions (properties, operations). When editing interactions, also update or add concepts as needed. The Domain Model connects to interactions: concepts participate as callers/receivers; state flows through Pre-Condition, Initiating-State, Resulting-State. See state-ooa-* rules: caller/receiver/state, interaction patterns, property types, composition.
- Example (right): Epic "Make Checks" has inline Concepts: `Check: targetNumber, roll(dice): Result`; `DifficultyClass: value`; `Modifier: source, value`. State Model has full definitions. After revising an interaction that touches CheckResult, you add CheckResult to both.

**DO NOT** edit only the Interaction Tree and skip the Domain Model or inline Concepts. Do not assume concepts are "done" — interaction changes often imply concept changes.
- Example (wrong): You add interaction "Resolve opposed check" but the Epic has no Concepts block and the Domain Model has no OpposedCheck. Right: Add OpposedCheck to Domain Model, add Concepts block under Epic with OpposedCheck, AttackerRoll, DefenderRoll.
