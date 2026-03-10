---
title: Supporting actor and Response
impact: MEDIUM-HIGH
tags: [discovery, interaction_tree, epic, story, step]
scanner: actor_response
---

## Supporting actor and Response

**DO** treat Supporting as the system (or subsystem) that responds — use Actor → System exchange; keep Epic-level (and Sub-epic) Response coarse-grained — what is true after the actor triggers at that level.
- Example (right): "System saves campaign PL"; "System persists budget"; Epic "Build a Character" → Response "System creates valid Character for Campaign".

**DO NOT** frame Supporting as a human or use human-to-human exchange; do not use story-level or sub-epic-level detail in Epic-level or Sub-epic Response.
- Example (wrong): "GM sets and communicates"; "Player tells GM"; Epic "Build a Character" → Response "System applies cost formula; deducts PP; validates traits" (that belongs in stories). Right: Epic Response "System creates valid Character for Campaign".
