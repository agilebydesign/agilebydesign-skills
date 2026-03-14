<!-- section: story_synthesizer.introduction -->
# Introduction

The story synthesizer skill turns context into an **Interaction Tree** and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. Outputs: story map, domain model, acceptance criteria, specifications.

**Interaction Tree:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). Epics group stories; the story is the backbone — the smallest unit that is both valuable and independently deliverable. Each epic and story can have Pre-Condition, Trigger, and Response. Scenarios optionally group steps; steps are atomic interactions.

**Domain Model:** Domain Models describe the state found in Pre-Condition, Trigger, and Response. **Domain Concepts** (the things that hold state and get operated on) are referenced via `**Concept**` in the name/labels of Interaction tree elements.

The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

 Domain concepts emerge from the use of a **17-step pipeline** that separates mechanical evidence extraction (CODE) from analytical reasoning (AI). Scripts extract structured evidence from contex into an **evidence graph** — actions, decisions, variations, states, and relationships.
 
 AI then operates on the evidence graph through focused passes — never on raw text directly. The evidence pipeline creates object models through behavior packet detection, mechanism synthesis, and decision ownership — not from surface noun extraction. Interaction Tree and Domain Model evolve together — no drift.

---

<!-- section: story_synthesizer.concept_scan -->
# Domain Concept Scan

The concept scan is the first AI step in the pipeline (Step 2). It runs after context has been normalized but before evidence extraction scripts run. Its purpose is to discover the conceptual structure of the system without designing classes.

## Goal

Produce a **conceptual map** that orients the evidence extraction scripts and feeds into later AI passes. This is not a domain model — it is a hypothesis about what the system is really about, where decisions live, and where behavior varies.

## Instructions

You are performing a domain concept scan.

Your goal is **NOT** to design classes yet.

Your goal is to discover the conceptual structure of the system.

Analyze the context and identify the following:

### 1. Core Domain Primitives

The fundamental things the system operates on. Not surface nouns — things that hold state, get transformed, or participate in decisions.

### 2. Interaction Phases

The major stages of domain interactions or resolution processes. What are the phases that context flows through?

### 3. Stateful Entities

Anything that accumulates state, conditions, or lifecycle changes. Things that are created, modified, tracked, or expired.

### 4. Authority Boundaries

Concepts that appear to own decisions or enforce rules. What decides? What validates? What controls transitions?

### 5. Resource Flows

Resources that are created, transferred, consumed, or modified. What moves through the system and who acts on it?

### 6. Variation Axes

Places where behavior changes depending on a mode, type, category, or condition. These often indicate polymorphic structures.

### 7. Rule Mechanisms

Clusters of rules that appear to revolve around the same mechanism. Rules that collaborate to produce an outcome.

### 8. Implicit Concepts

Missing or implicit concepts that appear necessary to explain the rules but are not named directly in the context.

## Constraints

- Do NOT assume these correspond to classes
- Be skeptical of surface nouns — focus on mechanisms, phases, and rule ownership
- Produce a conceptual map, not an object model
- After the map: identify potential conceptual abstractions that may later become domain objects
- Identify search anchors for targeted evidence extraction

## Output Structure

```
## Core Primitives
- [list]

## Interaction Phases
1. [ordered list]

## Stateful Entities
- [list]

## Authority Boundaries
- [list with what each controls]

## Resource Flows
- [list with flow direction]

## Variation Axes
- [list with what varies]

## Rule Mechanisms
- [list with mechanism description]

## Implicit Concepts
- [list with why each is needed]

## Search Anchors
- [terms/patterns for evidence extraction scripts to target]
```

## Output Location

Write to `<workspace>/story-synthesizer/concept_scan.md`.

---

<!-- section: story_synthesizer.evidence -->
# Evidence Model

Evidence extraction is the disciplined compression step of the pipeline. Scripts extract structured evidence from normalized context without pretending to design the model. These are evidence records, not object candidates.

## Canonical Evidence Structure

All extraction scripts write into a shared structure:

```json
{
  "documents": [],
  "terms": [],
  "actions": [],
  "decisions": [],
  "variations": [],
  "states": [],
  "relationships": [],
  "issues": []
}
```

| Type | Description | Script |
|------|-------------|--------|
| terms | Nouns, concepts — index entries for navigating context | `02_extract_terms.py` |
| actions | Subject-verb-object behavioral facts | `03_extract_actions.py` |
| decisions | Conditional logic (if/when/unless/must/on success/on failure) | `04_extract_decisions.py` |
| variations | Independent behavior axes (mode/type differences) | `05_extract_variations.py` |
| states | Lifecycle hints, condition accumulation, transitions | `06_extract_states.py` |
| relationships | Explicit associations, ownership, containment, dependency | `06_extract_states.py` |
| issues | Ambiguities, conflicts, contradictions | `07_consolidate_evidence.py` |

**Terms are index entries, not classes.** Actions and decisions carry stronger evidence for domain modeling than nouns do.

## Evidence Extraction Scripts

### Chunk index (abd-context-to-memory)

**Chunk index creation lives in `abd-context-to-memory`.** Run `index_memory.py --path <context_folder>` or `index_chunks.py --context-path <chunk_folder>` from that skill. Mandatory before `extract_evidence`.

- Validates chunk readiness: chunks present, count, paths, duplicates
- Builds chunk index with stable IDs, source locations, section mapping
- Output: `<workspace>/story-synthesizer/context/chunk_index.json`

### 02_extract_terms.py

Builds the concept index from normalized chunks.

- Extracts noun phrases, defined terms, section titles, repeated domain vocabulary
- Output: `terms.json` with `term_id`, `name`, `aliases`, `occurrences`

### 03_extract_actions.py

Extracts behavioral facts as subject-verb-object patterns.

- Example: "attacker makes attack check", "target rolls resistance", "effect applies condition"
- Output: `actions.json`

### 04_extract_decisions.py

Captures rule logic from conditional triggers.

- Triggers: if, when, unless, must, may not, on success, on failure
- Example: "if attack roll >= defense → hit"
- Output: `decisions.json`

### 05_extract_variations.py

Detects independent behavior axes.

- Patterns: "close vs ranged", "different types", "depending on", "one of the following"
- Output: `variations.json`

### 06_extract_states.py

Extracts stateful entities and explicit relationships.

- States: lifecycle hints, condition accumulation, transitions
- Relationships: explicit associations, ownership, containment, dependency
- Output: `states.json`, `relationships.json`

### 07_consolidate_evidence.py

Builds the AI-ready evidence graph from all extracted evidence.

- Creates: concept clusters, term→action links, term→decision links, variation links, state links, ambiguity list, conflict list, hotspot detection
- Output: `evidence_graph.json`, `evidence_summary.md`

## File Layout

**Source vs chunks:** Original content (PDF, PPTX, etc.) can live anywhere — track its path. The **chunks** (markdown output from `abd-context-to-memory`) must live in `story-synthesizer/context/`, not alongside the PDF. If no context path is configured, the skill looks in `context/` at workspace root for the **source** to chunk; chunk output goes to `story-synthesizer/context/`.

All processed context and evidence live under `story-synthesizer/`:

```
<workspace>/
  context/                  # original source (PDF, etc.) — default when none set; chunks go to story-synthesizer
  story-synthesizer/
    context/                # processed context
      chunks/               # chunk files (.md from abd-context-to-memory)
      chunk_index.json      # from abd-context-to-memory (index_chunks)
      context_analysis.json # from concept_tracker scan
      glossary.json         # from concept_tracker seed
    evidence/               # all evidence outputs
      terms.json, actions.json, decisions.json, variations.json, states.json, relationships.json
      evidence_graph.json, evidence_summary.md
```

**context_paths** in config points to `story-synthesizer/context/` (where chunks live) for evidence extraction.

## How Evidence Maps to Domain Model

| Evidence Type | Maps To |
|---------------|---------|
| actions | Operations on domain concepts |
| decisions | Policies, invariants, rules owned by concepts |
| variations | Polymorphic families, strategy patterns |
| states | Lifecycle, state machines, condition tracking |
| relationships | Composition, aggregation, association, dependency |
| terms | Index for navigating — NOT directly to classes |

## Running the Pipeline

```bash
# Chunk index: run from abd-context-to-memory first (index_memory.py or index_chunks.py)
python scripts/02_extract_terms.py --chunks <chunk_index.json>
python scripts/03_extract_actions.py --chunks <chunk_index.json>
python scripts/04_extract_decisions.py --chunks <chunk_index.json>
python scripts/05_extract_variations.py --chunks <chunk_index.json>
python scripts/06_extract_states.py --chunks <chunk_index.json>
python scripts/07_consolidate_evidence.py --extracted-path <extracted/>
```

