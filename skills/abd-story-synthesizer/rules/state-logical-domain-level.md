---
title: Logical/domain level
impact: HIGH
tags: shaping, discovery, exploration, specification
scanner: logical_domain
---

## Logical/domain level

**DO** keep everything at logical/domain level.
- Example (right): "Customer adds Book to Shopping Cart"; "Order created (submitted)"; "System validates payment details".

**DO NOT** describe implementation details or include infrastructure or technical failures.
- Example (wrong): "REST API returns 200"; "INSERT INTO orders"; "Database timeout"; "Network unreachable". Right: "Order persisted"; "Payment validated"; "Insufficient balance".
