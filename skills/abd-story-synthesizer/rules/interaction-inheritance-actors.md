---
title: Interactions inheritance — actors
impact: HIGH
tags: [discovery, exploration, story_map, story, step]
scanner: inheritance_actors
---

## Actors inheritance

**DO** use [User] or [System] at every trigger/response so the actor is visible without looking up. Use Title Case; no dot notation (e.g. `Triggering-Actor`, not `trigger.actor`). Stories inherit Triggering-Actor and Responding-Actor from Epic. Steps inherit from Story or higher; exception: when a step is system-triggered (e.g. "When **System** receives payment type selection"), that step may override Triggering-Actor. See `core.md`.
- Example (right): Epic "Make Checks": Triggering-Actor: User, Responding-Actor: System. Story: Triggering-Actor: [User], Responding-Actor: [System]. Step: Triggering-Actor: [User] or Triggering-Actor: User (when override).

**DO NOT** omit actor at every trigger/response. Do not use lowercase or dot notation for field names.
- Example (wrong): Step has Trigger without Triggering-Actor; reader must look up. Right: Every Trigger and Response shows actor explicitly.
