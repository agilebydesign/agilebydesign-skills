---
title: Enumerate all step permutations — cover all paths
impact: MEDIUM-HIGH
tags: [exploration, specification, step]
scanner: step_permutations
---

## Enumerate all step permutations — happy path, error path, edge cases

**DO** cover all validation paths, calculation branches, and state transitions explicitly. Include happy path, error path, and edge case steps. Every path through the logic gets a step.
- Example (right — all paths covered):
  - Step: Validate Rank in Range (When **User** enters rank; Then **System** validates rank is in 1–20 range)
  - Step: Reject Invalid Rank (When **User** enters rank outside range; Then **System** displays validation error)
  - Step: Calculate Modifier from Valid Rank (When rank is valid; Then **System** calculates modifier from rank)
- Example (right — calculation branches):
  - Step: Modifier for Average Rank (When rank is 10; Then modifier is 0)
  - Step: Modifier for Maximum Rank (When rank is 20; Then modifier is +5)
  - Step: Modifier for Minimum Rank (When rank is 1; Then modifier is -5)

**DO NOT** skip validation paths, assume happy path only, or omit edge cases.
- Example (wrong): Only "When **User** enters rank; Then **System** saves" — missing validation error step, boundary step.
- Example (wrong): Only success steps without error handling — what happens when validation fails?
- Example (wrong): Valid and invalid covered but no boundary conditions — what happens at limits?
