---
title: Interactions inheritance — Examples
impact: MEDIUM-HIGH
tags: [discovery, specification, interaction_tree, story, step, scenario, example]
scanner: inheritance_examples
---

## Examples inheritance

**DO** live on the interaction. Use [inherited] when tables come from parent; list the qualitative names (e.g. `[Logged In User, Active User Session, User Payment Type Access]`). Include step-specific or story-specific examples unbracketed. Name by state or condition — "Selected Country", "Selected PaymentType", "Approved Payment" — not generic labels like "Payment" or "Country". See `core.md`.
- Example (right): Epic has Examples: Logged In User, Active User Session. Story: Examples: [Logged In User, Active User Session]. Step: Examples: [Logged In User], Selected PaymentType (step-specific).

**DO NOT** repeat parent tables on children. Do not use generic labels like "Payment" or "Country". When inherited, list those names: `examples: [Logged In User, Active User Session, User Payment Type Access]`.
- Example (wrong): Story "Search by title" has full Examples table when Epic already has it. Right: Story: Examples: [inherited] or list names.
