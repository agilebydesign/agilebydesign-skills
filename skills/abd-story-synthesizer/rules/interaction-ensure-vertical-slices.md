---
title: Ensure vertical slices
impact: MEDIUM
tags: [discovery, interaction_tree, epic, story]
---

## Ensure vertical slices

Epics and stories should support vertical slices when increments are in scope — end-to-end flows across multiple epics/features, NOT horizontal layers.

**DO** design so that epics can be sliced vertically for end-to-end flows.
- Example (right): Increment 1 includes partial features from multiple epics (Order Entry, Payment, Storage, Display) to create complete flow from order entry through payment to confirmation.

**DO NOT** complete all features in one epic before moving to the next.
- Example (wrong): Increment 1: Complete Epic A (all features done); Increment 2: Complete Epic B (all features done) — creates horizontal layers that can't be tested end-to-end until final increment.
