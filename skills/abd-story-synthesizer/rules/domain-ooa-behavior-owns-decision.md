---
title: Behavior Owns Decision
impact: HIGH
tags: [discovery, ai_passes, domain]
scanner: decision_ownership
---

# Behavior Owns Decision

Place behavior on the object that owns the data needed for the decision. The information expert should own the rule.

**DO:** Assign decisions, validation, and rule enforcement to the object that holds the state needed to make the decision. If an object has properties, it should also have operations that use those properties.

Example (correct):
```
Account
- Number balance
- can_debit(amount) → balance >= amount
- debit(amount) → enforces invariant, updates balance
```

**DO NOT:** Split data from the logic that operates on it. Objects with properties but no meaningful operations are anemic — the decisions are elsewhere, typically in a service or manager.

Example (wrong):
```
Account
- Number balance
(no operations — debit logic lives in AccountService.debit(account, amount))

AccountService
- debit(account, amount) → checks account.balance >= amount, sets account.balance -= amount
```
