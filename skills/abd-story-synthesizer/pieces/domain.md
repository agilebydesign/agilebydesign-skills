
<!-- section: story_synthesizer.domain -->
# Domain Model

## Evidence-Driven Domain Discovery

Domain concepts emerge from the evidence pipeline — not from direct synthesis of raw context. The core principle: **do not go from nouns to classes. Go from context → mechanisms → behavior owners → object model.**

The pipeline has two stages: **upfront preparation** (done once per workspace) and **per-run modeling** (done on every slice run, regardless of session type).

### Upfront (done once, as part of session start)

These steps produce the raw material that all runs operate on. They execute during session creation (Phases 2–4 in the process) before any slices run:

1. **Evidence extraction** (CODE, scripts 02–07) — produces structured facts: actions, decisions, variations, states, relationships. Output: `evidence_graph.json`.
2. **Concept scan** (AI) — identifies core primitives, interaction phases, authority boundaries, variation axes, and implicit concepts. Output: `concept_scan.md`.

### Per-Run (done on every slice, every session type)

Every run that discovers new evidence must model it. The OOAD modeling steps execute on every slice — what varies is **depth**, not which steps run:

3. **Behavior packet detection** — cluster slice-scoped evidence into coherent mechanisms
4. **Mechanism synthesis** — find the real structural seams from packets
5. **Decision ownership** — assign each decision to the concept that should own it
6. **Object candidate formation** — derive candidates justified by owned behavior

The depth of modeling varies by session type (discovery, exploration, specification). See `pieces/session.md` for what each session type produces.

### Three Rules That Must Never Be Violated

1. **Do not go from nouns to classes.** Terms are index entries. Objects emerge from owned behavior, decisions, and state.
2. **Do not assign behavior to services until you fail to find a real owner.** Bias toward the information expert.
3. **Do not introduce inheritance until the domain proves substitutability and shared semantics.**

### Behavior Packet Detection

Detect coherent behavioral mechanisms before creating objects.

A behavior packet is a cluster of actions, decisions, required state, outputs, and variation rules that together form one mechanism.

**For each packet produce:**
- Name and description
- Actions included
- Decisions included
- Required state (information needed)
- Outputs and state changes
- Variation axis (if any)
- Likely role: domain object, value object, policy/strategy, state holder, or orchestration
- Evidence references

**Why this matters:** Behavior packets prevent the classic mistake of terms becoming classes and behavior getting pushed into services.

### Mechanism Synthesis

Move from packets to domain mechanisms. Ask:
- Which packets are facets of one deeper mechanism?
- Which mechanisms interact?
- Which mechanisms own important transitions, decisions, and outcomes?

**For each mechanism produce:**
- Name
- Inputs and outputs
- Internal decisions
- External collaborators
- Variation axes
- State touched
- Invariants enforced

**Why this matters:** Sometimes a packet is too small. Several packets may be one mechanism (e.g. targeting, delivery, resistance, condition progression). This finds the real structural seams. Objects should emerge from mechanisms, not the reverse.

### Decision Ownership

Assign each important decision to the concept that should own it.

**For each decision ask:**
- Who has the information needed?
- Who should own the rule?
- Who should enforce the invariant?
- Who should control the transition?
- Who should compute the outcome?
- Who should NOT own this?

**Rule:** Bias toward the information expert, not toward a controller or manager.

**For each mechanism produce:**
- Decision owner
- Collaborators required
- What remains orchestration only
- What should be polymorphic
- What should be stateful
- What should stay value-like

### Object Candidate Formation

Derive candidate objects from owned behavior and state.

**An object candidate must justify itself by at least one of:**
- Owns important decisions
- Enforces invariants
- Owns meaningful lifecycle or state
- Coordinates a tight behavior cluster as the natural expert
- Represents a cohesive value with validation and behavior
- Represents a true relationship with behavior of its own

If it is just "a noun that exists," it is not yet a valid object candidate.

**Output categories:**
- Domain entities
- Value objects
- Policies or strategies
- State holders
- Relationship objects
- Orchestration or application services (thin)

### Relationship and Boundary Modeling

Define real relationships based on behavior, not diagram aesthetics.

**For each relationship ask:**
- What behavior crosses this relationship?
- What decisions depend on it?
- Does the relationship have its own lifecycle or rules?
- Is it actually a hidden concept of its own?
- Is this ownership, association, collaboration, containment, or dependency?
- What consistency boundary applies?

**Also identify:**
- Aggregate-like boundaries
- State ownership boundaries
- Responsibility boundaries
- Creation and mutation boundaries

**Why this matters:** Fake relationships are one of the biggest causes of bad OO models. A relationship should exist because behavior needs it, not because nouns co-occur.

### Inheritance Test

Use inheritance only when the domain truly supports it. Test every proposed base/subtype structure:

1. **Shared identity or just shared algorithm?** If only shared algorithm, prefer strategy, policy, or composition.
2. **Stable substitutability?** Can every subtype truly stand in for the base without breaking behavior?
3. **Shared invariants?** Do subtypes inherit meaningful rules, not just fields?
4. **Variation in behavior or just configuration?** If the difference is data or config, do not create subtype inheritance.
5. **Does the hierarchy reflect the domain or the implementation?** If it is only convenient for code reuse, it is probably wrong.

**Good inheritance usually appears when:**
- The domain itself has a stable is-a structure
- The base has real semantics
- The subtypes share meaningful invariants and protocol

**Otherwise prefer:** composition, strategy, role objects, policies, tagged value types.

### Model Validation

Attack the candidate model before accepting it. This is mandatory on every run.

#### Scenario / Message Walkthrough

Make sure the model can actually behave. A model that looks elegant but fails in message flow is not good OOAD.

