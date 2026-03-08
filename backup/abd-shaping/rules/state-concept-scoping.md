---
title: Concept scoping
impact: HIGH
tags: state, concepts, structure
---

## Concept scoping

**DO** scope concepts to the Epic or Story that owns them — declare at the lowest common ancestor of all interactions that use the concept. Assign to ONE level only. When the child uses only parent concepts, leave State Concepts blank (inheritance assumed).
- Example: Shopping Cart under Shop for Books; Book Catalog under Browse Books; Account at root if used across both. Epic Make Checks has Check, DifficultyClass, Modifier; each story has State Concepts left blank.

**DO NOT** declare concepts at the wrong level or list every concept at the root. Do not repeat parent concepts on children.
- Example: Shopping Cart at root when only Shop for Books uses it. Epic Make Checks had State Concepts: Check, DifficultyClass, Modifier on Story "Make Standard Check" and "Make Opposed Check" — wrong: those concepts were on the Epic, so repeating them on stories violates "assign to ONE level only".
