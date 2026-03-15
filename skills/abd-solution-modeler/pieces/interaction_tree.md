# Interaction Tree Format

**Full spec:** `docs/requirements.md` § Interaction Tree Model.

## Hierarchy

Epic → Story → Scenario → Step

| Node | Meaning |
| ----- | ----- |
| Epic | Large domain capability; groups stories |
| Story | Smallest independently valuable behavior; backbone unit |
| Scenario | Step grouping for a condition |
| Step | Atomic interaction |

## Per Interaction

- **Trigger** — Triggering-Actor, Behavior
- **Response** — Responding-Actor, Behavior
- **Pre-Condition** — label only
- **Examples** — tables per concept

## Domain Grounding

Use `**Concept**` in labels. Every concept must exist in Domain Model.

## Inheritance

Parent → child; use `[brackets]` for inherited values.

## Progression by Phase

| Phase | Adds |
| ----- | ---- |
| 2 | Epic skeleton (names only) |
| 5 | Epics, sub-epics, first-cut stories (names only) |
| 6 | Story placement refined; structure only |
| 7 | Concepts linked to stories |
| 8 | Triggering-Actor, Responding-Actor per story |
| 9 | Trigger, Response, Pre-Condition, Steps |
| 10 | Variation paths |
| 11 | Scenarios, Failure-Modes, Constraints |
| 12 | Walkthrough validates (no new content) |
| 13 | Examples (tables per concept) |
