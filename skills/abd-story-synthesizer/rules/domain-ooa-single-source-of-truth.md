---
title: State Model — Single Source of Truth
impact: HIGH
tags: [discovery, domain]
---

## No Duplicate Primitive and Relationship for Same Value

**DO** when a concept has its own class with behavior (operations, invariants), reference it through a relationship only. The owning class accesses the value through the relationship. One source of truth.

- Example (right): Character has aggregation to PowerLevel. Character gets the level value through its PowerLevel reference. No redundant `Number power_level` property on Character.

**DO NOT** have both a primitive property AND a relationship to a class that holds the same value. Two sources of truth create inconsistency.

- Example (wrong): Character has `Number power_level` property AND an aggregation to PowerLevel class (which has `Number level`). Two places to get the same value — which is authoritative?
