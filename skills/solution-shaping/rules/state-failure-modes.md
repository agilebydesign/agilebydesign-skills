---
title: Failure modes
impact: MEDIUM
tags: state, failure, domain
---

## Failure modes

**DO** limit failure modes to a maximum of 3 per interaction; derive from domain rules, state conditions, or authorization.
- Example: "Insufficient balance"; "Account suspended"; "Cart is empty".

**DO NOT** include infrastructure or technical failures.
- Example: "Database timeout"; "Network unreachable"; "Server crash".
