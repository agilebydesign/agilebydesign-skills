---
title: Traverse From Root
impact: HIGH
tags: [domain, validation, ai_pass]
order: 120
type: rule
scanner: null
---

## Traverse From Root

**DO** traverse from root. The source owns creation; the created object receives the source and derives the value internally. Do not pass raw derived values.

**DO NOT** pass raw values when the source object is available.

- Example (wrong): `validation.resolve(source.value)`
- Example (correct): `source.create_validation(dc)` then `validation.resolve()` — validation gets value from source internally.
