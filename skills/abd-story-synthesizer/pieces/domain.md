<!-- section: story_synthesizer.domain.model -->
# Domain Model

The Domain Model holds **modules** (groupings of tightly related concepts) and **domain concepts** — the things that have state and can be operated on. Concepts are referenced in interactions via `**Concept**` in Pre-Condition, Trigger, Response, and Failure-Modes. Every `**Concept**` must exist in the Domain Model; concepts must be placed at the right level in the hierarchy. No drift between tree and model. Use source entity data, not aggregated/calculated values.

## Module

Grouping of tightly related concepts.

- **name** — module name
- **concepts** — list of tightly related domain concepts

## Domain Concept

A domain concept that holds state and can be operated on. Referenced in interactions via `**Concept**` in labels. Examples live on the interaction. The Domain Model connects what concepts know and do to interactions — concepts participate as callers, receivers, and collaborators; state flows through Pre-Condition, Triggering-State, and Resulting-State.

- **Name**
- **Module** — optional; grouping of tightly related concepts
- **Base-Concept** — optional
- **Properties** — with optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter.
- **Operations** — with optional collaborating concepts and invariants. It should be easy to reverse engineer the interactions in the interaction diagram to at least some level of operations on the Domain Model.

**Concept relationships:** When a concept "has" another concept, use composition (strong has-a; part cannot exist without whole) or aggregation (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.

---

<!-- section: story_synthesizer.domain.example -->
## Example: Domain Model for Country-Specific Payment (from Interaction Tree)

Based on the Complete Example in the Interaction Tree (Make **Country**-specific **PaymentType**), here are the corresponding domain concepts:

### Module: Payment

**Country**
- String country_code
- String country_name
- Operations: lookup by code, list available for user

**PaymentType**
- String payment_type (e.g. wire, ach)
- List<String> fields (from PaymentTypeFieldTypes)
- Operations: get fields for type, validate availability for country

**UserPaymentAccess**
- String user_name
- String country_code
- String payment_type
- Boolean available
- Operations: check(user, country, payment_type) → available

**PaymentDetails**
- String payment_type
- Number amount
- String currency
- String beneficiary_id
- String swift_code (wire) | routing_number, account_number (ach)
- Operations: validate(), submit()

**User**
- String user_name
- String user_role
- Operations: has_session(), has_access(country, payment_type)

**Session**
- String session_id
- Instant expires_at
- Operations: is_active(), extend()

**PaymentTypeFieldTypes**
- String payment_type
- List<String> fields
- Operations: get_fields(payment_type) → fields

These concepts are referenced in the Interaction Tree via `**Concept**` in Pre-Condition, Trigger, Response, and Examples. The interaction tree tables (Logged In User, Active User Session, User Payment Type Access, Selected Country, PaymentDetails (wire), etc.) are example data for these concepts.

---

<!-- section: story_synthesizer.domain.output -->
## Output Format

Format specification for the Domain Model output. Separate from the Interaction Tree. Concepts referenced via `**Concept**` in labels. See the Example above and the Complete Example in the Interaction piece for a full reference.

```
Concept : <Base Concept if any>
- <type> property
      <collaborating concepts if any>
- <type> operation(<param>, ...)
     <collaborating concepts if any>
- Interactions Interaction Concept used by (root node only)
- examples: list of domain concept tables in interaction tree using this concept
```
