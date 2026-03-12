
<!-- section: story_synthesizer.domain -->
# Domain Model

## Module

Grouping of tightly related concepts.

- **name** — module name
- **concepts** — list of tightly related domain concepts

## Domain Concept

A domain concept that holds state and can be operated on (equates to a class in object oritented code). Referenced in interactions via `**Concept`** in labels. Examples live on the interaction. The Domain Model connects what concepts know and do to interactions — concepts participate as callers, receivers, and collaborators; state flows through Pre-Condition, Triggering-State, and Resulting-State.

- **Name**
- **Module** — optional; grouping of tightly related concepts
- **Base-Concept** — optional
- **Properties** — with optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter. 
- **type selection:** Use `Dictionary<K,V>` when items are accessed by a key (name, type, id) — this applies to most "has many" relationships where you look up by name (e.g. abilities by type, skills by name, features by name). Use `List<T>` only when order matters and items are accessed by position (e.g. turn order, degree progression, sequential steps). Default to `Dictionary` for named domain collections.
- **Operations** — with optional collaborating concepts and invariants. It should be easy to reverse engineer the interactions in the interaction diagram to at least some level of operations on the Domain Model.

**Concept relationships:** When a concept "has" another concept, use composition (strong has-a; part cannot exist without whole) or aggregation (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.

---



## Example: Domain Model for Country-Specific Payment (from Interaction Tree)

Based on the Complete Example in the Interaction Tree (Make **Country**-specific **PaymentType**), here are the corresponding domain concepts:

### Module: Payment

**Country**

- String country_code
- String country_name
- Operations: lookup by code, list available for user

**PaymentType**

- String payment_type (e.g. wire, ach)
- List fields (from PaymentTypeFieldTypes)
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
- List fields
- Operations: get_fields(payment_type) → fields

These concepts are referenced in the Interaction Tree via `**Concept`** in Pre-Condition, Trigger, Response, and Examples. The interaction tree tables (Logged In User, Active User Session, User Payment Type Access, Selected Country, PaymentDetails (wire), etc.) are example data for these concepts.

---



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




## Foundational Object Models

A **foundational object model** is a subset of the domain model — a discrete set of objects, their logic, relationships, interactions, and state transitions — that serves as the base for the rest of the model. These models appear repeatedly across the system. Different parts of the system extend foundational objects but specialize with different data or rules. When you see the same objects doing the same things in multiple places, that's one foundational model.

Example: in a payments system, Account + Transaction + ValidationRule collaborate the same way whether you're processing a wire transfer, ACH, or direct debit. The base collaboration (debit account, validate, settle) is the foundational model. Wire vs ACH vs direct debit are extensions — they add different validation rules and settlement timing, but the objects and operations are the same.

Each foundational model likely becomes a distinct module in the domain model.

**How to identify foundational models (OOAD):**

1. **Find the objects.** Read through the context looking for domain nouns — things that hold state and get operated on. Not source document headings — actual things described in the content.
2. **Find the collaborations.** For each object, what other objects does it work with? What operations do they perform on each other? What state flows between them?
3. **Find the repetition.** Where do you see the same group of objects collaborating the same way in multiple places? That repetition is a foundational model.
4. **Do NOT trust the source document's categories.** Read actual content. Group by shared collaborations, not by chapter headings.
5. **Do NOT group by surface similarity.** Group by what objects collaborate and what operations they perform.

Use `concept_tracker.py report` to validate — high co-occurrence terms likely belong to the same foundational model.

**One sub-section per foundational model. Each contains:**

- **Domain Model** — Complete typed concept(s) with properties, operations, collaborators, invariants. Same format as domain concepts below. Use `Dictionary<K,V>` for named collections; `List<T>` only when order matters.
- **Extensions** — List of objects that extend or specialize this model. Names only.

**Output location:** Write to `<session>/domain-model.md` between `<!-- section: foundational_models -->` and `<!-- /section: foundational_models -->` markers.

---

The Domain Model holds **modules** (groupings of tightly related concepts) and **domain concepts** — the things that have state and can be operated on. Concepts are referenced in interactions via `**Concept`** in Pre-Condition, Trigger, Response, and Failure-Modes. Every `**Concept**` must exist in the Domain Model; concepts must be placed at the right level in the hierarchy. No drift between tree and model. Use source entity data, not aggregated/calculated values.
