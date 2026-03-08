---
title: Structured concepts — include in every slice run
impact: HIGH
tags: state, structure, workflow
---

## Structured concepts — include in every slice run

**DO** complete the full workflow for each slice: (1) interactions, then (2) derive concepts from interactions, (3) model concepts in OOAD style (State Model), (4) add inline Concepts blocks under Epics with compact definitions (properties, operations). When editing interactions, also update or add concepts as needed.
- Example: After revising an interaction that touches Check and CheckResult, add or update those concepts in the State Model and add a Concepts block under the Epic with Check, CheckResult, DifficultyClass, Modifier and their key properties/operations.

**DO NOT** edit only the Interaction Tree and skip the State Model or inline Concepts. Do not assume concepts are "done" — interaction changes often imply concept changes.
- Example (wrong): Revising an interaction but not updating the related concept or adding a Concepts block. Right: Update both interaction and concepts; add inline Concepts under the Epic.