Or use the build script shortcut:

```bash
python scripts/build.py extract_evidence
```

---

<!-- section: story_synthesizer.interaction.model -->
# Interaction Model

An interaction is a single meaningful exchange between two actors that results in either a retrieval of state or a change of state.

## Interaction

- **Name** — name of the interaction. **Ground in domain:** Every epic, story, scenario, and step must be grounded in domain language — either in the name or in the statement — using `**Concept**` (double stars, capitalization). Domain concepts must appear in `**Concept**` format so the domain conditions are described.
- **Statement** — one-sentence trigger and response; include domain concepts where appropriate.

**Name and statement (all nodes):** Use active verb language. Short name first, longer statement in brackets. Format: `Node: Short Name (Longer statement.)` — e.g. `Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays...)`. Name is always verb-noun or subject-qualifier; statement is always the longer sentence. **Epic statement:** Describe the scope of the epic (broad flows), not a single interaction. **Story/Step statement:** One trigger and response.
- **Impacts** — zero or more (see Impact below)
- **Constraints** — zero or more. Qualitative instructions on how this interaction is structured. A constraint may be a sentence, a reference to a collection of files, or (most commonly) a reference to a markdown file. Constraints are inherited from high to low (parent → child).
- **Pre-Condition** — label only. What must be true before. State qualifies through the label. Use `**Concept**` to reference domain concepts; each must exist in the Domain Model.
- **Trigger** — Triggering-Actor, Behavior (label), Triggering-State. Triggering-State is any state that qualifies the interaction (e.g. selecting an option of a certain type). Labels reference domain concepts; examples live on the interaction.
- **Response** — Responding-Actor, Behavior (label), Resulting-State. Resulting-State is the state that results from the interaction. Labels reference domain concepts; examples live on the interaction.
- **Examples** — collection of tables at the interaction level. One per concept referenced in labels. Pre-Condition, Trigger, and Response reference these through their labels; examples live on the interaction. Identify examples from boundary values, distinct scenarios, and representative combinations from steps and state.
- **Failure-Modes** — up to three; how the exchange can fail (rule/state based only)
- **Children** — child interactions of this interaction.

### Interaction Tree Rules

**Epics from context (not slices):** **DO NOT** name epics after slices. Epics and sub-epics come from the larger context (goal, domain, concept map, evidence) — they are functional. Place slice stories under appropriate sub-epics. Mark remainder as estimated.

**Node Hierarchy**
- Epic - Can nest to have epic children or story children. An epic whose parent is an epic is sometimes called a sub-epic. Names are typically simple verb-noun.
- Story - Smallest unit of testable value that is independently delivered. Names are typically simple verb-noun.
- Scenario - Groups steps; optional container for a story. Names describe the primary conditions tested in the scenario. Split scenarios when pre-conditions differ, success vs failure paths, or different branches.
- Step - Atomic interaction within a scenario. Steps are interactions: often in the form of **Trigger** (When) and **Response** (Then). Identify separate steps when: explicit action-reaction, actor or response changes, or when enumerating permutations (validation paths, branches, edge cases).

Epic → children (Epics, Stories)
Story → Scenarios OR Steps
Scenario → Steps
Step → lowest interaction for now

### The Story as Backbone

The **story** is the backbone of all the work above and below it. It is the central unit that everything connects to.

- **Above the story:** Epics and sub-epics exist only to **group stories together**. They are organizational structure, not the primary unit of value.
- **Below the story:** All steps, examples, and scenarios **belong to the story**. The story is the central spoke — everything below it hangs off the story.

**What a story is:** A story is something we can reasonably discuss as a valuable tactical interaction between the user and the system (or between systems). It is something that can be developed in a small amount of time — typically a couple of days for a developer (or a couple of hours for AI :). It is the smallest unit that is both valuable and independently deliverable. It needs to be testable, which means it must have a recognizable behavior that a user or stakeholder would recognize. Not necessarily always user-facing, but at least recognizable as a tangible business state that's changed or logic has been executed here.

**Stopping point:** The story is typically the stopping point **for Shaping and Discovery**. For Exploration and Specification, we go below the story (to steps, examples, scenarios). With slices and runs, *we have explicit control on the stopping point*: a run on a slice of a couple of epics can have criteria to only identify other epics and not stories. The stopping point is configurable. See Impact below for the Impact data model (types, status, evidence linking).

**Commonly Generated Fields Vary By Node Type:**
Any node level can use any field. Exceptions are always possible. The table below lists what we commonly generate for each node.

| Node | Commonly generated | Case By Case Generated |
|------|--------------------|------------------------|
| Epic | Triggering-Actor, Responding-Actor, Name (Verb Noun), Impact, Constraints | Pre-Condition, Triggering-State, Resulting-State, Examples, Failure-Modes|
| Story | Trigger , Response ; Name (Verb Noun), Examples, Pre-Condition (eg BDD background, Given, And); Failure-Modes, Constraints |
| Scenario | Trigger, Response, Pre-Condition (eg BDD Given, And); Examples |
| Step | Trigger, Response,(When, And, Then, And); Examples; Constraints (when step-specific) |

**Nodes inherit attributes from their parents.**
Child nodes inherit state, examples, pre-conditions, actors, domain concepts, and constraints. You can show inherited attributes explicitly in square brackets (e.g. `Triggering-Actor: [User]`, `Examples: [Logged In User, Active Session]`) so readers see which values came from the parent. When you use brackets, update them if the parent changes. **Inheritance applies either way** — even when you don't show brackets, the inherited values still apply to the child. See Interaction Tree Inheritance for conventions.

**Inheritance that we often want to call out explicitly through the [inherited thing] notation**
- **Epic from Epic:** Domain concepts. Lower-level epics (sub-epics) often use the inherited domain concepts from their parent epic.
- **Story from Epic:** Triggering-Actor, Responding-Actor, Pre-Condition, Examples based on Pre-Condition, domain concepts.
- **Scenario from Story:** Almost nothing needs to be explicitly stated.
- **Step from Story:** Triggering-Actor and Responding-Actor are often used, eg [User] and [System] from the story or higher. Exception: when a step is system-triggered (e.g. "When **System** receives payment type selection"), that step may override Triggering-Actor.

**Domain grounding:** Every epic, story, scenario, and step must be grounded in domain language. This primarily comes from the interactions (e.g., trigger and response) if they have been defined, but if they have not been defined, then it would come from the name or the statement. When trigger and response have been defined, the name is based on those, but sometimes we don't define these for a node, and just define the name at first. In either case, all of the above need to be grounded using `**Concept**` (double stars on both sides, capitalization). Avoid generic terms; use `**Country**`, `**PaymentType**`, etc., not "country" or "payment type". Concepts must come from the Domain Model here. Concept identified as part of exploring the interaction tree should be added to the Domain Model and vice versa. When we add things to the Domain Model, we should explore which interactions require those and update accordingly.

Concepts are placed at the level of the interaction hierarchy where they apply to all descendants. Every `**Concept**` must exist in the Domain Model — no drift.

### State

State qualifies an interaction through its **label** — a description of the condition. The interaction's **Examples** (tables) live on the interaction; example and label reference the domain concepts that correspond to those tables.

### Pre-Condition

State that must be present before an interaction starts. What must be true before the interaction. Label only (may use Given/And BDD format). Examples live on the interaction.

### Trigger

Who starts the interaction and what they do.

- **Triggering-Actor** — who starts the interaction
- **Behavior** — the label. Describes the action. Use When/And for steps, Given/When/Then for BDD, or verb-noun as appropriate.
- **Triggering-State** — state that qualifies the interaction (e.g. selecting an option of a certain type). Labels reference domain concepts; examples live on the interaction.

### Response (Then)

Resulting state after an interaction has finished. Who responds and what they do.

- **Responding-Actor** — who responds (typically system, subsystem, or component)
- **Behavior** — the label. Describes the response. Use Given/When/Then for BDD, or verb-noun as appropriate.
- **Resulting-State** — the state that results from the interaction. Labels reference domain concepts; examples live on the interaction.

### Step format

When steps are in scope, specify the format for step text:

- **When/Then** — strict BDD: Trigger as When, Response as Then (e.g. `When **User** browses countries; Then **System** displays list of **Country** options`).
- **Vanilla steps** — verb-noun: short labels (e.g. `User submits form`, `System validates payment`).

These are artificial distinctions — we can say any of these elements. The strategy specifies which mode(s) apply and what is in scope.

### Impact

An interaction may have an **impact**. Impacts apply at any level of the hierarchy. A known result can provide evidence for another impact (tie a hypothesis to a result).

