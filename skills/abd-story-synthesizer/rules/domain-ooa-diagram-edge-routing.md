---
title: Class Diagram — Explicit Edge Routing
impact: HIGH
tags: [class_diagram, domain]
---

## Explicit Edge Routing for Multiple Edges

**DO** when a class has multiple edges leaving from or arriving at the same side, specify explicit exit and entry connection points (exitX/exitY/entryX/entryY) so each edge has a distinct visual path. Distribute connection points across the available surface.

- Example (right): CombatManeuver has three outgoing edges — inheritance exits top-center (0.5, 0), "creates" dependency exits left-low (0, 0.7), opposed "creates" exits left-high (0, 0.15). Each edge is visually distinct.
- Example (right): Three child classes inherit from the same parent — each enters the parent's bottom at a different X (0.25, 0.5, 0.75).

**DO NOT** leave multiple edges with default routing from the same source — DrawIO will render them on top of each other, making edges invisible.

- Example (wrong): CombatManeuver has three edges all leaving from default anchor — they stack and become a single thick line. Reader can't distinguish inheritance from dependency.
