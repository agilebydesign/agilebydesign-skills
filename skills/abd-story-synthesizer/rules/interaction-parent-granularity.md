---
title: Hierarchy and parent granularity
impact: HIGH
tags: [discovery, interaction_tree, epic, story]
scanner: parent_granularity
---

## Hierarchy and parent granularity

**DO** keep parent nodes at appropriate granularity for their level.
- Example (right): Epic "Build a Character" → Response "System creates valid Character for Campaign".

**DO NOT** leak child-level detail into parent nodes.
- Example (wrong): Epic "Shop for Books" lists Pre-Condition "Cart line-item quantity = 2". Right: That belongs on Story "Update cart quantity".