- **Type** — user | economic | feasibility
- **Status** — hypothesis (we don't know yet) | result (measured outcome for an existing system)
- **Description**
- **Evidence-Ref** — optional; links to another impact that is a result

**Example:** Epic "User checks out" has impact hypothesis: "Reduces cart abandonment by 15%." Story "Apply discount code" has result: "In pilot, 12% of users who applied a code completed checkout." The result becomes evidence for the hypothesis.

### Constraints

Any node at any level can have one or more **constraints** — qualitative instructions on how this interaction is shaped. A constraint may be:
- A sentence (inline text)
- A reference to a collection of files that describe the constraint
- Most commonly: a reference to a markdown file

Constraints are inherited from high to low (parent → child). Typically at epic or story level; may appear in steps.

---

<!-- section: story_synthesizer.interaction.inheritance -->
## Interaction Tree Inheritance

Attributes from a parent node are inherited by child nodes. **Brackets indicate inherited values.** Use `[value]` or `[inherited]` so readers see what applies at each level; if the parent changes, update bracketed values in children.

**Inherited attributes:** Examples, actors. Place concepts at the lowest level where they apply to all descendants. Concepts are indicated by `**Concept**` in labels — no separate list.

**Convention:** `Triggering-Actor: [User]`, `Responding-Actor: [System]` — brackets mean "from parent." Unbracketed values are defined on this node. Use Title Case for field names; hyphens for compound terms (e.g. Pre-Condition); no dot notation.

**Guidelines for inherited values:**
- **Statement by level:** Epic statement describes the *scope* of the epic — the broad flows it encompasses — not a single interaction. Use `**Concept**` to ground in domain. Good: (**User** triggers **PaymentType** flows that vary by **Country**; **System** validates and executes per **Country**.) Bad: (**User** selects **Country** and **PaymentType**; **System** validates.) — that describes one story, not an epic. Story statement: one trigger and response. Step statement: When/Then for that step.
- **Pre-Condition:** Never use `Pre-Condition: [inherited]` alone. Always include the label (bracketed) so readers see what applies.
- **Triggering-Actor / Responding-Actor:** Use `[User]` or `[System]` at every trigger/response so the actor is visible without looking up. Use Title Case; no dot notation (e.g. `Triggering-Actor`, not `trigger.actor`).
- **Examples:** Live on the interaction. Use `[inherited]` when tables come from parent; list the qualitative names (e.g. `[Logged In User, Active User Session, User Payment Type Access]`). Include step-specific or story-specific examples unbracketed.
- **Example table names:** When you have data, you need a label. Name by state or condition — "Selected Country", "Selected PaymentType", "Approved Payment" — not generic labels like "Payment" or "Country". For mapping tables use descriptive names (e.g. "Payment Type Field Types"). When data varies by type, include the type (e.g. "PaymentDetails (wire)"). When multiple tables for the same concept appear in one step, add a qualifier in parentheses (e.g. "Selected PaymentType (selected, not available for country)"). When inherited, list those names: `examples: [Logged In User, Active User Session, User Payment Type Access]`.
- **Example scenario column:** Use a scenario column to map example rows to outcomes. Use kebab-case consistently (e.g. success, invalid-payment-details, payment-type-not-available).
- **Example block format:** Use `===` between tables. No blank lines between tables. Tables require a header separator row (`|---|---|`). Pattern: `Name:\n| col1 | col2 |\n|---|---|\n| data | data |\n===\nNext name:\n| table |`.

**Rule:** Put shared concepts at the epic level; only add story-specific concepts at the story level. Epic holds trigger state for rules that apply to all children (e.g. user access to payment types by country). Epics (including epic children of epics) group; they do not add trigger/response state. Stories inherit Pre-Condition, Triggering-Actor, and Responding-Actor from Epic.

**Placement rule:** Only put something at a level if it applies to every descendant. If a failure mode, concept, or rule applies only to specific scenarios or stories, place it on those nodes — not at the Epic.

---

<!-- section: story_synthesizer.interaction.example -->
## Complete Example

A typical reference hierarchy for making a country-specific payment (trigger, make transaction, fulfill). **Concepts** are referenced via `**Concept**` in labels. **Examples** live on the interaction. Pre-Condition, Trigger, and Response qualify through their labels. Epic holds rules that apply to all children (e.g. user access to payment types by country). Epics group; they do not add trigger/response state. Stories inherit from Epic. One story is taken to full detail with scenario and steps. (Other epics and stories not yet filled out.)

**Hierarchy levels:** Epic → Story → Scenario → Step (epics can nest; an epic child of an epic is sometimes called a sub-epic)

**Name and statement:** Active verb language, short name first, statement in brackets (see Interaction).

<!-- section: story_synthesizer.interaction.example.hierarchy -->
### Hierarchy

#### Epic: Make **Country**-specific **PaymentType** (**User** triggers **PaymentType** flows that vary by **Country**; **System** validates and executes per **Country**.)
- Triggering-Actor: User
- Responding-Actor: System
- Pre-Condition: Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)
- Examples:
  Logged In User:
  | scenario   | user_name | user_role   |
  |------------|-----------|-------------|
  | success    | Jane Doe  | Payer       |
  | payment-type-not-available | Jane Doe  | Payer       |
  ===
  Active User Session:
  | scenario   | user_name | session_id | expires_at |
  |------------|-----------|------------|------------|
  | success    | Jane Doe  | sess-001   | 2025-03-08  |
  | payment-type-not-available | Jane Doe  | sess-001   | 2025-03-08  |
  ===
  User Payment Type Access:
  | scenario   | user_name | country_code | country_name  | payment_type   | available |
  |------------|-----------|--------------|---------------|----------------|-----------|
  | success    | Jane Doe  | US          | United States | wire           | yes       |
  | success    | Jane Doe  | MX          | Mexico        | wire           | yes       |
  | payment-type-not-available | Jane Doe  | MX          | Mexico        | ach            | no        |
  ===
  Payment Type Field Types:
  | payment_type | fields |
  |--------------|--------|
  | wire         | amount, currency, beneficiary_id, swift_code |
  | ach          | amount, currency, beneficiary_id, routing_number, account_number |

  #### Story: **User** Triggers **Country**-Specific **PaymentType** (**User** determines **Country** and **PaymentType**; **System** validates and confirms.)
  - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
  - Failure-Modes:
    - validation errors (invalid **PaymentDetails**)
    - payment type not available for **Country** (see **UserPaymentAccess**)
  - Trigger:
    - Triggering-Actor: [User]
    - Behavior: **User** determines **Country** and **PaymentType**
  - Response:
    - Responding-Actor: [System]
    - Behavior: validates **PaymentDetails** and confirms success

<!-- section: story_synthesizer.interaction.example.steps -->
  ##### Scenario: Success — payment validated and confirmed

  ###### Steps

  - Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays list of **Country** options available for **PaymentType**)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: browses countries
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays list of **Country** options available for payment

  - Step 2: Select Country and Display Payment Types (When **User** selects **Country**; Then **System** displays all available **PaymentType** options for that country)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: selects **Country**
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays all available **PaymentType** options for that country
    - Examples:
      Selected Country:

      | scenario | country_code | country_name  |
      |----------|--------------|---------------|
      | success  | US           | United States |

      ===
      PaymentType:

      | scenario | country_code | payment_type |
      |----------|--------------|--------------|
      | success  | US           | wire         |
      | success  | US           | ach         |

  - Step 3: Select Payment Type and Start Payment (When **User** selects **PaymentType** and clicks start payment; Then **System** prepares payment form for that **PaymentType**)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: selects **PaymentType** and clicks start payment
    - Response:
      - Responding-Actor: [System]
      - Behavior: prepares payment form for that type
    - Examples:
      Selected PaymentType:

      | scenario | payment_type |
      |----------|--------------|
      | success  | wire         |

  - Step 4: Display Payment Details Based on Payment Type (When **System** receives payment type selection; Then **System** displays **PaymentDetails** with fields appropriate to the selected **PaymentType**)
    - Trigger:
      - Triggering-Actor: [System]
      - Behavior: receives payment type selection
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays **PaymentDetails** with fields from **PaymentTypeFieldTypes** for the selected **PaymentType**

  - Step 5: Make Payment and Successfully Validate It (When **User** enters valid **PaymentDetails** and submits; Then **System** validates the payment and confirms success)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: enters valid **PaymentDetails** and submits
    - Response:
      - Responding-Actor: [System]
      - Behavior: validates the payment and confirms success
    - Examples:
      PaymentDetails (wire):

      | scenario | payment_type | amount  | currency | beneficiary_id | swift_code |
      |----------|--------------|--------|----------|----------------|------------|
      | success  | wire         | 1000.00 | USD      | ben-001        | SWIFT123   |

  - Step 6: Make Payment and Validation Fails (When **User** enters invalid **PaymentDetails** and submits; Then **System** validates and returns validation errors)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: enters invalid **PaymentDetails** and submits
    - Response:
      - Responding-Actor: [System]
      - Behavior: validates and returns validation errors
    - Examples:
      PaymentDetails (wire):

      | scenario                | payment_type | amount  | currency | beneficiary_id | swift_code |
      |-------------------------|--------------|--------|----------|----------------|------------|
      | invalid-payment-details | wire         | 1000.00 | USD      | invalid-id     | SWIFT123   |

  ##### Scenario: Payment type not available for country

  ###### Steps

  - Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays list of **Country** options available for payment)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: browses countries
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays list of **Country** options available for payment

  - Step 2: Select Country and Attempt Unavailable Payment Type (When **User** selects **Country** where a **PaymentType** is not available; And **User** selects that **PaymentType** and clicks start payment; Then **System** indicates payment type not available for that country)
    - Trigger:
      - Triggering-Actor: [User]
      - Behavior: selects **Country**; then selects **PaymentType** and clicks start payment
    - Response:
      - Responding-Actor: [System]
      - Behavior: indicates payment type not available for that country
    - Examples:
      Selected Country:

      | scenario                   | country_code | country_name |
      |----------------------------|--------------|--------------|
      | payment-type-not-available | MX           | Mexico       |

      ===
      Selected PaymentType (selected, not available for country):

      | scenario                   | payment_type |
      |----------------------------|--------------|
      | payment-type-not-available | ach          |

  #### Epic: Submit **PaymentDetails** for **PaymentType**
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Triggering-Actor: [User]
    - Responding-Actor: [System]

  #### Story: **User** submits **PaymentDetails** for **Country**-specific **PaymentType**
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Triggering-Actor: [User]
    - Responding-Actor: [System]

  #### Epic: Fulfill **Payment** settlement
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Triggering-Actor: [User]
    - Responding-Actor: [System]

  #### Story: **User** completes **Payment** settlement
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Triggering-Actor: [User]
    - Responding-Actor: [System]

