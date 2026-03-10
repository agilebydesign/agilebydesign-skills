---
title: State Model — Bidirectional Relationships
impact: MEDIUM
tags: discovery, domain
scanner: domain_bidirectional
---

## When A References B, B Should Reference A

**DO** when Concept A has a Property or Operation that references B (non-primitive), B should have a corresponding reference to A — same relationship, both perspectives.

**DO** use relationship names that describe the relationship from each concept's viewpoint (Order contains LineItem; LineItem belongs to Order).

**DO NOT** require bidirectional mapping for primitives (String, Number, Boolean, etc.).

**DO NOT** use mismatched collaborators — the bidirectional pair must describe the SAME relationship from both sides.
