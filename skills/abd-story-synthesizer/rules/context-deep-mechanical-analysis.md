---
title: Deep mechanical analysis
impact: HIGH
tags: [discovery, interaction_tree, epic, story, domain]
---

## Deep mechanical analysis

Source material — whether documents, code, architecture diagrams, APIs, or specifications — often organizes content by superficial categories (chapters, modules, layers, teams, document sections). The real groupings come from analyzing the actual data: shared domain objects, shared state transitions, shared resolution patterns, shared workflows. During variation analysis, look past the source's own structure and group by what the content actually shares.

**DO** read the actual content of each item and identify shared mechanics across source categories. Ask: what domain objects does this share with other items? What state does it produce or consume? What workflow or resolution pattern does it follow? Group by shared mechanic, not by source heading.
- Example (right): Source has "Payments" chapter with Wire Transfer and ACH Transfer, and a separate "Collections" chapter with Direct Debit. All three share: **Account** debit/credit, **Transaction** lifecycle (initiated → authorized → settled → reconciled), **ComplianceCheck** validation. Group as "Execute **Transaction**" sub-epic, not "Payments" and "Collections" sub-epics.
- Example (right): Source lists "Refund" under Customer Service and "Chargeback" under Risk. Both reverse a **Transaction**, restore **Account** balance, and update **LedgerEntry**. Group as "Reverse **Transaction**" — same domain objects, same state flow, different trigger.

**DO NOT** accept the source material's own categories as the groupings for sub-epics and stories. Source structure is organizational convenience, not mechanical truth.
- Example (wrong): Sub-epic "Payments" with Wire and ACH stories, separate sub-epic "Collections" with Direct Debit story — even though all three share **Transaction** lifecycle, **Account** operations, and **ComplianceCheck**.
- Example (wrong): "Customer Service" sub-epic containing Refund and "Risk Management" sub-epic containing Chargeback — when both are the same Reverse **Transaction** mechanic with different entry points.

**How to force deep analysis:**
1. Read individual items (not just headings/summaries) — sample actual descriptions, definitions, specifications, code, or rules
2. For each item, identify: what domain objects does it reference? What state does it produce or consume? What workflow or resolution pattern does it follow?
3. Build a cross-reference: which items share the same domain objects, state transitions, or resolution patterns?
4. Group by shared mechanic, then note what differs within the group (parameters, not structure)
5. When the source labels something as one category but defines it in terms of another — trust the definition, not the label
