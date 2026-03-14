---
title: Anemia / Centralization Critique
impact: HIGH
tags: [domain, validation, ai_pass]
order: 110
type: ai_pass
scanner: null
---

## Anemia / Centralization Critique

Explicitly attack the candidate model before accepting it. This phase is mandatory.

**Look for:**
- Centralized handlers, resolvers, or managers
- Anemic entities with no decisions
- Objects that are just data bags
- Config-holder pseudo-objects
- Orphan concepts (referenced but not modeled)
- State with no owner
- Rules with no owner
- Fake inheritance (shared fields, no shared semantics)
- Type, mode, or effect switches that should be polymorphism
- Orchestration making domain decisions
- Relationships with no behavioral significance

**AI must propose minimal corrections** for each issue found.

**DO NOT** truncate. Full Model Assessment requires an explicit anemia critique table covering all issue types (centralized handlers, anemic entities, data bags, orphan concepts, state with no owner, rules with no owner, fake inheritance, type switches, orchestration making domain decisions). Persist the full assessment in run-N-ooad.md. A one-line note is insufficient.
