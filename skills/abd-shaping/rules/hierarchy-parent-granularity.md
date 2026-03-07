---
title: Hierarchy and parent granularity
impact: HIGH
tags: hierarchy, granularity, tree
---

## Hierarchy and parent granularity

**DO** keep parent nodes at appropriate granularity for their level.
- Example: Epic "Build a Character" → Response "System creates valid Character for Campaign".

**DO NOT** leak child-level detail into parent nodes.
- Example: Epic lists "Cart line-item quantity = 2" (that belongs on Story).
