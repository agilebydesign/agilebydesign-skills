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

## Variation Analysis

With the foundational models established (see `pieces/domain.md`), analyze what varies within each. The models are the lens — variation analysis asks: "for this model, what specializes it? What's the same base, what's different?"

- **Per foundational model:** What consumers extend it with new behavior (stories) vs add only new data (examples)?
- **Business rules** — distinct rules or conditions that change behavior within the model.
- **Workflows** — different sequences or paths that change steps, actors, or outcomes.
- **State** — different state transitions or preconditions that change required or resulting state.

This is where the interaction verbs and nouns become structured:
- **Verbs** — User/System actions, organized by which foundational model they operate on.
- **Nouns** — Domain concepts, placed within their foundational model.
- **What is consistent, what is different** — within each model, not across the whole context.

**Output location:** Write to `<session>/interaction-tree.md` between `<!-- section: variation_analysis -->` and `<!-- /section: variation_analysis -->` markers.

---

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

<!-- section: story_synthesizer.domain -->
# Domain Model

## Module

Grouping of tightly related concepts.

- **name** — module name
- **concepts** — list of tightly related domain concepts

## Domain Concept

A domain concept that holds state and can be operated on. Referenced in interactions via `**Concept`** in labels. Examples live on the interaction. The Domain Model connects what concepts know and do to interactions — concepts participate as callers, receivers, and collaborators; state flows through Pre-Condition, Triggering-State, and Resulting-State.

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

---

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

**Set path for new work area:** Edit the synthesizer's `conf/abd-config.json` and set `"skill_space_path": "/path/to/workspace"` (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/`. Context paths are owned by the skill space (see Phase 1).

**Get path to continue:** Run `get_config` to see where the skill is currently pointed.

**Script:**

```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_config
```

**Output:** JSON with `engine_root`, `skill_space_path` (and `skill_path` as shorthand), `config_path`, and optionally `strategy_path`, `context_paths`. The engine resolves `skill_space_path` from the synthesizer's config and `context_paths` from the skill space's `conf/abd-config.json`.

---

## Phase 2: Prepare Context

Setup — run once per workspace, skip if context is already chunked and scanned.


| Human                                                          | AI / Script                                                                          | AI                                                        | Human → AI     |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------- | -------------- |
| Says "analyze concepts", "prepare context", or "scan concepts" | Validates chunking, runs `concept_tracker.py seed` → `scan` → `report`, deep-reads | Reports chunking status, cross-cutting terms, co-clusters | Reviews report |


Three steps (see `pieces/session.md` § 2 - Context for details):

1. **Chunking (§2a):** Ensure source documents are chunked to markdown. `get_instructions` validates automatically — warns if unchunked or stale.
2. **Concept Tracking (§2b):** Run `concept_tracker.py` to scan chunks and build term cross-references.
3. **Concept Deep Analysis (§2c):** Deep-read 3–5 representative chunks per candidate model to identify mechanically distinct categories from source text.

---

## Phase 3: Start Session


| Human                                        | AI / Script                                       | AI                                             | Human → AI                                 |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| Says "start a session" or "create a session" | Invokes script `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts → incorporates changes |


Create, open, or continue an existing session. Name it (user-provided or AI-derived from context). The session file stores strategy: Level of Detail, Scope, Context Inventory, Foundational Object Models, Variation Analysis, Interactions, and slices. Option: carry slices over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

**Session path:** `<skill-space>/story-synthesizer/<session-name>/<session-name>-session.md`

**Naming convention:** Session files end with `-session.md`. The session folder `<session-name>/` contains the session file, the first-cut output files (`interaction-tree.md`, `domain-model.md`), and a `runs/` folder for run logs.

The session/strategy declares **tags in scope** (e.g. `discovery`, `interaction_tree`, `stories`, `domain`, `steps`). The engine filters rules by tags. See `pieces/session.md` for session content, slices, discriminators, and tag definitions.

**Session creation is a run (run-0).** Treat it exactly like any other run: produce output, validate with `build.py validate`, fix violations, record corrections in `runs/run-0.md`. The user reviews and corrects strategy, foundational models, variation analysis, and first-cut output files. Run `build.py validate` on `interaction-tree.md` and `domain-model.md` before session creation is considered done. Corrections feed into run 1 — they are not lost.

**Script:**

```bash
python scripts/build.py get_instructions create_strategy
```

---

## Phase 4: Execute a Run


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

**Before starting a run:** Check for unrecorded corrections from session creation or previous runs. If unsure, run `python scripts/build.py get_instructions correct_run` to review the chat for missed corrections.

**Build phase validation:** After producing output, run `build.py validate`. Fix any violations before marking the run complete — validation is part of the build phase. See Phase 3 and `pieces/validation.md`.

---

## Phase 5: Validate


| Human                                                                    | AI / Script                 | AI                                       | Human → AI                                 |
| ------------------------------------------------------------------------ | --------------------------- | ---------------------------------------- | ------------------------------------------ |
| Says "validate", "run validation", "check the output" (or after Phase 1) | Invokes `build.py validate` | Reports violations; fixes if build phase | Updates and adjusts → incorporates changes |


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

## Phase 6: Correct


| Human                                | AI / Script                                    | AI                                          | Human → AI                                 |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews output and gives corrections | Invokes script `get_instructions validate_run` | Applies corrections to run log (may re-run) | Updates and adjusts → incorporates changes |


Human reviews the run output and identifies mistakes. Corrections go to the run's Corrections section in the run log. Each correction must include a DO or DO NOT rule, an example of what was wrong, and the fix. AI may re-run the slice with corrections applied. 

See `pieces/runs.md` § Corrections Format and § When User Gives a Correction.

**Checking for missed corrections:** Run `get_instructions correct_run` to review the chat for unrecorded changes. Run `correct_all` to do the full correction pipeline (run → session → skill) in one shot.

**Script:**

```bash
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions correct_run
python scripts/build.py get_instructions correct_all
```

---

## Phase 7 : Adjust


| Human                                        | AI / Script                                        | AI                                          | Human → AI                                 |
| -------------------------------------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews corrections, decides what to promote | Invokes script `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts → incorporates changes |