---

<!-- section: story_synthesizer.interaction.output -->
## Output Format

**Output path:** `<workspace>/story-synthesizer/interactions/interaction-tree.md`

Format specification for the Interaction Tree output. See the Complete Example above for a full reference.

**Constraints:** Any node can have a `Constraints:` collection — qualitative instructions on how the interaction is shaped. Each constraint may be a sentence, a file path, or (most commonly) a markdown reference. Inherited high to low. Typically at epic or story level; may appear in steps.

<!-- section: story_synthesizer.interaction.output.hierarchy -->
### Epics and Stories View (Hierarchy)

The tree view: Epic → Epic/Story children. Each node shows name, actors, and inherited vs own fields.

**Epic (filled out — has Examples)**
- Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- `- Triggering-Actor:` value
- `- Responding-Actor:` value
- `- Constraints:` collection (sentence, file path, or markdown reference; inherited high to low)
- `- Pre-Condition:` full label (Given/And)
- `- Examples:` state table block (see Example Block Format below)

**Epic (not filled out — inherits only)**
- Heading: `## Epic: <name using **Domain Concepts**> (<statement>)`
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [full inherited label]
- `- Examples:` [list of inherited state table names]
- `- Triggering-Actor:` [User] (or other actor)
- `- Responding-Actor:` [System] (or other actor)

**Story (filled out — has Trigger, Response, Failure-Modes, Scenarios)**
- Heading: `### Story: <name using **Domain Concepts**> (<statement>)` — same pattern as Epic
- `- Pre-Condition:` [inherited]
- `- Failure-Modes:` bullet list (up to 3)
- `- Trigger:` sub-bullets Triggering-Actor, Behavior
- `- Response:` sub-bullets Responding-Actor, Behavior
- `###### Scenario:` name
- `####### Steps`
- Step items (see Story Details View)

**Story (not filled out)**
- Heading: `#### Story:` + **Name**
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [inherited]
- `- Examples:` [inherited table names]
- `- Triggering-Actor:` [inherited]
- `- Responding-Actor:` [inherited]

<!-- section: story_synthesizer.interaction.output.details -->
### Story Details View (Drill-down)

When a story is expanded: Scenarios, Steps, and per-step Trigger/Response/Examples.

**Step (no Examples)**
- `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- `- Constraints:` [inherited] or own (when step-specific)
- `- Trigger:` [inherited], Behavior
- `- Response:` [inherited], Behavior

**Step (with Examples)**
- Same as Step (no Examples), plus `- Examples:` block
- Each table: label, blank line, header row, separator row, data rows
- Each table is a separate block; blank line between tables

**Step (system-triggered)**
- Triggering-Actor overridden to [System] when the step is system-triggered (e.g. "When **System** receives...")

**Example table**
- Always add a qualifier in parentheses: `ConceptName (qualifier):`
- **Scenario column:** Required on entity tables. Use kebab-case (e.g. success, invalid-details, not-available).
- **Inherited examples:** Show as `Examples: [Table Name 1, Table Name 2, ...]` — list names, not tables.

**Epic-level example tables**

Entity table (scenario + fields):

```
  Qualifier Domain Concept:
  | scenario   | field1 | field2   |
  |------------|--------|----------|
  | success    | val1   | val2     |
  | other-case | val1   | val2     |

  AnotherQualifier Domain Concept:
  | scenario   | field1 | field2 | field3 | field4 | field5 |
  |------------|--------|--------|--------|--------|--------|
  | success    | val1   | val2   | val3   | val4   | val5   |
  | other-case | val1   | val2   | val3   | val4   | val5   |
```

<!-- section: story_synthesizer.interaction.output.headings -->
### Heading Levels

| Level | Use |
|-------|-----|
| `#` | Epic |
| `##` | Child Epic (Every level of nesting at a header level) |
| `###` | Story (Assuming only two levels of epic nesting) |
| `####` | Scenario (Assuming only two levels of epic nesting) |
| `#####` | Steps (Assuming only two levels of epic nesting) |

---

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

---

<!-- section: story_synthesizer.context -->
# Context Preparation

Prepared context is a foundational component that must be present before the skill can run. Each step cascades: chunking before evidence extraction, evidence extraction before AI passes.

## Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown using the `abd-context-to-memory` skill before any analysis. **Chunk output goes to `story-synthesizer/context/`** — not alongside the PDF. The source (PDF, etc.) stays where it is; only the processed `.md` chunks move into the skill.

- **Source:** Original content can live anywhere. If no path is set, `context/` at workspace root is the default source.
- **Chunks:** Output of chunking → `<workspace>/story-synthesizer/context/chunks/*.md`
- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "312 sections; Accounts 12–45, Transactions 46–95, Compliance 150–200; chunk types: account definitions, transaction rules, validation policies."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

## Evidence Extraction Pipeline

After chunking, run the evidence extraction pipeline to build structured evidence from the normalized chunks. See `pieces/evidence.md` for the full pipeline specification.

```bash
python scripts/build.py extract_evidence
```

Requires `chunk_index.json` from abd-context-to-memory. Runs scripts 02–07 in sequence:
- Chunk index — from abd-context-to-memory (`index_memory.py` or `index_chunks.py`); mandatory
- `02_extract_terms.py` — noun phrases, defined terms, vocabulary index
- `03_extract_actions.py` — subject-verb-object behavioral facts
- `04_extract_decisions.py` — conditional logic and rules
- `05_extract_variations.py` — behavior axes and mode differences
- `06_extract_states.py` — stateful entities and explicit relationships
- `07_consolidate_evidence.py` — build evidence graph with links, clusters, hotspots

**Output:** `evidence_graph.json` and `evidence_summary.md` in `<workspace>/story-synthesizer/evidence/`.

## Concept Tracking (Optional)

The `concept_tracker.py` tool remains available as a supplementary tool for quick term frequency and co-occurrence analysis. It is not required — the evidence extraction pipeline subsumes its function with richer evidence types.

```bash
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <context_analysis.json> --min-units 5
```

## Variation Analysis

The evidence extraction pipeline captures variations (script 05). For deeper analysis, review the extracted variations and formalize: per mechanism, what's consistent, what differs, what extends with new behavior (→ story) vs adds data to same behavior (→ example).

Variation analysis can be saved to `<workspace>/story-synthesizer/context/context_analysis.json` under each model's `variation` key for use in session strategy.

---

# Process Overview

Your task is to build an **Interaction Tree** and **Domain Model** using a pipeline that separates mechanical evidence extraction (CODE) from analytical reasoning (AI).

The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

---

## The Pipeline (3 Sections)

**Each stage has its own independent checklist.** Kick off the checklist when you start that stage.

