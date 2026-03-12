---
title: Interactions inheritance — domain concepts
impact: HIGH
tags: [discovery, story_map, story, domain]
scanner: inheritance_domain_concepts
---

## Domain concepts inheritance

**DO** scope domain concepts to the Epic or Story that owns them — declare at the lowest common ancestor of all interactions that use the concept. Assign to ONE level only. Stories rarely define domain concepts — they inherit from epic. Reference concepts via `**Concept**` in labels (see `core.md`).
- Example (right): Shopping Cart under Epic "Shop for Books"; Book Catalog under Epic "Browse Books"; Account at root if used across both. Epic "Make Checks" has State Concepts: Check, DifficultyClass, Modifier.

**DO** place concepts at the most specific level where relevant. Local (single sub-epic) vs shared (multiple sub-epics): elevate to parent when shared; keep local when only one sub-epic uses them. Concepts should be complete functional units (Properties + Operations), not fragments.

**DO** use Domain Model format for concept examples — Properties, Operations, Module — not CRC class-responsibility-card format (no "Get X: Type, Collaborator" style). See `pieces/domain.md` Domain Concept and § Output Format.

**DO NOT** declare concepts at the wrong level or list every concept at the root. Do not put concepts on individual stories when they apply to multiple — promote to parent.
- Example (wrong): Shopping Cart at root when only Epic "Shop for Books" uses it. State Concepts Check, DifficultyClass, Modifier on both Story "Make Standard Check" and Story "Make Opposed Check" when Epic "Make Checks" already has them. Right: Epic has concepts.

**DO NOT** use CRC format (responsibilities + collaborators) for Domain Model examples. Use Domain Concept format: Name, Module, Properties, Operations.
