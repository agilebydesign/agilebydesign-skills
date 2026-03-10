---
title: Example tables match Domain Model
impact: HIGH
tags: [specification, example, domain]
scanner: example_domain_match
---

## Example tables must align with Domain Model

**DO** ensure every example table corresponds to a domain concept in the Domain Model. Table columns must match the concept's properties. Table relationships must match the Domain Model's concept relationships (composition, aggregation). Every `**Concept**` referenced in Pre-Condition, Trigger, or Response labels must have a corresponding example table (or inherit one). Every example table must be referenced via `**Concept**` in labels — no orphaned tables.
- Example (right): Domain Model has `Country` with properties `country_code`, `country_name`. Example table: `Selected Country: | scenario | country_code | country_name |`. Domain Model has `User` → `Session` (composition). Tables appear in order: `Logged In User`, then `Active User Session` — relationship expressed through table ordering.

**DO** use source entity data in tables, not aggregated or calculated values. Show the actual records that produce the outcome. If a scenario computes a result, the table shows the inputs, not the output count.
- Example (right): `UpdateReport (renames): | original_name | new_name | parent |` — shows actual renamed entities.
- Example (wrong): `UpdateReport: | renames_count | new_count | | 1 | 2 |` — counts defer real work; where do these numbers come from?

**DO** express table relationships through table ordering and qualifier names — not through ID columns. IDs are implementation concerns. Domain Model says `Epic` contains `SubEpic`; tables appear in that order: `Epic` first, then `SubEpic (child of Epic)`.
- Example (right): `User: | user_name | user_role |` then `Session: | user_name | session_id | expires_at |` — connected by domain attribute, not by `user_id` foreign key.

**DO NOT** have `**Concept**` in labels without a matching example table. Do not have example tables that no label references. Do not invent column names not in the Domain Model — use the concept's actual property names.
- Example (wrong): Steps reference `**PaymentType**` but no PaymentType example table exists. Or: `Entitlement` table exists but no step mentions `**Entitlement**`.
- Example (wrong): Domain has `recipient_name` but table uses `payee` or `beneficiary_label`.

**DO NOT** flatten related concepts into one table or use lookup-style tables with ID columns for joining. Each concept gets its own table; relationships are expressed through ordering and qualifiers.
- Example (wrong): `| enterprise_id | recipient_id | account_id |` — flat table loses relationship structure. Right: separate tables for Enterprise, Recipient, Account in domain relationship order.
