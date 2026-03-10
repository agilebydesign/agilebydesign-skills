---
title: Background vs scenario setup
impact: MEDIUM
tags: [story, scenario, example]
scanner: background_setup
---

## Shared setup as Pre-Condition with Examples at story level

**Background** (BDD) = **Pre-Condition with Examples at the story level**. Scenarios below inherit that Pre-Condition and Examples. No separate Background section — use the interaction hierarchy.

**DO** put shared setup as Pre-Condition with Examples on the story (or epic). Use Given/And only — state, not actions. Use **Concept** notation. Scenarios show inherited Pre-Condition and Examples in brackets.

**Example (right):**

```
#### Story: User Triggers Country-Specific PaymentType
- Pre-Condition: Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)
- Examples:
  Logged In User:
  | scenario   | user_name | user_role |
  |------------|-----------|-----------|
  | success    | Jane Doe  | Payer     |
  ===
  Active User Session:
  | scenario   | user_name | session_id | expires_at |
  |------------|-----------|------------|------------|
  | success    | Jane Doe  | sess-001   | 2025-03-08 |

##### Scenario: Success — payment validated and confirmed
- Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
- Examples: [Logged In User, Active User Session]

###### Steps
- Step 1: Browse Country for Payment ...
```

**DO NOT** repeat setup in each scenario when it applies to all. Do not put actions in Pre-Condition — only state (Given/And). Do not use a separate "Background" block; use story-level Pre-Condition + Examples and inheritance.

**Example (wrong):** Each scenario repeats full Given/And and example tables. **Right:** Story holds Pre-Condition + Examples; scenarios show `[inherited]` or list names.
