---
title: Required state
impact: HIGH
tags: state, preconditions, inheritance
---

## Required state

**DO** declare shared required state on the parent only; list only new or unique required state on children; make required state comprehensive — ask "Would this work if [X] didn't exist?". Assign to ONE level only — if unique to a story, keep on story; if on more than one story, promote to parent. When the child uses only parent concepts/state, leave Required State and State Concepts blank (inheritance assumed).
- Example: Parent: "Books exist in catalog"; Child: "Books match search criteria" (specializes). "Can you search if no books exist?" → required. Epic Make Checks has Check, Modifier, DifficultyClass; all children have State Concepts left blank. PowerPointBudget on 3 of 4 stories → promote to Sub-epic; remove from the 3.

**DO NOT** duplicate shared state on children or omit required preconditions. Do not repeat parent concepts on children. Do not put concepts on individual stories when they apply to multiple — that causes you to omit them on some.
- Example: Child repeats "Books exist" when parent already has it. Epic Make Checks had State Concepts on each story; Story "Make Secret Check" had State Concepts left blank but the model omitted that Check, Modifier, DifficultyClass all apply — wrong: putting concepts on individual stories caused them to be forgotten on Secret Check.
