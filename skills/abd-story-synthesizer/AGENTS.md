<!-- section: story_synthesizer.introduction -->
# Introduction

The story synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

The story skill **synthesizes** source material into an **Interaction Tree** and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. Outputs: story map, domain model, acceptance criteria, specifications.

In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Synthesis can stop at the story level; details are flushed out later.

**Interaction Tree:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). Epics group stories; the story is the backbone — the smallest unit that is both valuable and independently deliverable. Each epic and story can have Pre-Condition, Trigger, and Response. Scenarios optionally group steps; steps are atomic interactions.

**Domain Model:** Domain Models describe the state found in Pre-Condition, Trigger, and Response. **Domain Concepts** (the things that hold state and get operated on) are referenced via `**Concept**` in the name/labels of Interaction tree elements (e.g. Make `**Country**`-specific `**Payment**`). Interaction Tree and Domain Model evolve together — no drift.

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

---

<!-- section: story_synthesizer.process -->
# Process Overview

Your task is to **synthesize** context into an **Interaction Tree** and **Domain Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them.

See `pieces/interaction.md` for the Interaction Tree data model. 

See `pieces/domain.md` for the Domain Model data model.

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

---

## Phase 1: Set Work Area


| Human                                           | AI / Script                | AI                                           | Human → AI                    |
| ----------------------------------------------- | -------------------------- | -------------------------------------------- | ----------------------------- |
| Says "set path", "new workspace", or "continue" | Runs `build.py get_config` | Reports current paths; sets new if requested | Confirms or provides new path |


Before starting or continuing work, establish where output goes. **New work:** set `skill_space_path` to point to the workspace. **Continue existing work:** get the current path and verify.

