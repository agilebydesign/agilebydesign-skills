---
title: Interactions inheritance — Initiating-State
impact: MEDIUM-HIGH
tags: epic, story
---

## Initiating-State inheritance

**DO** place Initiating-State at the level where it applies to all descendants. Epic holds initiation state for rules that apply to all children (e.g. user access to payment types by country). Epics (including epic children of epics) group; they do not add initiation/response state. Stories inherit Pre-Condition, Initiating-Actor, and Responding-Actor from Epic. Initiating-State qualifies the interaction (e.g. selecting an option of a certain type). See `core.md`.
- Example (right): Epic "Make Checks": Initiating-State: User has access to Check, Modifier, DifficultyClass. Story: inherits; adds only when story-specific.

**DO NOT** put Initiating-State at a level if it applies only to specific scenarios or stories — place it on those nodes. Do not put concepts on individual stories when they apply to multiple — promote to parent.
- Example (wrong): Epic "Make Checks" has no Initiating-State but each story has different access rules — promote shared rules to Epic. Right: Epic has rules that apply to all children.
