---
title: Sequential order
impact: HIGH
tags: hierarchy, order, flow
---

## Sequential order

**DO** order the tree sequentially — required state creators before consumers; follow actual flow, not topic grouping.
- Example: Create Character → Set Scenario → Start Turn → Perform Action (not: Resolve Checks → Run Combat).

**DO NOT** organize by topic when it violates sequence.
- Example: "All checks together" or "Run Combat" before "Create Character" or "Set Scenario".
