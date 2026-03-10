---
title: State Model — Domain Language
impact: HIGH
tags: discovery, domain
scanner: domain_naming
---

## Use Domain Language from Source

**DO** use domain language from stories and acceptance criteria. Mine vocabulary from source material.

**DO** use standard types (String, Number, Boolean, List, Dictionary, UniqueID, Instant) for Properties; prefer domain concepts over scattering primitives. See domain-ooa-property-types.

**DO** write Operation names in natural English (Calculates total, Validates inventory, Is exhausted when fully redeemed).

**DO NOT** use Hold, Get, Has as defaults — find domain-specific verbs (Is identified by, Defines, Starts valid at, Expires at).

**DO NOT** use Manager, Service, Handler, Factory suffixes for concept names.

**DO NOT** use abbreviations or technical jargon when simple English works.