After all runs (or when the user wants), review corrections collected in run logs (including `run-0.md` from session creation). Determine what needs to change. Incorporate into the session strategy and/or promote to the skill's rules those that apply across projects. The session file is the source of truth.

**When promoting corrections to the skill**, record the fix details in the run log's "Promoted to Skill" section — a table with: Correction, Target file, and Change (a from→to snapshot, not the full diff). This creates a traceable history of why each rule or piece was added or changed.

See `pieces/session.md` § Patterns and `pieces/runs.md` § Patterns.

**Script:**

```bash
python scripts/build.py get_instructions improve_strategy
```

### Three layers of correction

Corrections flow through three layers. Each layer builds on the previous — don't skip ahead, but don't stop at recording either. Be aggressive about suggesting what should change at each layer.


| Layer           | Operation         | Where                                            | What happens                                                                                            |
| --------------- | ----------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **1. Record**   | `correct_run`     | Run log (`runs/run-N.md`)                        | DO/DO NOT captured with wrong/correct examples. The fix is applied to the output files.                 |
| **2. Strategy** | `correct_session` | Session file (`*-session.md`)                    | Correction incorporated into session strategy so future runs in this session follow it.                 |
| **3. Skill**    | `correct_skill`   | Skill rules/pieces (`rules/*.md`, `pieces/*.md`) | Correction promoted to a skill rule or process piece. Recorded in "Promoted to Skill" table in run log. |
| **All**         | `correct_all`     | All three in sequence                            | Runs all three layers: record → strategy → skill.                                                       |


**Don't give up on making changes.** Each layer builds on the previous. Be aggressive in suggestions at every layer — propose the change, let the user decide.

---

## Process Checklist

- **Session created and approved** — session file at `sessions/<session-name>.md` with strategy and slices; user approves before runs start
- **Run 1 produced** — output for first slice; run log written to `sessions/<session-name>/runs/run-1.md`
- **Run 1 approved** — user reviews; corrections to run log; re-run until approved
- **Run 2 … Run N** — each remaining slice: produce → review → corrections → re-run until approved
- **Review and Adjust** — review all corrections in run logs; incorporate into session strategy and/or promote to skill rules

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

### 2 - Context

Context preparation has three steps: chunk it, scan it, read it. Each step builds on the previous.

#### 2a - Context Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown before analysis. The `get_instructions` command validates this automatically — if documents are unchunked or stale, it warns with the command to run.

- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "406 sections; Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

#### 2b - Concept Tracking

Run `concept_tracker.py` to extract terms from chunks and build a cross-reference matrix. Required before foundational models — if not available, stop and report the error.

```bash
python scripts/concept_tracker.py seed --source <domain-model-or-wordlist>   # optional: seed glossary
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <terms_report.json> --min-units 5
```

**Output:** `terms_report.json` with per-unit terms, term index, cross-references by frequency, and co-occurrence clusters. Use the report to drive foundational model identification (§4).

#### 2c - Concept Deep Analysis

The concept tracker finds *what terms exist* and *where they co-occur*, but does NOT reveal mechanical variation. Before writing foundational models or variation analysis, deep-read the source chunks for each candidate model.

