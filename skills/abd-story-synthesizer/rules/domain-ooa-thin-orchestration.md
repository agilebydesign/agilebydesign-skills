---
title: Thin Orchestration
impact: HIGH
tags: [discovery, ai_passes, domain]
scanner: thin_orchestration
---

# Thin Orchestration

Orchestration layers coordinate — they do not decide. Business logic belongs to the object that owns the data needed for the decision.

**DO:** Keep orchestrators thin — they sequence calls, pass messages, and handle lifecycle. Decisions, validation, and rule enforcement live on domain objects.

Example (correct):
```
PaymentProcessor (orchestration)
- process(payment) → delegates to payment.validate(), account.debit(), settlement.execute()

Payment (domain object)
- validate() → owns validation rules
- apply_fees() → owns fee calculation
```

**DO NOT:** Put business logic in orchestrators, managers, or handlers. If an orchestrator is making decisions about domain state, the decision belongs on the domain object instead.

Example (wrong):
```
PaymentProcessor (orchestration)
- process(payment) → checks payment.amount > 0, checks account.balance >= amount, calculates fees, applies discount rules
```
