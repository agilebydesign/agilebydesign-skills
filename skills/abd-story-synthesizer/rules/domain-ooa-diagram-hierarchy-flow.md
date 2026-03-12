---
title: Class Diagram — Inheritance Flows Top-Down
impact: HIGH
tags: [class_diagram, domain]
---

## Inheritance Flows Top-Down

**DO** position base/imported classes at the top of the diagram page with children extending downward. Inheritance arrows (hollow triangles) point upward from child to parent. The visual hierarchy matches the conceptual hierarchy — readers see the base abstraction first, then specializations below.

- Example (right): Rollable import at top (y=40), Check import below (y=180), AttackCheck and DamageResistance side by side below Check (y=400). Arrows point up from children to parents.

**DO NOT** place base classes at the bottom with children above — this inverts the visual hierarchy and forces readers to scan backwards.

- Example (wrong): AttackCheck at top (y=40), Check import at bottom (y=550). Inheritance arrow points downward — readers see the specialization before the abstraction.
