---
title: Class Diagram — Import Cross-Model Base Classes
impact: HIGH
tags: [class_diagram, domain]
---

## Import Cross-Model Base Classes

**DO** when a page's concepts extend or use concepts from other foundational models, import those base classes at the top of the page to show the full ancestry chain. Include the grandparent when it establishes context for how the parent was created.

- Example (right): Attack and Damage page imports both Rollable [from: Resolution System] and Check [from: Resolution System] with a "creates" dependency edge between them. Reader sees the full chain: Rollable → Check → AttackCheck/DamageResistance.

**DO NOT** show only the immediate parent import while omitting the grandparent that gives context. The reader needs to understand where the parent came from.

- Example (wrong): Attack and Damage page imports Check but not Rollable — reader can't see that Checks originate from Rollable.perform_check().
