---
title: Foundation Inclusion in Early Slices
impact: HIGH
tags: [session, slices]
order: 40
type: rule
scanner: null
---

## Foundation Inclusion in Early Slices

**DO** include foundational setup in early slices when the core flow depends on it. Examples: product setup, account creation, user onboarding, configuration before core use. If the solution requires something to exist or be configured before the main flow runs, the first slice must model that.

**DO NOT** defer foundational setup to a later slice when the first slice's flow is under-specified without it.