**Set path for new work area:** Edit `conf/abd-config.json` and set `"skill_space_path": "/path/to/workspace"` (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/`.

**Get path to continue:** Run `get_config` to see where the skill is currently pointed.

**Script:**

```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_config
```

**Output:** JSON with `engine_root`, `skill_space_path` (and `skill_path` as shorthand), `config_path`, and optionally `strategy_path`, `context_paths`. The script returns resolved paths from `conf/abd-config.json`.

---

## Phase 2: Start Session


| Human                                        | AI / Script                                       | AI                                             | Human → AI                                 |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| Says "start a session" or "create a session" | Invokes script `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts → incorporates changes |


Create, open, or continue an existing session. Name it (user-provided or AI-derived from context). The session file stores strategy: Level of Detail, Scope, Variation Analysis, and slices. Option: carry slices over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

**Session path:** `<skill-space>/story-synthesizer/sessions/<session-name>.md`

The session/strategy declares **tags in scope** (e.g. `discovery`, `interaction_tree`, `stories`, `domain`, `steps`). The engine filters rules by tags. See `pieces/session.md` for session content, slices, discriminators, and tag definitions.

**Script:**

```bash
python scripts/build.py get_instructions create_strategy
```

---

## Phase 3: Execute a Run


| Human                                                             | AI / Script                                 | AI                                | Human → AI                                 |
| ----------------------------------------------------------------- | ------------------------------------------- | --------------------------------- | ------------------------------------------ |
| Says "proceed," "build it," "run slice", "next run", "next slice" | Invokes script `get_instructions run_slice` | Produces run output for the slice | Updates and adjusts → incorporates changes |


Slices are completed through a run. One run per slice. A run may require multiple iterations (user reviews → corrections to run log → re-run) until approved. Corrections carry forward: run 2 applies corrections from run 1; run 3 applies corrections from runs 1 and 2.

**Output path:** `<skill-space>/story-synthesizer/` — Interaction Tree and Domain Model (format in `output/interaction-tree-output.md` and `output/domain-model-output.md`). **Run logs:** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md`

See `pieces/session.md` for slices. See `pieces/runs.md` for run lifecycle, run log structure, and corrections format.

**Script:**

```bash
python scripts/build.py get_instructions run_slice [--strategy path/to/strategy.md]
```

**You MUST call `get_instructions` before producing any synthesis output.** The Engine assembles the correct sections, strategy, and paths. Never proceed without calling it first.

**Build phase validation:** After producing output, run `build.py validate`. Fix any violations before marking the run complete — validation is part of the build phase. See Phase 4 and `pieces/validation.md`.

---

## Phase 4: Validate


| Human                                                                    | AI / Script                 | AI                                       | Human → AI                                 |
| ------------------------------------------------------------------------ | --------------------------- | ---------------------------------------- | ------------------------------------------ |
| Says "validate", "run validation", "check the output" (or after Phase 2) | Invokes `build.py validate` | Reports violations; fixes if build phase | Updates and adjusts → incorporates changes |


Run `build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. Validation behavior depends on scope and context:

### Validate Run

Validate **only the output of the current run**. Ignore previous work. Use when the user says "validate our run" or "check what we just did." **Fix violations before marking the run complete** — this is part of the build phase.

### Validate Slice

Validate **everything in the slice** — all accumulated output for that slice. Use when the user says "validate the slice" or "validate slice 1." **Fix violations before marking the run complete** — this is part of the build phase.

### Explicit Validate (User Request Only)

When the user **explicitly asks to validate** (e.g. "validate", "run validation", "check the output") **outside a build phase** — do **not** fix violations. Run validate, report violations, and leave with the reviewer. Do not edit files unless you are in a build phase (run_slice, validate_run, validate_slice).

See `pieces/validation.md` for the full validation checklist.

**Script:**

```bash
python scripts/build.py validate
python scripts/build.py validate path/to/interaction-tree.md
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions validate_slice
```

---

## Phase 5: Correct


| Human                                | AI / Script                                    | AI                                          | Human → AI                                 |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews output and gives corrections | Invokes script `get_instructions validate_run` | Applies corrections to run log (may re-run) | Updates and adjusts → incorporates changes |


Human reviews the run output and identifies mistakes. Corrections go to the run's Corrections section in the run log. Each correction must include a DO or DO NOT rule, an example of what was wrong, and the fix. AI may re-run the slice with corrections applied. 

See `pieces/runs.md` § Corrections Format and § When User Gives a Correction.

**Script:**

```bash
python scripts/build.py get_instructions validate_run
```

---

## Phase 6: Adjust


| Human                                        | AI / Script                                        | AI                                          | Human → AI                                 |
| -------------------------------------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews corrections, decides what to promote | Invokes script `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts → incorporates changes |


After all runs (or when the user wants), review corrections collected in run logs. Determine what needs to change. Incorporate into the session strategy and/or promote to the skill's rules those that apply across projects. The session file is the source of truth. 

See `pieces/session.md` § Patterns and `pieces/runs.md` § Patterns.

**Script:**

```bash
python scripts/build.py get_instructions improve_strategy
```

---

## Process Checklist

- [ ] **Session created and approved** — session file at `sessions/<session-name>.md` with strategy and slices; user approves before runs start
- [ ] **Run 1 produced** — output for first slice; run log written to `sessions/<session-name>/runs/run-1.md`
- [ ] **Run 1 approved** — user reviews; corrections to run log; re-run until approved
- [ ] **Run 2 … Run N** — each remaining slice: produce → review → corrections → re-run until approved
- [ ] **Review and Adjust** — review all corrections in run logs; incorporate into session strategy and/or promote to skill rules

---

# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, variation analysis, scaffold, slices, and focus; saved as an MD file. One run per slice; runs write logs. See sections below for details.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes for each node. Discovery focuses on epics and stories; Exploration adds steps below stories; Specification adds steps, scenarios, and examples. The predefined session types have predefined node levels and fields (see table below). You can also define a custom level of detail.


| Session Type      | Node levels                                       | Fields per node                                                                                                                                                                                                                                                                   |
| ----------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Epics (can nest), Stories. Stopping point: story. | Epic: Name (verb-noun), Triggering-Actor, Responding-Actor, Constraints, domain concepts (`**Concept`**), Pre-Condition, Triggering-State, Resulting-State, Trigger (Behavior, Triggering-Actor), Response (Behavior, Responding-Actor). Story: same. Domain Model with concepts. |
| **Exploration**   | Steps (below story).                              | Step: Trigger, Response, Constraints (when step-specific). Steps not grouped into scenarios. No error conditions or edge cases. Straight and linear.                                                                                                                              |
| **Specification** | Steps, Scenarios (below story).                   | Step: Trigger, Response, Examples, Constraints (when step-specific). Steps grouped into scenarios. Failure-Modes (failure conditions).                                                                                                                                            |


See `core.md` for constraints, step format, and full field definitions.  

#### Validation and Build Rule Tags

The node levels and fields chosen to be generated (e.g. Epics, Stories, Steps, Examples) determine which rules guide the build and validate the output. Tags exist for elements and fields (`epic`, `story`, `step`, `example`, `domain`) and for session types (`discovery`, `exploration`, `specification`). A Discovery session generating epics and stories means all rules tagged with `discovery`, `epic`, `story`, `interaction_tree`, `domain` will be used; a Specification session adds `specification`, `step`, `scenario`, `example`, `step_edge_case`.

**How rules are injected:** The session/strategy declares tags in scope. When `get_instructions` is called, the engine filters rules from `rules/*.md` by matching any in-scope tag. Each rule file must have YAML frontmatter with `tags: [discovery, interaction_tree, story, domain, ...]`. Rules apply to both the build phase (guiding synthesis output) and validation (checking output against rules). See `rules/README.md` for the full tag set.


| Tag                | Description                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| `discovery`        | Story-level detail: Trigger, Response, Pre-Condition, Triggering-State, Resulting-State |
| `exploration`      | Steps below story; linear, no edge cases                                                |
| `specification`    | Steps, scenarios, examples, failure modes                                               |
| `interaction_tree` | Epic/Story hierarchy; names, actors, constraints                                        |
| `epic`             | Epic-level nodes; hierarchy, granularity                                                |
| `story`            | Story-level fields: Trigger, Response, Pre-Condition, etc.                              |
| `domain`           | Domain Model — concepts, Properties, Operations                                         |
| `step`             | Atomic Trigger/Response; When/Then or verb-noun                                         |
| `step_edge_case`   | Steps + Failure-Modes; error paths                                                      |
| `example`          | Example tables per concept                                                              |
| `scenario`         | Step grouping by path                                                                   |


**Default when no session:** `tags: [discovery, interaction_tree, epic, story, domain]`.

### 2 - Scope

What portion of the context we are working with. Scope is not just a list — it **categorizes** the context. Scope drives which slices get synthesized.

- **Raw context** — If we have nothing built yet: all context, or a subset. Categorize it (e.g. index, chunk types, section mapping). Example: "406 sections; Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251; chunk types: effect definitions, advantage definitions, skill definitions, combat rules."
- **Existing structure** — If we have built output: "these stories", "all these epics", "Epic 2 and its sub-epics".

**Chunking:** Not all context will be chunked, but chunking makes variation analysis much easier. When context is chunked, use the chunk inventory (index, types) to drive scope.

**Bespoke strategies:** A custom strategy can mix components beyond the predefined session types (e.g. discovery + examples at sub-epic level, or exploration + domain concepts). The strategy defines which tags are in scope; the engine filters rules accordingly. Examples can be scoped at different levels — the strategy defines where.

### 3 - Variation Analysis

Identify differences in the scope that allow you to synthesize the elements that go into the interaction tree and Domain Model. The analysis informs when to group context into a single story and the patterns used to create different stories. **Perform enough interaction and OOAD analysis** to identify differences that could come from any of:

- **Business rules** — distinct rules or conditions change behavior.
- **System interactions** — different systems or integration points change exchange pattern.
- **Workflows** — different sequences or paths change steps, actors, or outcomes.
- **Structure** — different concept shapes or taxonomies change the interaction.
- **State** — different state transitions or preconditions change required or resulting state.

**Go over all context in enough detail** to understand how to identify all items. For instance, if doing Discovery and the context is a game rulebook, go chapter by chapter and examine the rulebook for every different rule: is it more of the same (part of same story), or different (new story)?

**The AI is empowered to create a more detailed interaction tree and domain model at whatever detail it needs to identify a pattern.** Once it has done so, it can create the rest of stories using that pattern without detailing everything. The same holds for other session types: e.g. a Specification session might go through a couple of stories and attached domain to see how to write good examples, then not need to create the rest to know what examples stories would have — just name them.

#### Variation Analysis Structure

The session's Variation Analysis section should follow this structure (with more or less detail as needed):

**1. Context Inventory / Scope**

- Source paths, chunk index (if chunked), chunk types
- Map to structure: e.g. "Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251"

**2. Analysis — Interaction**

- **Verbs** — User/System actions (Configure, Add, Choose, Apply, Resolve, Roll, Track, Create, Assign, etc.)
- **Nouns** — Domain concepts (Character, Campaign, Effect, Modifier, etc.)
- **What is consistent, what is different** — Common interactions for potentially very different data. E.g. "Configure Effect" applies to Affliction, Damage, Weaken — same workflow, different parameters per effect type.

**3. Analysis — Domain**

- Combine nouns into domain concept scaffolding
- Per-concept: properties, lifecycle, relationships
- Effect-specific structure table (when applicable): each effect type has different data structure

**4. Scaffold — Interaction Model**

- Epic/Sub-epic/Story breakdown
- A few stories per epic in full detail; then "X more stories based on pattern" (e.g. "24 more Configure Effect stories grouped by structural similarity")
- Pattern-change boundaries (when does the pattern change? new epic? new sub-epic?)

**5. Scaffold — Domain Model**

- Module per major concept (Character, Power, Effect, etc.)
- State model scaffolding per concept

**Scaffold completeness:** The scaffold does not need to enumerate every story. A few stories per epic, then "X more stories based on each [power, effect, etc.]" is often sufficient. The pattern, once identified, drives the rest.

### 4 - Scaffold

Enough of the interaction tree and domain model is synthesized to understand how remaining slices will be processed. Initial structure: epic/sub-epic/story breakdown, a few stories in full detail, then "X more stories based on pattern." Domain concepts with properties, lifecycle, and relationships. The scaffold does not need to enumerate every story — patterns drive the rest.

#### Scaffold (by Session Type)


| Session Type      | Scaffolded together                                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Interaction scaffold (epics, stories) + Domain scaffold. A few stories per epic in full; rest by pattern.                                    |
| **Exploration**   | Steps (linear). Optionally domain for step context.                                                                                          |
| **Specification** | Steps + Scenarios + Examples together. May scaffold a couple of stories with full examples to establish pattern, then apply pattern to rest. |


### 6 - Slices

The order in which you work through slices is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

A **slice** is a collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope for the run. Slices are stored in the session file; tick each when a run is done for it.

**Ideas:** Architectural slice, domain slice, integration slice, workflow slice, value slice, risk slice. Favour vertical slicing. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

**New session:** Slices can be carried over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

### 7 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.

---

<!-- section: story_synthesizer.runs -->
# Runs

During a session you synthesize the scope of a slice through a run. **One run per slice.** Run 1 = slice 1, run 2 = slice 2, etc. A run captures what happened, what changed, when it changed. The session defines level of detail; the slice defines scope for the run.

**Going deeper on the same slice** (e.g. adding steps to discovered stories) is a **new session** with a different focus, not another run.

Each run writes a **run log** to its own file under the session's runs folder. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md` (N = run number). Configurable via skill-space config.

## Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the session's level of detail (e.g. 4–7 stories if stopping at stories; epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a DO or DO NOT to the run log's Corrections section (see Corrections Format below). Re-run the slice; update the run log; repeat until approved.
3. **Next slice** — Proceed to the next slice. Apply corrections from previous runs. Same pattern: produce → review → corrections → re-run until approved.
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

1. **Add to run log** — Create or append to `runs/run-N.md` (use `run-0.md` for corrections during session start / strategy creation). Format:
  - **DO** or **DO NOT:** [the rule]
  - **Example (wrong):** [what was done incorrectly]
  - **Example (correct):** [what it should be]
2. **Apply the correction** — Refine session strategy or re-run with corrections as input.
3. **Proactively confirm** — Say: "I've added this to the run log. Correction: [brief summary]. I've applied it."

**First-run corrections:** Use `runs/run-0.md` to capture corrections during session start and initial tree/model building. Same format. The run log feeds future runs.

<!-- section: story_synthesizer.runs.patterns -->
## Patterns (from Runs)

**Strategy is upfront; runs can extend it.** After each run, examine all runs for new patterns. If found, add to the session's Patterns section.


| Run   | What was built                                               | Pattern found             | Applicable to               |
| ----- | ------------------------------------------------------------ | ------------------------- | --------------------------- |
| run-1 | e.g. "wrote steps and examples for all stories under epic X" | Brief pattern description | Scope where pattern applies |


**Example:** Run 2 built steps and examples for "Configure Power Effect" stories. Pattern: "Effect-type stories share same step structure — Configure, Validate, Apply." Applicable to: other effect types under the same epic.

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