```text
1. OVERALL CONTEXT
   Checklist: overall_context_checklist_template.md → overall-context-checklist.md
   - Phase 1: Set Skill Space
   - Phase 2: Prepare Context
   - Phase 3: Extract Evidence
   - Phase 4: Map Concepts
   - Phase 5: Model Discovery and Assessment (on entire concept map and evidence)
   Outputs: chunk_index.json, evidence graph, concept_scan, foundational-model.md, domain-model.md (foundation)

2. SESSION
   Checklist: session_checklist_template.md → <session>/session-checklist.md
   - Phase 6: Create Session
   Outputs: <session>-strategy.md
   **Before starting:** Go to Overall Context and complete anything not done (chunk index, evidence graph, concept scan, OOAD foundation).
   **STOP HERE. Do NOT run slices until user says "run slice", "build it", or "proceed"**

3. SLICE-RUNS
   Checklist: run_checklist_template.md → <session>/runs/run-N-checklist.md (per slice run)
   - Phase 7: Model Generation (builds on foundation)
   - Phase 8: Validate Rules and Scanners
   - Phase 9: Render Diagrams
   - Phase 10: Make Corrections

  At any time during session and slice-run a user may
    - Improve Strategy from Corrections
    - Improve Skill from Corrections
```

---

# 1. Overall Context

Everything that prepares the workspace before any session. Run once per workspace (or when context changes).

**Kick off checklist:** Run `python scripts/create-checklist.py overall` when starting this stage. This checklist is independent of Session and Slice-Runs.

**CRITICAL:** Create checklist when starting: `create-checklist [overall|session|run]`. Update when step completes: `create-checklist update <path> --step N` or edit the file. A change is not tracked until the checklist is updated.

---

## Phase 1: Set Skill Space


| Human                                          | AI / Script                                 | AI                              | Human → AI                    |
| ---------------------------------------------- | ------------------------------------------- | ------------------------------- | ----------------------------- |
| Says "set skill space to X" or "new workspace" | Runs `build.py get_config`, validates paths | Reports paths; checks readiness | Confirms or provides new path |


Configure the skill space path in `abd-story-synthesizer/conf/abd-config.json` and the context paths in `<skill-space>/conf/abd-config.json`.

```bash
python scripts/build.py get_config
```

---

## Phase 2: Prepare Context


| Human                                          | AI / Script                      | AI                                | Human → AI       |
| ---------------------------------------------- | -------------------------------- | --------------------------------- | ---------------- |
| Says "prepare context" or provides source docs | Chunks documents, indexes chunks | Reports chunk count and readiness | Confirms sources |


Chunk source documents and build chunk index using the `abd-context-to-memory` skill. **Chunk index creation is mandatory** — run `index_memory.py` or `index_chunks.py` from that skill.

**DO NOT use `index_chunks.py` when source has PDF/PPTX/DOCX.** Use `index_memory.py` — it converts, chunks, and indexes. `index_chunks.py` only indexes existing chunks; it does not create them.

```bash
# From abd-context-to-memory skill:
python index_memory.py --path <context_folder>
# or, when chunks already exist:
python index_chunks.py --context-path <chunk_folder> [--output <path>]
```

Output: `<workspace>/story-synthesizer/context/chunk_index.json`

---

## Phase 3: Extract Evidence


| Human                   | AI / Script                              | AI                                   | Human → AI      |
| ----------------------- | ---------------------------------------- | ------------------------------------ | --------------- |
| Says "extract evidence" | Runs extraction pipeline (scripts 02–07) | Reports evidence counts and hotspots | Reviews summary |


Run the evidence extraction pipeline. Scripts extract structured evidence from normalized chunks — terms, actions, decisions, variations, states, relationships — then consolidate into an evidence graph.

```bash
python scripts/build.py extract_evidence
```

Requires `chunk_index.json` from abd-context-to-memory. Runs scripts 02–07 in sequence:

- `02_extract_terms.py` — noun phrases, vocabulary index
- `03_extract_actions.py` — subject-verb-object behavioral facts
- `04_extract_decisions.py` — conditional logic and rules
- `05_extract_variations.py` — behavior axes and mode differences
- `06_extract_states.py` — stateful entities and explicit relationships
- `07_consolidate_evidence.py` — build evidence graph with links, clusters, hotspots

Output: `evidence_graph.json` and `evidence_summary.md` in `<workspace>/story-synthesizer/evidence/`. See `pieces/evidence.md` for full specification.

---

## Phase 4: Map Concepts


| Human                                 | AI / Script                             | AI                      | Human → AI          |
| ------------------------------------- | --------------------------------------- | ----------------------- | ------------------- |
| Says "map concepts" or "concept scan" | Invokes `get_instructions concept_scan` | Produces conceptual map | Reviews and adjusts |


AI concept scan on normalized context. Discovers core primitives, interaction phases, authority boundaries, variation axes, rule mechanisms, and implicit concepts. Orients later AI passes (model discovery, validation).

```bash
python scripts/build.py get_instructions concept_scan
```

Output: `<workspace>/story-synthesizer/concept_scan.md`. See `pieces/concept_scan.md` for full specification.

---

## Phase 5: Model Discovery and Assessment


| Human                                 | AI / Script                                      | AI                                                       | Human → AI          |
| ------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- | ------------------- |
| Says "model discovery" or "OOAD"      | Invokes `model_discovery` and `model_validation` | Produces OOAD analysis and validated domain model foundation | Reviews and adjusts |


**Runs on the entire concept map and evidence** — not per slice. Produces a foundational domain model that slice runs build on. Do this once per workspace (or when context changes).

### Model Discovery (OOAD)

**Behavior packet adequacy:** Packets must specify enough structure to build the model — concepts, flow (who creates what, who receives), and any mapping/composition rules the domain needs. Do not use a minimal one-liner.

1. **Behavior packet detection** — cluster evidence into coherent mechanisms
2. **Mechanism synthesis** — find real structural seams from packets
3. **Decision ownership** — assign each decision to the concept that should own it
4. **Object candidate formation** — derive candidates from owned behavior and state
5. **Relationship & boundary modeling** — define relationships based on behavior
6. **Inheritance test** — verify substitutability and shared protocol; propose base when concepts share acquisition/validation protocol

```bash
python scripts/build.py get_instructions model_discovery
```

**Persist the OOAD analysis** to `<workspace>/story-synthesizer/foundational-model.md`.

### Model Assessment (Validation)

**Verify behavior packets are adequate.** If packets are minimal, reject and redo discovery. **Persist the full assessment** to foundational-model.md. A one-line note is insufficient.

1. **Scenario / message walkthrough** — verify the model can actually behave
2. **Anemia / centralization critique** — find data bags, fake inheritance, misplaced behavior
3. **Base and inheritance check** — find concepts that share protocol and should extend a common base
4. **Final domain model foundation** — produce only after passes stabilize

```bash
python scripts/build.py get_instructions model_validation
```

Output: `<workspace>/story-synthesizer/foundational-model.md` and `<workspace>/story-synthesizer/domain/domain-model.md` (foundation). Slice runs extend this foundation.

---

# 2. Session

Create and configure a session. One session per analysis focus (discovery / exploration / specification). Defines level of detail, scope, and slices. **Do not run any slice here.**

**Kick off checklist:** Run `python scripts/create-checklist.py session <name>` when starting this stage. This checklist is independent of Overall Context and Slice-Runs.

---

## Phase 6: Create Session


| Human                                    | AI / Script           | AI                            | Human → AI          |
| ---------------------------------------- | --------------------- | ----------------------------- | ------------------- |
| Says "start session" or "create session" | Runs `create_session` | Strategy file created on disk | Updates and adjusts |


Create, open, or continue an existing session. The session defines: Level of Detail (discovery/exploration/specification), Scope, and Slices. The evidence graph, concept scan, and OOAD foundation are already available.

**CRITICAL: Phase 6 creates the strategy file only. Do NOT run any slice.** The user must explicitly say "run slice", "build it", or "proceed" before Phase 7 (Model Generation).

**After creating strategy:** Run `get_instructions validate_session --strategy <path>` and validate slices against slice rules before running any slice.

**When the user corrects strategy, slices, or scope during session creation:** Apply the fix and record the correction in `runs/run-0.md`. See `pieces/runs.md` § When User Gives a Correction. A change is not complete until the correction is recorded.

See `pieces/session.md` for session content, slice design, and tag definitions.

```bash
python scripts/build.py create_session [session_name]
```

Output: `<workspace>/story-synthesizer/<session-name>/<session-name>-strategy.md`

---

# 3. Slice-Runs

