---
title: Resulting state
impact: HIGH
tags: state, outcomes, inheritance
---

## Resulting state

**DO** apply the same inheritance rules to Resulting State as Required State — shared on parent, child-specific on child. At Epic/Sub-epic level, express as a single, high-level outcome; use outcome language only (what is true afterward).
- Example: Parent: "Cart populated"; Child: "Shopping Cart: empty → has-items". Epic: "Character is built and valid within campaign PL and PP limits"; "validation result recorded".

**DO NOT** duplicate resulting state across levels or use action language in Resulting State. Do not use intermediate steps, granular outcomes, or behavior/action language in Epic/Sub-epic Resulting State.
- Example: "System validates" or "System records" (use outcome: "validation result recorded"). Epic-level wrong: "Character has PP budget allocated"; "Character is fully built; Character has all traits; Character validated against PL".
