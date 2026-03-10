---
title: Interactions inheritance — Triggering-State
impact: MEDIUM-HIGH
tags: [discovery, interaction_tree, story]
---

## Triggering-State inheritance

**DO** place Triggering-State at the level where it applies to all descendants. Epic holds trigger state for rules that apply to all children (e.g. user access to payment types by country). Epics (including epic children of epics) group; they do not add trigger/response state. Stories inherit Pre-Condition, Triggering-Actor, and Responding-Actor from Epic. Triggering-State qualifies the interaction (e.g. selecting an option of a certain type). See `core.md`.
- Example (right): Epic "Make Checks": Triggering-State: User has access to Check, Modifier, DifficultyClass. Story: inherits; adds only when story-specific.

**DO NOT** put Triggering-State at a level if it applies only to specific scenarios or stories — place it on those nodes. Do not put concepts on individual stories when they apply to multiple — promote to parent.
- Example (wrong): Epic "Make Checks" has no Triggering-State but each story has different access rules — promote shared rules to Epic. Right: Epic has rules that apply to all children.