1. Use `term_index` from `terms_report.json` to find which chunks contain each candidate model's key terms
2. For each candidate model, read 3–5 representative chunks
3. Extract the mechanically distinct categories from the actual source text — not from memory
4. Record which sections were read and what categories were found

**Validation pass on "examples" annotations:** After drafting the scaffold, for every annotation that says "X are examples (same flow)," verify from source chunks that all items share the same interaction flow. The test: does the item change who rolls, what DC, what triggers the check, or what the outcome does? If yes — separate story, not example.

### 4 - Foundational Object Models

Using the concept tracker report and deep read pass (§3b), identify foundational models via OOAD (find objects, find collaborations, find repetition — see `pieces/domain.md` § Foundational Object Models for full process). Each model: State Model (typed concepts with properties, operations, collaborators) + Extensions (names only). Each model becomes a module in the domain model.

**Output:** Write to `<session>/domain-model.md` § Foundational Object Models (between `<!-- section: foundational_models -->` markers). Session §4 references the output file — do not duplicate models here. Auto-injected into `create_strategy` prompt.

### 5 - Variation Analysis

Per foundational model from §4, analyze what varies: what's consistent, what differs, what extends with new behavior (→ story) vs adds data to same behavior (→ example). Identify business rules, workflow differences, and state variations. See `pieces/interaction.md` § Variation Analysis for full process.

**Output:** Write to `<session>/interaction-tree.md` § Variation Analysis (between `<!-- section: variation_analysis -->` markers). Session §5 references the output file — do not duplicate analysis here. Auto-injected into `create_strategy` prompt.

### 6 - Interaction Scaffold

**Story vs Example rule:** Functionality that extends a foundational model with NEW BEHAVIOR requires a story (new operations, new state transitions, new validation rules). Adding DATA to the same behavior is just an example on an existing story. This is how you decide what becomes a story and what becomes an example.

Build the interaction tree on top of the foundational models:

- Epic/Sub-epic/Story breakdown
- Each sub-epic references which foundational model(s) it extends
- List ALL story names (lean format: name + parenthetical examples). The session scaffold identifies every story.
- Pattern-change boundaries (when does the pattern change? new epic? new sub-epic?)
- The scaffold lists names only — no Trigger, Response, Pre-Condition, or other fields. Those belong in the interaction-tree.md output file.

**Scaffold format:** Lean — epic name, story names with parenthetical examples, variation analysis rationale. List ALL story names so slices can be properly designed (you need the full picture to build vertical slices). 

### 7 - First-Cut Output Files

The scaffold phase produces the **first cut of the real output files** (`interaction-tree.md`, `domain-model.md`). These are not separate "scaffold files" — they ARE the deliverables at version 1. Runs expand them slice by slice.

The first cut uses pattern+extrapolation: 2-3 stories per epic in full detail (Trigger, Response, Pre-Condition, domain concepts), remaining stories listed by name only. Runs expand the named stories with full detail slice by slice.

**Validate first-cut outputs.** Session creation is run-0 — run `build.py validate` on `interaction-tree.md` and `domain-model.md` before session creation is done. Same rules, same scanners, same fix-before-marking-complete as any run. The session scaffold (§6) also gets the slice scanner (`session-slice-not-epic-by-epic`).

#### First Cut (by Session Type)


| Session Type      | First cut produces                                                                                                                           |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | `interaction-tree.md` (epics, 2-3 stories per epic in full; rest by pattern) + `domain-model.md` (concepts with properties and operations). |
| **Exploration**   | Steps added to existing stories in `interaction-tree.md`. Optionally domain updates.                                                         |
| **Specification** | Steps + Scenarios + Examples added to existing stories. May detail a couple of stories fully to establish pattern, then apply to rest.        |


### 8 - Slices

The order in which you work through slices is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

**DO NOT slice by epic.** If your slices map 1:1 to epics, you did it wrong. Each slice must build something AND use it — end-to-end. There is no value in building all of one epic's stories without proving they work by using them. Group build + use into categories and implement that way.

**Slicing checklist:**
- Does each slice build AND use something?
- Does any slice build things that aren't used until a later slice? If yes, restructure.
- Are slices ordered from simple to complex, layering on complexity?
- Does each slice prove the previous one works before adding the next layer?

A **slice** is a collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope for the run. Slices are stored in the session file; tick each when a run is done for it.

**Ideas:** Architectural slice, domain slice, integration slice, workflow slice, value slice, risk slice. Favour vertical slicing. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

**New session:** Slices can be carried over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

### 9 - Runs

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
