---
title: Interactions inheritance — actors
impact: HIGH
tags: epic, story, step
---

## Actors inheritance

**DO** use [User] or [System] at every initiation/response so the actor is visible without looking up. Use Title Case; no dot notation (e.g. `Initiating-Actor`, not `initiation.actor`). Stories inherit Initiating-Actor and Responding-Actor from Epic. Steps inherit from Story or higher; exception: when a step is system-initiated (e.g. "When **System** receives payment type selection"), that step may override Initiating-Actor. See `core.md`.
- Example (right): Epic "Make Checks": Initiating-Actor: User, Responding-Actor: System. Story: Initiating-Actor: [User], Responding-Actor: [System]. Step: Initiating-Actor: [User] or Initiating-Actor: User (when override).

**DO NOT** omit actor at every initiation/response. Do not use lowercase or dot notation for field names.
- Example (wrong): Step has Initiation without Initiating-Actor; reader must look up. Right: Every Initiation and Response shows actor explicitly.
