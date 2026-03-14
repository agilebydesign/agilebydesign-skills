---
title: Base and Inheritance Check
impact: HIGH
tags: [domain, validation, ai_pass]
order: 120
type: ai_pass
scanner: null
---

## Base and Inheritance Check

### Concepts that share structure — should they extend a common base?

**Check each cluster** for shared protocol and shared invariants. When concepts share:
- (a) cost or acquisition mechanics
- (b) participation in validation (e.g. PL caps)
- (c) lifecycle (bought/allocated during build)
- (d) membership in a parent's collection

…then a common base may be appropriate. Shared protocol: `cost()`, participation in validation, acquisition via budget.

**Look for:**
- Missing base — concepts that share acquisition, cost, and validation role but lack a common supertype
- Over-inheritance — base with no real semantics; subtypes share only fields, not behavior

**Verdict:** Introduce a base when the *role* is the same and variation is in implementation. Avoid over-bias against inheritance when concepts clearly share protocol and invariants.

**DO NOT** defer to future refinement. When concepts share protocol (cost, acquisition, validation role, lifecycle, membership in a parent's collection), introduce the shared base in the current slice. Do not say "consider base in future refinement" when the protocol is shared now.

**AI must propose minimal corrections** (e.g. add CharacterTrait as base for AbilityRank, Defense, Skill, Advantage).
