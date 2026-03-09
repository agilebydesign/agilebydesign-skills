---
title: State Model — Atomic Operations
impact: HIGH
tags: discovery, domain
---

## One Operation = One Behavior

**DO** keep Operations atomic: one Operation = one behavior.

**DO** describe behavior (Acquires, Releases, Calculates, Validates), not outcome (Prevents, Issues).

**DO NOT** pack multiple conditions into one Operation (e.g. "Releases on unlock, redemption complete, or timeout" → split into separate Operations).

**DO NOT** use outcome phrasing (Prevents, Issues) when behavior phrasing is clearer (Acquires, Releases).
