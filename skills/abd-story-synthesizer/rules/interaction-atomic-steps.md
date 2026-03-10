---
title: Write atomic steps — don't repeat base logic
impact: MEDIUM-HIGH
tags: [exploration, specification, step]
scanner: atomic_steps
---

## Atomic steps — state general case once, variations only state what differs

**DO** state the general behavior once in the first step. Additional steps for variations only state what changes from the general case. Edge cases state only the edge behavior.
- Example (right — general case):
  - Step 1: Move Node to New Parent (When **Node** moves to new parent; Then **Node** removes itself from current parent and adds itself to target parent as last child and resequences siblings)
- Example (right — variation only states the difference):
  - Step 2: Move Node at Specified Position (When position is specified; Then **Node** adds itself at specified position instead of last)
- Example (right — edge case only states the edge):
  - Step 3: Position Exceeds Children Count (When position exceeds children count; Then position adjusts to last)

**DO NOT** repeat the same base logic across multiple steps. Don't copy-paste the full trigger/response with minor tweaks.
- Example (wrong — three steps all repeat "removes from parent, adds to target, resequences"):
  - Step 1: When **Node** moves → removes from parent, adds to target as last, resequences
  - Step 2: When **Node** moves with position → removes from parent, adds at position, resequences
  - Step 3: When **Node** moves with invalid position → removes from parent, adjusts position, moves, resequences
- Right: Step 1 has the full logic; Step 2 says "adds at position instead of last"; Step 3 says "position adjusts to last".
