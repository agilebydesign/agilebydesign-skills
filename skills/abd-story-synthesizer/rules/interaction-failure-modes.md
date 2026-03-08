---
title: Failure modes
impact: MEDIUM
tags: story, step
scanner: failure_modes
---

## Failure modes

**DO** limit failure modes to a maximum of 3 per interaction; derive from domain rules, state conditions, or authorization.
- Example (right): "Insufficient balance"; "Account suspended"; "Cart is empty"; "Payment type not available for country".

**DO NOT** include infrastructure or technical failures.
- Example (wrong): "Database timeout"; "Network unreachable"; "Server crash". Right: "Insufficient balance"; "Account suspended".
