---
title: State Model — Composition and Aggregation
impact: HIGH
tags: discovery, domain
scanner: domain_composition
---

## Composition vs Aggregation

**DO** when a concept "has" another concept, distinguish:

| Relationship | Meaning | Lifecycle | Example |
|--------------|---------|-----------|---------|
| **Composition** | Strong has-a; part cannot exist without whole | Shared — part dies with whole | Order and LineItem; Book and Page |
| **Aggregation** | Weak has-a; whole has no meaning without multiple instances of the same part (e.g. crowd, flock, mob) | Independent | Crowd (people); Flock (birds); Cart and Product |

**DO** prefer composition and aggregation over inheritance for concept relationships. Inheritance couples types tightly; composition/aggregation keep flexibility.

## Sequence Diagrams

**DO NOT** generate sequence diagrams. Object flow and walkthrough strategies (object-to-object interactions) are in scope; formal sequence diagrams are not.
