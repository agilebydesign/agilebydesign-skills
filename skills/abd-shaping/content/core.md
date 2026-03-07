# Core Definitions

<!-- section: shaping.core.interaction -->
## An Interaction

A single meaningful exchange between two actors that results in either:
- A meaningful **retrieval** of state, OR
- A meaningful **change** of state

**Each interaction includes:**
- **Actor** (Initiating) — who starts the exchange
- **Supporting** — who responds (typically a system, subsystem or component)
- **State Concepts** — domain concepts involved
- **Required State** — preconditions, what must be true from a state perspective
- **Initiation** — what the initiating actor does (verb-noun)
- **Response** — what the supporting actor does (behavior only; no state language)
- **Resulting State** — what must be true afterward (state only; no action language)
- **Failure Modes** — how the exchange can fail (max 3, rule/state based)

<!-- section: shaping.core.state_concept -->
## State Concept

A domain concept that holds state and can be operated on. It is defined in the State Model and scoped to the Epic or Story that owns it.

**Each State Concept includes:**
- **Concept name** — optionally `: BaseConcept` if it extends another
- **Properties** — state the concept holds; `<type> property` (e.g., `Number balance`, `LineItem[] line-items`)
- **Collaborating concepts** — other concepts this property works with or depends on (optional, listed under the property)
- **Invariant** — constraint on a property; when an invariant applies to a single property, state it under that property
- **Operations** — what can be done to the concept; `<return type> operation(<params>)` (e.g., `debit(Amount): Transaction`, `addItem(Book, Quantity): LineItem`)
- **Collaborating concepts** — other concepts this operation works with or depends on (optional, listed under the operation)
- **Invariant** — constraint on an operation; when an invariant applies to a single operation, state it under that operation

**Relationship between Interactions and State Concepts:**
- Interactions **reference** State Concepts in their Required State, State Concepts field, and Resulting State
- **Required State** describes what must be true of the State Concepts before the interaction (e.g., Account status = active)
- **Resulting State** describes what becomes true of the State Concepts after the interaction (e.g., Shopping Cart: empty → has-items)
- **Response** (behavior) operates on State Concepts; the operations defined in State Concepts are what the supporting actor performs
- **Workflow:** Start with interactions → identify which concepts are touched → model them in the State Model; scope each concept to the Epic or Story that owns it
