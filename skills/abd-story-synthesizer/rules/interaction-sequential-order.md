---
title: Sequential order
impact: HIGH
tags: [discovery, interaction_tree, epic, story]
---

## Sequential order

**DO** order the tree sequentially — required state creators before consumers; follow actual flow, not topic grouping.
- Example (right): Create Character → Set Scenario → Start Turn → Perform Action.

**DO NOT** organize by topic when it violates sequence.
- Example (wrong): "All checks together" or "Run Combat" before "Create Character" or "Set Scenario". Right: Create Character → Set Scenario → Start Turn → Perform Action.
