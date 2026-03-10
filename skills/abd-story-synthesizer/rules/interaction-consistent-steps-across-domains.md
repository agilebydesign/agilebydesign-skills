---
title: Keep steps consistent across connected domains
impact: MEDIUM
tags: [exploration, specification, step]
scanner: consistent_steps
---

## Consistent steps across connected domains — parallel structure, scoped to one domain

**DO** at small scale, steps covering multiple domain objects together is acceptable. As domain objects develop distinct behavior, scope each step to one domain and keep structure consistent across connected domains.
- Example (right — small scale, together is fine):
  - Step: Submit Payment (When **User** submits payment; Then **System** validates and routes) — covering wire and ACH together when each has simple, similar validation.
- Example (right — scaled, scoped to one domain with parallel structure):
  - Step: Submit Wire Payment (When **User** submits wire payment; Then **System** validates intermediary bank and routes to wire rail)
  - Step: Submit ACH Payment (When **User** submits ACH payment; Then **System** validates routing number and routes to ACH rail)
  - Same pattern, same depth, domain-specific details as the only variation.

**DO** treat steps that cross multiple domain behaviors as the signal to split the story. If a step mentions both wire validation AND ACH routing, the story needs splitting.

**DO NOT** mix domain object behaviors in one step when each has distinct logic. Don't write inconsistent steps across connected domains — if wire has 5 detailed steps and ACH has 1 vague step, the depth should be parallel.
- Example (wrong): "When **User** submits payment; Then **System** validates wire rules and ACH rules and check rules" — too broad when each has distinct validation.
- Example (wrong): Wire story has 5 steps covering every validation; ACH story has 1 step. Keep depth and structure parallel.
