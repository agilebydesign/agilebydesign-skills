---
title: Deep mechanical analysis
impact: HIGH
tags: [discovery, interaction_tree, epic, story, domain]
---

## Deep mechanical analysis

Source material — whether documents, code, architecture diagrams, APIs, or specifications — often organizes content by superficial categories (chapters, modules, layers, teams, document sections). The real groupings come from analyzing the actual data: shared domain objects, shared state transitions, shared resolution patterns, shared workflows. During variation analysis, look past the source's own structure and group by what the content actually shares.

**DO** read the actual content of each item and identify shared business logic, data, and structure across source categories. Ask: what domain objects does this share with other items? What state does it produce or consume? What workflow does it follow? Group by shared business logic, not by source heading.
- Example (right): Source has "Payments" chapter with Wire Transfer and ACH Transfer, and a separate "Collections" chapter with Direct Debit. All three share: **Account** debit/credit, **Transaction** lifecycle (initiated → authorized → settled → reconciled), **ComplianceCheck** validation. Group as "Execute **Transaction**" sub-epic, not "Payments" and "Collections" sub-epics.
- Example (right): Source lists "Refund" under Customer Service and "Chargeback" under Risk. Both reverse a **Transaction**, restore **Account** balance, and update **LedgerEntry**. Group as "Reverse **Transaction**" — same domain objects, same state flow, different trigger.

**DO** elevate shared business logic to a dedicated section in the variation analysis when it is identified. Core domain logic that spans multiple sub-epics or epics must be called out explicitly — not buried inside individual sub-epic descriptions. The variation analysis should have a section (e.g. "Core Domain Logic") that names the shared elements, lists what participates, and states what differs. This section drives the scaffold and the domain model — shared concepts become first-class citizens, not implementation details of individual stories.
- Example (right): Analysis reveals that "Compliance Validation" is shared across Payments, Collections, and Transfers — three different sub-epics. Variation analysis gets a "Core Domain Logic: Compliance Pipeline" section. **ComplianceCheck**, **ValidationRule**, and **ComplianceResult** become first-class domain concepts. Every sub-epic that uses the pipeline references it.
- Example (wrong): "Payments" sub-epic mentions ComplianceCheck in passing. "Collections" sub-epic mentions it separately. No connection drawn. Domain model has no ComplianceCheck concept — it's just a bullet point inside each sub-epic's description.

**DO NOT** accept the source material's own categories as the groupings for sub-epics and stories. Source structure is organizational convenience, not the truth about what business logic is shared.
- Example (wrong): Sub-epic "Payments" with Wire and ACH stories, separate sub-epic "Collections" with Direct Debit story — even though all three share **Transaction** lifecycle, **Account** operations, and **ComplianceCheck**.
- Example (wrong): "Customer Service" sub-epic containing Refund and "Risk Management" sub-epic containing Chargeback — when both are the same Reverse **Transaction** workflow with different entry points.

**How to force deep analysis:**
1. Read individual items (not just headings/summaries) — sample actual descriptions, definitions, specifications, code, or rules
2. For each item, identify: what domain objects does it reference? What state does it produce or consume? What workflow does it follow?
3. Build a cross-reference: which items share the same domain objects, state transitions, or workflows?
4. Group by shared business logic, then note what differs within the group (parameters, not structure)
5. When the source labels something as one category but defines it in terms of another — trust the definition, not the label
6. Anything shared by 3+ sub-epics or 2+ epics is core domain logic — elevate it to a dedicated variation analysis section and make its concepts first-class in the domain model
