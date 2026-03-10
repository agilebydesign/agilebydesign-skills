---
title: Interactions inheritance — Pre-Condition
impact: HIGH
tags: [discovery, interaction_tree, epic, story]
scanner: inheritance_precondition
---

## Pre-Condition inheritance

**DO** declare shared Pre-Condition on the parent only; list only new or unique Pre-Condition on children; make Pre-Condition comprehensive — ask "Would this work if [X] didn't exist?". Assign to ONE level only — if unique to a story, keep on story; if on more than one story, promote to parent. When the child uses only parent concepts/state, leave Pre-Condition and domain concepts blank (inheritance assumed). See `core.md`.
- Example (right): Epic "Browse Books": Pre-Condition "Books exist in catalog"; Story "Search by title": Pre-Condition "Books match search criteria" (specializes). Epic "Make Checks": State Concepts Check, Modifier, DifficultyClass; Stories have State Concepts blank. PowerPointBudget on 3 of 4 stories → promote to Sub-epic; remove from the 3.

**DO NOT** duplicate shared Pre-Condition on children or omit required preconditions. Do not repeat parent concepts on children. Do not put concepts on individual stories when they apply to multiple — that causes you to omit them on some. Stories rarely define domain concepts — they inherit from epic.
- Example (wrong): Story "Search by title" has Pre-Condition "Books exist in catalog" when Epic already has it. Epic "Make Checks" has State Concepts on each story; Story "Make Secret Check" has State Concepts blank and the model omits Check, Modifier, DifficultyClass — they were forgotten. Right: Epic has concepts; all stories inherit (blank).