Execute one run per slice. Phases 7–10: Model Generation → Validate Rules and Scanners → Render Diagrams → Make Corrections. Each slice run builds on the OOAD foundation from Stage 1. At any time: Improve Strategy or Improve Skill from corrections.

**Kick off checklist:** Run `python scripts/create-checklist.py run <session> <n>` at the start of each slice run. This checklist is independent per run.

---

## Phase 7: Model Generation


| Human                         | AI / Script                          | AI                                                 | Human → AI          |
| ----------------------------- | ------------------------------------ | -------------------------------------------------- | ------------------- |
| Says "run slice", "build it", "proceed" | Invokes `get_instructions run_slice` | Produces interaction tree + domain model for slice | Reviews and adjusts |


**Builds on the OOAD foundation** from Stage 1 (Phase 5). The foundation (foundational-model.md, domain-model.md) provides mechanisms, ownership, and validated concepts. Slice runs produce the interaction tree and domain model extensions for that slice's scope.

Produce the interaction tree and domain model for the slice. Domain concepts from the foundation sync into the interaction tree via `**Concept**` references.

```bash
python scripts/build.py get_instructions run_slice
```

---

## Phase 8: Validate Rules and Scanners


| Human         | AI / Script              | AI                 | Human → AI                   |
| ------------- | ------------------------ | ------------------ | ---------------------------- |
| After Phase 7 | Runs `build.py validate` | Reports violations | Fixes and re-runs until pass |


Run rule scanners. Fix any violations before marking the run complete. See `pieces/validation.md`.

```bash
python scripts/build.py validate
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions validate_slice
```

---

## Phase 9: Render Diagrams


| Human               | AI / Script           | AI               | Human → AI |
| ------------------- | --------------------- | ---------------- | ---------- |
| After model changes | Updates class diagram | Renders diagrams | Reviews    |


Update class diagram for domain model changes. See `pieces/diagrams.md`.

---

## Phase 10: Make Corrections


| Human                                | AI / Script                            | AI                             | Human → AI          |
| ------------------------------------ | -------------------------------------- | ------------------------------ | ------------------- |
| Reviews output and gives corrections | Invokes `get_instructions correct_run` | Applies corrections to run log | Updates and adjusts |


See `pieces/runs.md` for corrections format and `pieces/correct.md` for the correction layers.

```bash
python scripts/build.py get_instructions correct_run
python scripts/build.py get_instructions correct_all
```

---

## Improve Strategy / Improve Skill (at any time)


| Human                                        | AI / Script                                 | AI                                          | Human → AI          |
| -------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------- |
| Reviews corrections, decides what to promote | Invokes `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts |


**At any time during session and slice-run** a user may Improve Strategy from Corrections or Improve Skill from Corrections. See `pieces/correct.md` for the three layers (run → session → skill).

```bash
python scripts/build.py get_instructions improve_strategy
```

---

## Slice-Run Checklist

**Independent checklist per slice run.** Run `python scripts/create-checklist.py run <session> <n>` at the start of each run. Tick each item when done.


| #    | Phase   | Step                                                              | Done |
| ---- | ------- | ----------------------------------------------------------------- | ---- |
| 1    | Phase 7 | Model Generation — produce interaction tree + domain model for slice (builds on OOAD foundation) | ☐    |
| 2    | Phase 8 | Validate Rules and Scanners — `build.py validate`; fix violations | ☐    |
| 3    | Phase 9 | Render Diagrams — update class diagram                            | ☐    |


Phase 10 (Make Corrections) and Improve Strategy / Improve Skill are recorded as needed. See `pieces/run_checklist_template.md` for the full checklist.

---

## Process Checklist

Each stage has an independent checklist. Kick off the checklist when starting that stage.

**1. Overall Context** — `overall-context-checklist.md`

- Phase 1: Skill space set
- Phase 2: Context prepared (chunk_index.json)
- Phase 3: Evidence extracted (evidence_graph.json)
- Phase 4: Concepts mapped (concept_scan.md)
- Phase 5: Model Discovery and Assessment (foundational-model.md, domain-model.md)

**2. Session** — `<session>/session-checklist.md`

- Phase 6: Session created (`<session>-strategy.md`)

**3. Slice-Runs** — `<session>/runs/run-N-checklist.md` (per run)

- Phase 7: Model Generation
- Phase 8: Validate Rules and Scanners
- Phase 9: Render Diagrams
- Phase 10: Make Corrections
- Improve Strategy / Improve Skill — at any time from corrections

---

# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, and slices. Context must be prepared before starting a session (see `pieces/context.md`). One run per slice; runs write logs.

**Session location:** `<workspace>/story-synthesizer/<session-name>/`. Strategy: `<session-name>-strategy.md`. Runs: `runs/run-N.md`, `runs/run-N-validation.md`, `runs/run-N-checklist.md`. OOAD foundation is produced in Stage 1 (Phase 5) at workspace level: `story-synthesizer/foundational-model.md`, `domain/domain-model.md`.

## Session Naming

When the user says "run a session called X" (e.g. "run a session called discovery") and does **not** provide a custom name, name the session `X<unique number>` so it does not collide with existing sessions. Examples: `discovery1`, `discovery2`, `exploration1`. If the user specifies a name (e.g. "run a session called my-campaign-discovery"), use that name instead.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes. Each session type defines what a run produces.


| Session Type      | What runs produce                                                                                                                                                                                             | Artifacts                                | Tags                                                                       | Slice size                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Story-Map (Epic/story hierarchy; short names only) as first cut of the **interaction tree.** Foundational object model portion of the **domain model** (typed state: properties, operations, collaborators). | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `discovery`, `story_map`, `epic`, `story`, `domain`                        | Large — one or more, foundational model or cross-cutting concern per slice, all the way thin slice of multiple concepts end to end |
| **Exploration**   | Full story fields: Trigger, Response, Pre-Condition, Triggering-State, Resulting-State, domain concepts, Failure-Modes, Constraints. Steps below stories. Completes domain model.                             | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `exploration`, `story_map`, `epic`, `story`, `domain`, `step`              | Medium — a group of related stories that share state or workflow                                                                    |
| **Specification** | Steps grouped into scenarios. Examples (tables per concept). Failure-Modes.                                                                                                                                   | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `specification`, `step`, `step_edge_case`, `scenario`, `example`, `domain` | Small — individual stories or story pairs with shared scenarios                                                                     |


**Default when no session:** `tags: [discovery, story_map, epic, story, domain]`.

### 2 - Scope

What portion of the analyzed context this session works with. Context must already be prepared (see `pieces/context.md`).

- **All** (default) — entire analyzed context
- **Subset** — specific context categories (e.g., "Payments module only", "User Registration + Authentication")

If no scope is set, ask the user. The AI can suggest scope based on the context analysis (concept report, variation analysis). Default is "all."

**Context readiness check:** Before setting scope, verify context is prepared (chunked, scanned, deep-read, variation analysis). If context is missing or stale, ask the user to prepare it first (see `pieces/context.md`).

### 3 - Slices

Slices define the order of work. Each slice scopes one run. Slice design depends on session type.

**Apply slice rules** when designing slices. Run `get_instructions create_strategy` to load rules. After creating strategy, run `get_instructions validate_session --strategy <path>` to validate slices against slice rules.

**Epics from context (not slices):** Do not name epics after slices. Epics and sub-epics come from the larger context (goal, domain, concept map, evidence). Place slice stories under appropriate sub-epics. See [interaction-epics-from-context](../rules/interaction-epics-from-context.md).

**DO NOT slice by epic.** Each slice must end to end lfe cycle of  a user, product, service or oter aspect of the user-solution journey

#### Discovery Slices

Discovery slices (slices focused on building the story-map) are **big** — scoped to a cross-cutting concern or foundational model from `context_analysis.json`. The variation analysis already identifies the models and their categories; each slice covers one model (or related group of models) and produces all the epics and stories that touch it.

**Slicing by foundational model:** Each model from context analysis becomes a candidate slice. Related models that share state (e.g., Resolution System used by Combat) may be grouped or ordered by dependency.

**Slice checklist:**

- Does the slice cover a complete foundational model or cross-cutting concern?
- Are state dependencies respected (creators before consumers)?
- Is the slice big enough to be coherent but small enough to review?

#### Exploration Slices

Exploration slices can reuse discovery slices or define new ones scoped to a smaller collection of stories that need details  added.

#### Specification Slices

Specification slices often scope to a couple of stories that need scenarios, examples, and failure modes.

### 4 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.

**During session creation (before any slice runs):** When the user corrects strategy, slices, or scope, apply the fix and record the correction in `runs/run-0.md`. See `pieces/runs.md` § When User Gives a Correction.

What each run produces is defined by the session's level of detail (see § 1). A session has one run type — all runs in a session produce the same kind of output.

---

<!-- section: story_synthesizer.runs -->
# Runs

During a session you synthesize the scope of a slice through a run. **One run per slice.** Run 1 = slice 1, run 2 = slice 2, etc. A run captures what happened, what changed, when it changed. The session defines level of detail; the slice defines scope for the run.

**Epics from context (not slices):** Do not name epics after slices. Epics and sub-epics come from the larger context (goal, domain, concept map, evidence). Place slice stories under appropriate sub-epics. See [interaction-epics-from-context](../rules/interaction-epics-from-context.md).

**Going deeper on the same slice** (e.g. adding steps to discovered stories) is a **new session** with a different focus, not another run.

Each run writes a **run log** to its own file under the session's runs folder. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md` (N = run number). Configurable via skill-space config.

## Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the session's level of detail (e.g. 4–7 stories if stopping at stories; epics only if stopping at sub-epics). Write the run log. Render domain model changes to class diagram (see `pieces/diagrams.md`). User reviews.
2. **Corrections → run log** — When a mistake is found, add a DO or DO NOT to the run log's Corrections section (see Corrections Format below). Re-run the slice; update the run log and diagram; repeat until approved.
3. **Next slice** — Proceed to the next slice. Apply corrections from previous runs. Same pattern: produce → render diagram → review → corrections → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the session and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

## Run Log Structure

```
# Run N

## Scope
The slice for this run. At least node names (epics, stories) in scope. E.g.:
- Epic: User checks out
- Story: Apply discount code
- Story: Select payment method

## Before
What we had at the start (e.g., raw context, stories, steps). Summary or snippet.

## After
What we had afterwards (e.g., context → stories, stories → steps). Summary or snippet.

## Corrections
The DOs and DON'Ts added during this run. Each time the user finds a mistake, add a new correction here (do not add to session file directly). Each correction includes:
- The rule
- Example (wrong)
- Example (correct)
```

Run logs are used to track progress, feed into agents, analyze patterns, or refine the session strategy. The post-synthesis review promotes reusable corrections from run logs to the session or skill rules.

<!-- section: story_synthesizer.runs.corrections -->
## Corrections Format

When adding corrections to the run log (Corrections section), each **DO** or **DO NOT** must include:

- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the slice until the user approves. Corrections stay in the run log; the post-synthesis review promotes reusable ones to the session or skill rules.

## When User Gives a Correction

**Trigger phrases:** "wrong", "correction", "this is wrong", "strategy is wrong", "too superficial", "fix this", "redo", "try again"

**You MUST:**

1. **Apply the correction** — Refine session strategy, update output files, or re-run with corrections as input.
2. **Add to run log** — Create or append to the appropriate run log. Format:
  - **DO** or **DO NOT:** [the rule]
  - **Example (wrong):** [what was done incorrectly]
  - **Example (correct):** [what it should be]
3. **Proactively confirm** — Say: "I've added this to the run log. Correction: [brief summary]. I've applied it."

**A change is not complete until the correction is recorded.** Making the fix without recording the correction means the pattern is lost — it won't carry forward to future runs or sessions. Both the fix AND the correction are required.

**Which run log:**
- **During session creation (before any runs):** Use `runs/run-0.md`. Session creation is iterative — the user will correct strategy, variation analysis, and first-cut output files. All corrections go in `run-0.md`. These corrections feed into run 1.
- **During a run:** Use `runs/run-N.md` (N = current run number).

## Checking for Missed Corrections

Run `python scripts/build.py get_instructions correct_run` to review the chat for unrecorded corrections. Use `correct_session` to incorporate corrections into the session strategy. Use `correct_skill` to promote corrections to skill rules. Use `correct_all` to run all three in sequence. The `run_slice` operation reminds you to check before proceeding.

<!-- section: story_synthesizer.runs.patterns -->
## Patterns (from Runs)

**Strategy is upfront; runs can extend it.** After each run, examine all runs for new patterns. If found, add to the session's Patterns section.


| Run   | What was built                                               | Pattern found             | Applicable to               |
| ----- | ------------------------------------------------------------ | ------------------------- | --------------------------- |
| run-1 | e.g. "wrote steps and examples for all stories under epic X" | Brief pattern description | Scope where pattern applies |


**Example:** Run 2 built steps and examples for "Configure Power Effect" stories. Pattern: "Effect-type stories share same step structure — Configure, Validate, Apply." Applicable to: other effect types under the same epic.

---

<!-- section: story_synthesizer.diagrams -->
# Class Diagrams

When a run produces or modifies domain model concepts, render the changes to a DrawIO class diagram. One page per foundational model. The diagram is the visual representation of `domain-model.md` — they stay in sync.

## Diagram File

**Path:** `<session>/class diagram.drawio` (alongside `domain-model.md`)

Each foundational model section in `domain-model.md` maps to one page in the diagram. Page names must match section names exactly (e.g., "Resolution System", "Combat System").

## When to Render

- **After producing domain model output** in a run — render new/changed concepts to the diagram
- **After corrections that change domain model** — update the diagram to match
- **After user edits the diagram in DrawIO** — sync back to `domain-model.md` using `sync-to-model`

## Tools

All tools are in `scripts/` in the synthesizer skill. Run from that directory.

```bash
cd skills/abd-story-synthesizer/scripts
python drawio_class_cli.py <command> <drawio-file> [options]
```

### Diagram Management

| Command | Usage |
|---------|-------|
| `init` | `init <file> --page <name>` — create file or add page |
| `inspect` | `inspect <file> [--page <name>]` — JSON: classes, edges, overlaps |
| `sync-to-model` | `sync-to-model <file> [--page <name>] [--model <md-path>]` — sync diagram classes back to domain-model.md with diffs |

### Class CRUD

| Command | Usage |
|---------|-------|
| `add-class` | `add-class <file> --page <page> --name <Name> [--base <Base>] [--props "p1\|p2"] [--ops "o1\|o2"] [--invs "i1\|i2"] [--x N] [--y N]` |
| `update-class` | `update-class <file> --page <page> --name <Name> --add-prop "..." \| --remove-prop "..." \| --add-op "..." \| --remove-op "..." \| --add-inv "..." \| --set-base <Base>` |
| `delete-class` | `delete-class <file> --page <page> --name <Name>` — removes class and all its edges |
| `move` | `move <file> --page <page> --name <Name> --x N --y N` |

### Relationship CRUD

| Command | Style | Usage |
|---------|-------|-------|
| `add-inheritance` | Hollow triangle (straight) | `--child <Child> --parent <Parent>` |
| `add-composition` | Filled diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-aggregation` | Hollow diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-association` | Open arrow (orthogonal) | `--from <Source> --to <Target> [--straight]` |
| `add-dependency` | Dashed open arrow (straight) | `--from <Source> --to <Target> [--label <text>]` |
| `delete-edge` | — | `--from <Source> --to <Target>` |

## Layout Guidelines

- **Inheritance:** Base on top, extensions below. Straight vertical lines preferred.
- **Composition/aggregation:** Orthogonal routing (right-angle corners). Diamond on the owner (parent) side.
- **Association:** Orthogonal routing. Use `--straight` when classes are on the same row to avoid bends.
- **Dependency:** Dashed straight line for creates/uses relationships (e.g., Rollable creates Check).
- **Grid layout:** Position classes in rows — parents row 0, children/dependents row 1+. Avoid all-on-one-row; aim for a square diagram.
- **No overlaps:** After positioning, run `inspect` to check for overlapping classes. Use `move` to fix.
- **No crossing edges:** Position classes so edges don't cross over other classes. Place related classes adjacent.

## UML Relationship Selection

| Relationship | When to use | DrawIO style |
|-------------|-------------|--------------|
| **Inheritance** | Concept extends another (e.g., Ability : Rollable) | Hollow triangle |
| **Composition** | Part cannot exist without whole; collection property (e.g., Character ◆→ Ability via Dictionary) | Filled diamond |
| **Aggregation** | Whole references part but part has independent lifecycle (e.g., Character ◇→ PowerLevel) | Hollow diamond |
| **Association** | Concept uses another in operations (e.g., Check → DC, Check → Degree) | Open arrow |
| **Dependency** | Concept creates instances of another (e.g., Rollable --creates-→ Check) | Dashed arrow |

## Cross-Model Imports

When a concept from one foundational model is referenced in another (e.g., Ability extends Rollable from Resolution System), mark it explicitly in both places.

### Domain Model Convention

Add `[from: Source Module]` after the base class:

```
**Ability** : Rollable [from: Resolution System]
**AttackCheck** : Check [from: Resolution System]
```

### Class Diagram Convention

Add the imported class using `--imported-from`:

