---
title: No Generic Resolvers
impact: HIGH
tags: [discovery, ai_passes, domain]
scanner: generic_resolver
---

# No Generic Resolvers

Generic resolver, handler, manager, or processor classes that route all behavior through one point are a sign of missing domain abstractions.

**DO:** Create specific domain objects for specific behaviors. If multiple types share a pattern, use polymorphism — each type owns its own behavior.

Example (correct):
```
WireTransfer
- validate() → validates SWIFT code, multi-day settlement rules
- execute() → executes wire-specific settlement

ACHTransfer
- validate() → validates routing number, batch rules
- execute() → executes ACH-specific settlement
```

**DO NOT:** Use generic "resolver" or "handler" classes that route all behavior through one point. These centralize decisions that should be distributed to domain objects.

Example (wrong):
```
TransferResolver
- resolve(type, data) → if type == "wire": ... elif type == "ach": ... elif ...
```
