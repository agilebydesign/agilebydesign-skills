---
title: Cross-cutting domain concepts
impact: HIGH
tags: [discovery,exploration, interaction_tree, epic, story, domain]  
---

## Cross-cutting domain concepts

Some domain concepts appear across multiple sub-epics, epics, or entity types — not just within one part of the context. These are cross-cutting concepts. They are often the most important concepts in the domain model because they connect otherwise separate workflows. Identify them during variation analysis and treat them as first-class citizens in the domain model and the scaffold.

**DO** scan the entire context for domain concepts that are referenced by 3+ sub-epics or 2+ epics. These are cross-cutting — they connect different parts of the system. Call them out in a dedicated section of the variation analysis (e.g. "Core Domain Logic") and make them first-class concepts in the domain model.
- Example (right): **Transaction** is referenced by Payments (create), Collections (create), Refunds (reverse), Reporting (query), and Compliance (validate). It's cross-cutting. Variation analysis gets a "Core Domain Logic: Transaction Lifecycle" section. **Transaction** is a first-class domain concept with its own properties, operations, state transitions, and collaborators. Every sub-epic that uses it references the shared concept.
- Example (right): **AuditTrail** is written to by Order Processing, Payment Processing, User Management, and Compliance. It's cross-cutting. It gets its own domain concept with properties (timestamp, actor, action, entity, before/after state) and is referenced by all four sub-epics.

**DO** trace how the cross-cutting concept is used differently by each participant — what produces it, what consumes it, what modifies it, what queries it. This reveals the concept's full lifecycle and ensures the domain model captures all its operations.
- Example (right): **Notification** is produced by Order Processing (order confirmed), Payment Processing (payment failed), and User Management (password reset). Each produces different notification types, but all share the same delivery pipeline (create → route → deliver → track). Domain model captures the shared pipeline and the type-specific data.

**DO NOT** treat a concept as local to one sub-epic when it appears across multiple parts of the context. Burying a shared concept inside one sub-epic hides its true scope and creates drift between the interaction tree and the domain model.
- Example (wrong): **ValidationResult** used by Payment validation, Order validation, and User registration validation — but only defined as a property inside the Payment sub-epic's domain description. Other sub-epics reinvent it or reference it inconsistently.
- Example (wrong): **Status** (pending/active/suspended/closed) applied to Accounts, Orders, and Subscriptions — but treated as three separate concepts instead of one shared **LifecycleStatus** with entity-specific extensions.

**How to identify cross-cutting concepts:**
1. During variation analysis, list every domain concept mentioned in each sub-epic/epic
2. Cross-reference: which concepts appear in 3+ sub-epics or 2+ epics?
3. For each cross-cutting concept: who produces it? Who consumes it? Who modifies it? Who queries it?
4. Elevate to a dedicated variation analysis section and make it first-class in the domain model
5. Ensure every sub-epic and story that participates references the shared concept — no drift
