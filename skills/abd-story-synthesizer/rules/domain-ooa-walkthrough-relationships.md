---
title: State Model — Derive Relationships from Mechanical Walkthrough
impact: HIGH
tags: [discovery, exploration, domain]
---

## Derive Relationships from Mechanical Walkthrough

**DO** walk through the actual execution flow to determine UML edge types. For each relationship ask: what creates what? What receives what as a parameter? What object's state actually changes?

- **Dependency "creates"** — concept produces another during execution (e.g. `attempt() → Check`)
- **Association** — concept receives another as a parameter and operates on it directly (e.g. `apply(character) → Character`)
- **Composition** — concept owns another as a long-lived part (e.g. Character ◆→ Ability)

Draw the edge to the concept whose state actually changes, not downstream consumers that merely read the already-modified values.

- Example (right): CombatManeuver.attempt() creates AttackCheck (phase 1) and creates opposed Check (phase 2) → two dependency "creates" edges. TradeManeuver.apply(character) modifies character stats → association to Character, no edge to AttackCheck (created later from modified stats).
- Example (right): Rollable.perform_check() creates Check → dependency "creates". Check holds `Rollable source` to navigate back → association Check → Rollable.

**DO NOT** use vague dependency labels ("uses", "modifies", "opposed") that describe intent rather than the mechanical relationship. Don't overuse dependency for everything — distinguish creates-during-execution from operates-on-parameter from holds-as-part.

- Example (wrong): CombatManeuver --"uses"-→ AttackCheck, --"opposed"-→ Check, TradeManeuver --"modifies"-→ AttackCheck. Three dependencies with labels that don't convey whether the concept creates, holds, or merely references the target.