```bash
python drawio_class_cli.py add-class <file> --page "Character Trait System" --name Rollable --imported-from "Resolution System" --props "Number modifier" --x 40 --y 620
```

The imported class renders with a dashed border and a `«from: Module»` stereotype label above the name. Add inheritance edges from local classes to the import as normal.

### Keeping Cross-Model References in Sync

When a concept changes in its home model:
1. Update the concept in the home model's page and domain-model.md section
2. Update imported copies in other pages (properties may differ — imports typically show only the key properties)
3. Run `inspect` on pages that import the concept to verify edges still connect

**Imported classes are lightweight copies** — they show the concept name, stereotype, and key properties only. They don't need full operations or invariants (those live in the home model).

## Domain Model Type Conventions

- **Enum types** for constrained options: `EnumType name {value1, value2, ...}` — not `String name (option1/option2)`
- **Derived properties** with invariants: `Number cost` + `Invariant: cost = rank × 2` — not `calculate_cost() → Number`
- **Invariants** for all rules, formulas, and constraints — not embedded in property descriptions or operation signatures

## Class Diagram Rules

Rules tagged `class_diagram` in `rules/` govern diagram rendering conventions. These are injected when using the class diagram CLI tool — they are NOT part of synthesis run instructions. Apply them during the rendering workflow below.

Key rules:
- **Hierarchy flow** — base classes top, children below (`domain-ooa-diagram-hierarchy-flow.md`)
- **Cross-model imports** — import base classes that establish ancestry context (`domain-ooa-diagram-cross-model-imports.md`)
- **Edge routing** — explicit exit/entry points when multiple edges share a source (`domain-ooa-diagram-edge-routing.md`)

## AI Workflow for Rendering

After producing domain model output for a slice:

1. **Review `class_diagram` rules** — apply positioning and edge conventions from `rules/domain-ooa-diagram-*.md`
2. **Init** page if needed: `init <file> --page "<Model Name>"`
3. **Add classes** with properties, operations, invariants at planned grid positions (base classes top, children below)
4. **Add edges** — inheritance first (defines vertical structure), then composition/aggregation, then associations/dependencies. Use explicit exitX/exitY/entryX/entryY when multiple edges leave the same class.
5. **Inspect** to check for overlaps and edge routing
6. **Move** any classes that overlap or cause edge crossings
7. **Verify** sync: `sync-to-model` should report "no changes" (diagram matches model)

When user edits the diagram in DrawIO:

1. User saves the diagram
2. Run `sync-to-model` to see diffs and apply changes back to `domain-model.md`

---

<!-- section: story_synthesizer.correct.run -->
# Correct Run

Review this chat for changes made to session files that are not recorded as corrections in the current run log.

**For each change you made during this session:**

1. Was it a user-requested fix, restructuring, or improvement? (Skip trivial changes: typo fixes, formatting, count updates that follow from other changes)
2. Does a corresponding DO or DO NOT correction exist in the run log?
3. If not — propose the correction to the user before writing it.

**For each candidate correction, present to the user:**

- **Change:** Brief description of what was changed
- **Proposed correction:** The DO or DO NOT rule
- **Record this?** (yes / skip)

Only skip trivial changes (formatting, typos, mechanical count updates). Everything else is a candidate — changes that reflect a pattern about how to structure stories, domain models, scaffolds, variation analysis, or the process itself.

**Write corrections in domain-neutral language.** Corrections must apply across any domain — payments, retail, games, healthcare, whatever. Use terms like "business rules", "workflow", "validation", "data variants", "cross-cutting concepts" — not the current skill space's domain terms. The examples can reference the current domain to illustrate, but the rule itself must be generic.

**After review, write approved corrections to the run log** using the standard format:
- **DO** or **DO NOT:** [the rule]
- **Example (wrong):** [what was done incorrectly]
- **Example (correct):** [what it should be]

<!-- section: story_synthesizer.correct.session -->
# Correct Session

Review the corrections in the current run log and determine which should be incorporated into the session strategy.

**For each correction in the run log:**

1. Does this correction affect how the session's variation analysis, slices, or scaffold should be structured?
2. Is it specific to this session's context (not a universal rule)?
3. If yes to both — propose incorporating it into the session strategy.

**For each candidate, present to the user:**

- **Correction:** The DO or DO NOT from the run log
- **Strategy impact:** What would change in the session file (variation analysis section, slice scope, scaffold structure)
- **Proposed change:** The specific edit to the session file
- **Apply this?** (yes / skip)

Be aggressive in suggestions. If a correction reveals a pattern that should change the variation analysis, slice ordering, or scaffold structure — propose it. Don't wait for the user to ask.

**After review, apply approved changes to the session file** and note in the run log which corrections were incorporated into strategy.

<!-- section: story_synthesizer.correct.skill -->
# Correct Skill

Review the corrections in the current run log and determine which should be promoted to the skill's rules or process pieces.

**For each correction in the run log:**

1. Is this correction reusable across projects — not specific to this session's domain?
2. Does an existing skill rule already cover it? (If so, does the rule need strengthening?)
3. If reusable and not covered — propose promoting it to a new or existing rule.

**For each candidate, present to the user:**

- **Correction:** The DO or DO NOT from the run log
- **Target:** New rule, strengthen existing rule, or update process piece
- **Target file:** The specific file path (e.g. `rules/interaction-data-vs-logic-story-split.md`)
- **Proposed change:** What to add or modify
- **Promote this?** (yes / skip)

Be aggressive in suggestions. If a correction applies beyond this project's domain, it belongs in the skill. Don't hold back — propose the change, let the user decide.

**After review, apply approved changes to the skill** and record in the run log's "Promoted to Skill" table:

| Correction | Target file | Change |
|-----------|-------------|--------|

Then rebuild AGENTS.md: `python scripts/build.py`

---

<!-- section: story_synthesizer.validation.checklist -->
# Validation Checklist

Verify against output format in `pieces/interaction.md` § Output Format and `pieces/domain.md` § Output Format. Run `build.py validate` — see `pieces/process.md` Phase 4.

**Scanner mode:** With NLTK (grammar) or mistune (AST) installed, scanner mode is **full**. Without them, the scanner runs in **nerfed** mode (regex-only checks). The validate command prints `Scanner mode: full` or `Scanner mode: nerfed` at startup. Violations are reported as (rule_id, message, location, snippet); exit code is always 0.

**AI behavior:** In a **build phase** (run_slice, validate_run, validate_slice): report violations and fix them before marking complete. On **explicit validate** (user says "validate" outside a build phase): report violations only — do not fix. Do not edit files unless in a build phase.

**Strategy alignment:** Nodes include fields for the current mode (Discovery, Exploration, Specification). Do not require fields out of scope.

---

## Interaction Tree

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Triggering-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state
- [ ] Examples: state table block or `Examples: [Table Name 1, ...]` when inherited

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Trigger, Response present
- [ ] Trigger: sub-bullets Triggering-Actor, Behavior (no state language in Behavior)
- [ ] Response: sub-bullets Responding-Actor, Behavior (no action language in outcome)
- [ ] Scenario and Steps when in scope

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Trigger and Response with [inherited] when from parent
- [ ] System-triggered steps override Triggering-Actor to [System]

**Example tables**
- [ ] Qualifier in parentheses: `ConceptName (qualifier):`
- [ ] Scenario column required on entity tables; kebab-case (e.g. success, invalid-details)
- [ ] Each table: label, blank line, header row, separator row, data rows

**Hierarchy and order**
- [ ] Epic → Epic/Story → Scenario → Step (epics can nest)
- [ ] Required state creators appear before consumers; tree follows actual flow
- [ ] Each node touches at least one domain concept via `**Concept**` in labels

---

## Domain Model

**Concept**
- [ ] Format: `Concept : <Base Concept if any>`
- [ ] Properties, operations, collaborating concepts listed
- [ ] `examples:` list of domain concept tables from interaction tree
- [ ] Each concept referenced via `**Concept**` in interaction tree must exist here
- [ ] Concepts scoped to Epic/Story that owns it (lowest common ancestor of all interactions that use it)
- [ ] Stories rarely define domain concepts — they inherit from epic
- [ ] Invariants under specific property/operation when they apply to that property/operation only

---

## Failure Modes

- [ ] Max 3 per interaction
- [ ] From domain rules, state conditions, or authorization only (no infrastructure or technical failures)

---

## Content

- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level
- [ ] Assumptions stated when unclear (no invented mechanics)
- [ ] **Granularity:** Sufficient stories to capture rule detail; no collapsing of large sections into single stories

---

## Corrections Format

When adding corrections to the run log, use this format:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix

If failing on the same guidance again, add an extra example to the existing DO/DO NOT block.

---
