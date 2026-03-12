---
title: Interactions inheritance — Resulting-State
impact: HIGH
tags: [discovery, story_map, story]
scanner: inheritance_resulting_state
---

## Resulting-State inheritance

**DO** apply the same inheritance rules to Resulting-State as Pre-Condition — shared on parent, child-specific on child. At Epic/Sub-epic level, express as a single, high-level outcome; use outcome language only (what is true afterward). Resulting-State is the state that results from the interaction (see `core.md`).
- Example (right): Parent: "Cart populated"; Child: "Shopping Cart: empty → has-items". Epic: "Character is built and valid within campaign PL and PP limits"; "validation result recorded".

**DO NOT** duplicate Resulting-State across levels or use action language in Resulting-State. Do not use intermediate steps, granular outcomes, or behavior/action language in Epic/Sub-epic Resulting-State.
- Example (wrong): "System validates" or "System records"; Epic "Build a Character" → "Character has PP budget allocated"; "Character is fully built; Character has all traits; Character validated against PL". Right: "validation result recorded"; Epic "Character is built and valid within campaign PL and PP limits".