**Run walkthroughs for:**
- Happy path
- Error path
- Edge case
- Exception path
- Stateful repetition
- Alternate variation mode
- Recovery, retry, or cancellation where relevant

**Validate at two levels:**

**Scenario flow:** What happens in the domain?

**Message flow:** Which object sends what message to whom? Does the receiver know enough to act? Is the sender delegating a decision or making it centrally?

**This step exposes:** missing objects, misplaced behavior, centralization, fake relationships, state with no owner.

#### Anemia / Centralization Critique

Explicitly attack the candidate model before accepting it.

**Look for:**
- Centralized handlers, resolvers, or managers
- Anemic entities with no decisions
- Objects that are just data bags
- Config-holder pseudo-objects
- Orphan concepts (referenced but not modeled)
- State with no owner
- Rules with no owner
- Fake inheritance (shared fields, no shared semantics)
- Type, mode, or effect switches that should be polymorphism
- Orchestration making domain decisions
- Relationships with no behavioral significance

**AI must propose minimal corrections** for each issue found.

#### Final Domain Model Output

Produce the final model only after the previous steps have stabilized.

**For each object:**
- Name
- Purpose
- Core state (properties)
- Decisions owned
- Invariants enforced
- Collaborators
- Messages sent and received
- Lifecycle ownership (if applicable)

**Also include:**
- Polymorphic families
- Value objects
- Real relationship types (with behavioral justification)
- Boundary notes
- Orchestration skeleton (thin)
- Unresolved ambiguities
- Rejected alternatives (if useful)

**The final model should be a consequence of the earlier reasoning, not a guess.**

---

## Domain Model Structure

The Domain Model holds **modules**, **domain concepts**, and **foundational classes** — all in one file (`domain-model.md`). Concepts are referenced in interactions via `**Concept**` in Pre-Condition, Trigger, Response, and Failure-Modes. Every `**Concept**` must exist in the Domain Model. No drift between tree and model. Use source entity data, not aggregated/calculated values.

### Module

A grouping of tightly related concepts that collaborate around the same mechanism.

- **name** — module name
- **concepts** — list of tightly related domain concepts

Each module typically maps to one page in the class diagram.

### Domain Concept

A domain concept holds state and can be operated on (equates to a class in OO code). Concepts participate as callers, receivers, and collaborators in interactions; state flows through Pre-Condition, Triggering-State, and Resulting-State.

- **Name**
- **Module** — which module this concept belongs to
- **Base-Concept** — optional; parent concept for inheritance
- **Foundational** — tag `[foundational]` if this is a core class (see below)
- **Properties** — with optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter.
- **type selection:** Use `Dictionary<K,V>` when items are accessed by a key (name, type, id) — this applies to most "has many" relationships where you look up by name (e.g. abilities by type, skills by name, features by name). Use `List<T>` only when order matters and items are accessed by position (e.g. turn order, degree progression, sequential steps). Default to `Dictionary` for named domain collections.
- **Operations** — with optional collaborating concepts and invariants. It should be easy to reverse engineer the interactions in the interaction diagram to at least some level of operations on the Domain Model.

**Concept relationships:** When a concept "has" another concept, use composition (strong has-a; part cannot exist without whole) or aggregation (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.

### Foundational Classes

A **foundational class** is a domain concept tagged `[foundational]`. Foundational classes are the stable core that everything else hangs off — the base collaborations that repeat across the system. Later slices add concepts that extend or use foundational classes, but the foundational classes themselves remain stable.

There is one domain model, not separate "foundational" and "full" models. The tag distinguishes core classes from extensions.

Example: in a payments system, Account + Transaction + ValidationRule collaborate the same way whether you're processing a wire transfer, ACH, or direct debit. These three are foundational classes. Wire, ACH, and direct debit are extensions added in later slices.

**How foundational classes emerge:**

Foundational classes are identified through the OOAD pipeline, not by scanning for nouns:

1. **Evidence graph hotspots** — high co-occurrence terms indicate tightly collaborating concepts. These are foundational candidates.
2. **Concept scan primitives** — core primitives and authority boundaries point to decision owners.
3. **Behavior packet detection → mechanism synthesis → decision ownership → object candidate formation** — the per-run OOAD steps confirm candidates by demonstrating they own behavior, not just data.

Do NOT trust source document categories. Do NOT group by surface similarity. Group by what objects collaborate and what operations they perform.

**Lifecycle across slices:**

- **Discovery slices** — produce foundational classes (base classes, core collaborations). Tag them `[foundational]`. Skip variations — if a base class has a million specializations, wait for later slices.
- **Later discovery slices** — add more classes. Some extend foundational classes (e.g., Ability extends Trait). Some become new foundational classes if they establish a new collaboration pattern.
- **Exploration slices** — add depth to existing classes (operations, invariants, trigger/response). May add new classes but mostly fill in what discovery sketched.
- **Specification slices** — add examples, scenarios, edge cases. Rarely add new classes.

Foundational classes get extra scrutiny: inheritance test, anemia critique, scenario walkthrough.

### Output Format

```
**ConceptName** [foundational] : <Base Concept if any>
- <type> property
      <collaborating concepts if any>
- <type> operation(<param>, ...)
     <collaborating concepts if any>
- Interactions: interaction nodes this concept is used by
- examples: list of domain concept tables in interaction tree using this concept
```

**Output location:** `<session>/domain-model.md` between `<!-- section: foundational_models -->` and `<!-- /section: foundational_models -->` markers.

### Example: Domain Model for Country-Specific Payment

Based on the Complete Example in the Interaction Tree (Make **Country**-specific **PaymentType**):

#### Module: Payment

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

These concepts are referenced in the Interaction Tree via `**Concept**` in Pre-Condition, Trigger, Response, and Examples.
