# Core Data Model

## What the Story Synthesizer Does

The story synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

Your task is to **synthesize** source material into an **Interaction Tree** and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. Outputs: story map, domain model, acceptance criteria, specifications, walkthroughs.

In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Synthesis can stop at the story level; details are flushed out later.

**Interaction Tree:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). Epics group stories; the story is the backbone — the smallest unit that is both valuable and independently deliverable. Each story has Pre-Condition, Trigger, Response, and statement. Scenarios optionally group steps; steps are atomic interactions.

**State** runs alongside. Pre-Condition is what must be true before; Response implies resulting state. Domain concepts (the things that hold state and get operated on) are referenced via `**Concept**` in labels; each must exist in the Domain Model. Tree and Domain Model evolve together — no drift.

---

All concepts are defined below. See the output folder: `output/interaction-tree-output.md` and `output/domain-model-output.md` for format and presentation.

<!-- section: story_synthesizer.core.interaction -->
## Interaction Model

An interaction is a single meaningful exchange between two actors that results in either a retrieval of state or a change of state.

### Interaction

- **Name** — name of the interaction. **Ground in domain:** Every epic, story, scenario, and step must be grounded in domain language — either in the name or in the statement — using `**Concept**` (double stars, capitalization). Domain concepts must appear in `**Concept**` format so the domain conditions are described.
- **Statement** — one-sentence trigger and response; include domain concepts where appropriate.

**Name and statement (all nodes):** Use active verb language. Short name first, longer statement in brackets. Format: `Node: Short Name (Longer statement.)` — e.g. `Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays...)`. Name is always verb-noun or subject-qualifier; statement is always the longer sentence. **Epic statement:** Describe the scope of the epic (broad flows), not a single interaction. **Story/Step statement:** One trigger and response.
- **Impacts** — zero or more (see Impact below)
- **Constraints** — zero or more. Qualitative instructions on how this interaction is structured. A constraint may be a sentence, a reference to a collection of files, or (most commonly) a reference to a markdown file. Constraints are inherited from high to low (parent → child).
- **Pre-Condition** — label only. What must be true before. State qualifies through the label. Use `**Concept**` to reference domain concepts; each must exist in the Domain Model.
- **Trigger** — Triggering-Actor, Behavior (label), Triggering-State. Triggering-State is any state that qualifies the interaction (e.g. selecting an option of a certain type). Labels reference domain concepts; examples live on the interaction.
- **Response** — Responding-Actor, Behavior (label), Resulting-State. Resulting-State is the state that results from the interaction. Labels reference domain concepts; examples live on the interaction.
- **Examples** — collection of tables at the interaction level. One per concept referenced in labels. Pre-Condition, Trigger, and Response reference these through their labels; examples live on the interaction.
- **Failure-Modes** — up to three; how the exchange can fail (rule/state based only)
- **Children** — child interactions of this interaction.

#### Interaction Tree Rules
**Node Hierarchy**
- Epic - Can nest to have epic children or story children. An epic whose parent is an epic is sometimes called a sub-epic. Names are typically simple verb-noun.  
- Story - Smallest unit of testable value that is independently delivered. Names are typically simple verb-noun.  
- Scenario - Groups steps; optional container for a story. Names describe the primary conditions tested in the scenario.  
- Step - Atomic interaction within a scenario. Steps are interactions: often in the form of **Trigger** (When) and **Response** (Then). 

Epic → children (Epics, Stories)  
Story → Scenarios OR Steps
Scenario → Steps  
Step --> lowest interaction for now

#### The Story as Backbone

The **story** is the backbone of all the work above and below it. It is the central unit that everything connects to.

- **Above the story:** Epics and sub-epics exist only to **group stories together**. They are organizational structure, not the primary unit of value.
- **Below the story:** All steps, examples, and scenarios **belong to the story**. The story is the central spoke — everything below it hangs off the story.

**What a story is:** A story is something we can reasonably discuss as a valuable tactical interaction between the user and the system (or between systems). It is something that can be developed in a small amount of time — typically a couple of days for a developer (or a couple of hours for AI :). It is the smallest unit that is both valuable and independently deliverable. It needs to be testable, which means it must have a recognizable behavior that a user or stakeholder would recognize. Not necessarily always user-facing, but at least recognizable as a tangible business state that's changed or logic has been executed here.

**Stopping point:** The story is typically the stopping point **for Shaping and Discovery**. For Exploration, Walkthrough, and Specification, we go below the story (to steps, examples, scenarios). With slices and runs, *we have explicit control on the stopping point*: a run on a slice of a couple of epics can have criteria to only identify other epics and not stories. The stopping point is configurable. See Impact below for the Impact data model (types, status, evidence linking).

**Commonly Generated Fields Vary By Node Type:** 
Any node level can use any field. Exceptions are always possible. The table below lists what we commonly generate for each node.

| Node | Commonly generated | Case By Case Generated |
|------|--------------------|------------------------|
| Epic | Triggering-Actor, Responding-Actor, Name (Verb Noun), Impact, Constraints | Pre-Condition, Triggering-State, Resulting-State, Examples, Failure-Modes|
| Story | Trigger , Response ; Name (Verb Noun), Examples, Pre-Condition (eg BDD backgroun, Given, And); Failure-Modes, Constraints |
| Scenario | Trigger, Response, Pre-Condition (eg BDD Given, And); Examples |
| Step | Trigger, Response,(When, And, Then, And); Examples; Constraints (when step-specific) |

**Nodes inherit attributes from their parents.** 
Child nodes inherit state, examples, pre-conditions, actors, domain concepts, and constraints. You can show inherited attributes explicitly in square brackets (e.g. `Triggering-Actor: [User]`, `Examples: [Logged In User, Active Session]`) so readers see which values came from the parent. When you use brackets, update them if the parent changes. **Inheritance applies either way** — even when you don't show brackets, the inherited values still apply to the child. See Hierarchy Inheritance for conventions.

**Inheritance that we often want to call out explicitly through the [inherited thing] notation**
- **Epic from Epic:** Domain concepts. Lower-level epics (sub-epics) often use the inherited domain concepts from their parent epic.
- **Story from Epic:** Triggering-Actor, Responding-Actor, Pre-Condition, Examples based on Pre-Condition, domain concepts.
- **Scenario from Story:** Almost nothing needs to be explicitly stated.
- **Step from Story:** Triggering-Actor and Responding-Actor are often used, eg [User] and [System] from the story or higher. Exception: when a step is system-triggered (e.g. "When **System** receives payment type selection"), that step may override Triggering-Actor.

**Domain grounding:** Every epic, story, scenario, and step must be grounded in domain language. This primarily comes from the interactions (e.g., trigger and response) if they have been defined, but if they have not been defined, then it would come from the  the name or  the statement. When When trigger and response have been defined, the name is based on those, but sometimes we don't define these for a node, and just define the name at first. In either case, all of the above need to be grounded using `**Concept**` (double stars on both sides, capitalization). Avoid generic terms; use `**Country**`, `**PaymentType**`, etc., not "country" or "payment type". Concepts must come from the Domain Model here. Concept identified as part of exploring the interaction tree should be added to the Domain Model and vice versa. When we add things to the Domain Model, we should explore which interactions require those and update accordingly.

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

## Domain Model

The Domain Model holds **modules** (groupings of tightly related concepts) and **domain concepts** — the things that have state and can be operated on. Concepts are referenced in interactions via `**Concept**` in Pre-Condition, Trigger, Response, and Failure-Modes. Every `**Concept**` must exist in the Domain Model; concepts must be placed at the right level in the hierarchy. No drift between tree and model. Use source entity data, not aggregated/calculated values.

### Module

Grouping of tightly related concepts.

- **name** — module name
- **concepts** — list of tightly related domain concepts

<!-- section: story_synthesizer.core.domain_concept -->
### Domain Concept

A domain concept that holds state and can be operated on. Referenced in interactions via `**Concept**` in labels. Examples live on the interaction. The Domain Model connects what concepts know and do to interactions — concepts participate as callers, receivers, and collaborators; state flows through Pre-Condition, Triggering-State, and Resulting-State.

- **Name**
- **Module** — optional; grouping of tightly related concepts
- **Base-Concept** — optional
- **Properties** — with optional collaborating concepts and invariants. Use standard types: String, Number, Boolean, List, Dictionary, UniqueID, Instant. Use `List<T>` or `Dictionary<K,V>` when element types matter.
- **Operations** — with optional collaborating concepts and invariants. It should be easy to reverse engineer the interactions in the interaction diagram to at least some level of operations on the Domain Model.
 
**Concept relationships:** When a concept "has" another concept, use composition (strong has-a; part cannot exist without whole) or aggregation (weak has-a; whole has no meaning without multiple instances of the same part — e.g. crowd, flock, mob). Prefer composition/aggregation over inheritance.

### Domain Model Example (from Interaction Tree)

The following concepts correspond to the Complete Example hierarchy (Make **Country**-specific **PaymentType**). Each `**Concept**` referenced in the interaction tree must exist here.

**Module: payment**

- **User** — Properties: user_name (String), user_role (String). Operations: browse_countries(), select_country(**Country**), select_payment_type(**PaymentType**), enter_payment_details(**PaymentDetails**), submit(). Examples: Logged In User.
- **Session** — Properties: session_id (String), user_name (String), expires_at (Instant). Operations: is_active(). Examples: Active User Session.
- **Country** — Properties: country_code (String), country_name (String). Operations: get_payment_types(). Examples: Selected Country.
- **PaymentType** — Properties: payment_type (String). Operations: get_field_types(). Examples: PaymentType, Selected PaymentType.
- **UserPaymentAccess** — Properties: user_name (String), country_code (String), payment_type (String), available (Boolean). Operations: has_access(**User**, **Country**, **PaymentType**). Examples: User Payment Type Access.
- **PaymentTypeFieldTypes** — Properties: payment_type (String), fields (List&lt;String&gt;). Examples: Payment Type Field Types.
- **PaymentDetails** — Properties: payment_type (String), amount (Number), currency (String), beneficiary_id (String), swift_code (String), routing_number (String), account_number (String). Operations: validate(). Examples: PaymentDetails (wire).

---

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

## Complete Example

A typical reference hierarchy for making a country-specific payment (trigger, make transaction, fulfill). **Concepts** are referenced via `**Concept**` in labels. **Examples** live on the interaction. Pre-Condition, Trigger, and Response qualify through their labels. Epic holds rules that apply to all children (e.g. user access to payment types by country). Epics group; they do not add trigger/response state. Stories inherit from Epic. One story is taken to full detail with scenario and steps. (Other epics and stories not yet filled out.)

**Hierarchy levels:** Epic → Story → Scenario → Step (epics can nest; an epic child of an epic is sometimes called a sub-epic)

**Name and statement:** Active verb language, short name first, statement in brackets (see Interaction).

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
      | success  | US           | ach          |

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

# Process Overview

Your task is to **synthesize** context into an **Interaction Tree** and **Domain Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them.

**You MUST follow this process.** When the user says "create the story map," "proceed," "build it," "build a strategy," "generate the output," "start a session," or similar, you **MUST** call `python scripts/build.py get_instructions <operation>` and inject its output before producing any synthesis output. Do not rely on AGENTS.md alone.

| User says | Operation |
|-----------|-----------|
| "start a session", "create a session" | `create_strategy` |
| "build a strategy", "create the strategy", "propose slices" | `create_strategy` |
| "proceed", "build it", "run slice 1", "next run" | `run_slice` |
| "validate our run", "check what we just did" | `validate_run` |
| "validate the slice", "validate slice 1" | `validate_slice` |

**Usage:** From the skill directory, run `python scripts/build.py get_instructions <operation>`. See **Script Invocation** for paths, validate, and full details.

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes.

### 1. Start Session


| Human                                        | AI / Script                                       | AI                                             | Human → AI                                 |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| Says "start a session" or "create a session" | Invokes script `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts → incorporates changes |


Create, open, or continue an existing session. Name it (user-provided or AI-derived from context). The session file stores strategy: Level of Detail, Scope, Variation Analysis, and slices. Option: carry slices over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.  
Please *see Sessiions,md* for further details

### 2. Execute A Run


| Human                                                             | AI / Script                                 | AI                                | Human → AI                                 |
| ----------------------------------------------------------------- | ------------------------------------------- | --------------------------------- | ------------------------------------------ |
| Says "proceed," "build it," "run slice", "next run", "next slice" | Invokes script `get_instructions run_slice` | Produces run output for the slice | Updates and adjusts → incorporates changes |


Slices are completed through a run. Run 1 = slice 1, run 2 = slice 2, etc. A run may require multiple iterations (user reviews → corrections to run log → re-run) until approved. We use slices and runs to prevent produceing a complete interaction tree or domain model in one pass — iterate slice by slice. Corrections carry forward: run 2 applies corrections from run 1; run 3 applies corrections from runs 1 and 2.  
Please *see Sessiions,md* for further details

### 3. Correct


| Human                                | AI / Script                                    | AI                                          | Human → AI                                 |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews output and gives corrections | Invokes script `get_instructions validate_run` | Applies corrections to run log (may re-run) | Updates and adjusts → incorporates changes |


**Description:** Human reviews the run output and identifies mistakes. Corrections go to the run's  Corrections section in the the run log. Each correction must include a DO or DO NOT rule, an example of what was wrong, and the fix. AI may re-run the slice with corrections applied.

### 4. Adjust


| Human                                        | AI / Script                                        | AI                                          | Human → AI                                 |
| -------------------------------------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews corrections, decides what to promote | Invokes script `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts → incorporates changes |


**Description:** After all runs (or when the user wants), review corrections collected in run logs. Determine what needs to change. Incorporate into the session strategy and/or promote to the skill's rules those that apply across projects. The session file is the source of truth

## Output Paths (default)

- **Session:** `<skill-space>/story-synthesizer/sessions/<session-name>.md` — Strategy (Level of Detail, Scope, Variation Analysis), **slices** (list with tick when run done), and session metadata
- **Output:** `<skill-space>/story-synthesizer/` — Interaction Tree and Domain Model (format in `output/interaction-tree-output.md` and `output/domain-model-output.md`)
- **Runs:** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/` — run logs (one file per run, e.g. `run-1.md`)

These paths can be configured under the skill-space config (`abd-config.json`) so the user can choose where files go and what they are named.

### Running Slices

**Slices** are units of context to synthesize (e.g. a chunk range, an epic, a set of stories). **Runs** produce output for one slice each: run 1 = slice 1, run 2 = slice 2. Each run writes a log; corrections go to the log and carry forward to later runs.  
Please *see Sessiions,md* for further details

1. **Run the first slice** — Produce output for Slice 1 according to the session's level of detail (e.g., 4–7 stories if stopping at stories; epics and sub-epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a **DO** or **DO NOT** to the **run log** (the run's Corrections section). Each correction must include:
  - The **DO** or **DO NOT** rule
  - **Example (wrong):** What was done incorrectly
  - **Example (correct):** What it should be after the fix
  - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
  - Re-run the slice; update the run log with the new Before/After and any additional corrections; repeat until the user approves
3. **Next slice** — Proceed to the next slice. Apply corrections from previous runs. Same pattern: produce → review → corrections to run log → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the session and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

## Process Checklist

**Each session needs the following flow:**

- **Session created and approved** — Session file created at `sessions/<session-name>.md` with strategy (Level of Detail, Scope, Variation Analysis, slices); user approves before runs start
- **Run 1 produced** — Output for first slice; run log written to `sessions/<session-name>/runs/run-1.md`
- **Run 1 approved** — User reviews; when mistakes are found, add DO/DO NOT to the **run log** Corrections section (with wrong/correct examples); re-run taking corrections into account; repeat until user approves
- **Run 2 … Run N** — For each remaining slice: produce → review → corrections to run log → re-run until approved. To go deeper on a slice (e.g. add steps), start a new session with a different focus.
- **Review and Adjust** — When all runs are done (or when user wants): review all corrections in run logs; incorporate into session strategy and/or promote to skill rules

---

<!-- section: story_synthesizer.output.interaction_tree -->
# Interaction Tree Output

Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

**Constraints:** Any node can have a `Constraints:` collection — qualitative instructions on how the interaction is shaped. Each constraint may be a sentence, a file path, or (most commonly) a markdown reference. Inherited high to low. Typically at epic or story level; may appear in steps.

---

# Epics and Stories View (Hierarchy)

The tree view: Epic → Epic/Story children. Each node shows name, actors, and inherited vs own fields.

# Epic (filled out — has Examples)

- Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- `- Triggering-Actor:` value
- `- Responding-Actor:` value
- `- Constraints:` collection (sentence, file path, or markdown reference; inherited high to low)
- `- Pre-Condition:` full label (Given/And)
- `- Examples:` state table block (see Example Block Format below)

## Epic (not filled out — inherits only)

- Heading: `## Epic: <name using **Domain Concepts**> (<statement>)`
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [full inherited label]
- `- Examples:` [list of inherited state table names]
- `- Triggering-Actor:` [User] (or other actor)
- `- Responding-Actor:` [System] (or other actor)

### Story (filled out — has Trigger, Response, Failure-Modes, Scenarios)

- Heading: `### Story: <name using **Domain Concepts**> (<statement>)` — same pattern as Epic
- `- Pre-Condition:` [inherited]
- `- Failure-Modes:` bullet list (up to 3)
- `- Trigger:` sub-bullets Triggering-Actor, Behavior
- `- Response:` sub-bullets Responding-Actor, Behavior
- `###### Scenario:` name
- `####### Steps`
- Step items (see Story Details View)

### Story (not filled out)

- Heading: `#### Story:` + **Name**
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [inherited]
- `- Examples:` [inherited table names]
- `- Triggering-Actor:` [inherited]
- `- Responding-Actor:` [inherited]

---

# Story Details View (Drill-down)

When a story is expanded: Scenarios, Steps, and per-step Trigger/Response/Examples.

## Step (no Examples)

- `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- `- Constraints:` [inherited] or own (when step-specific)
- `- Trigger:` [inherited], Behavior
- `- Response:` [inherited], Behavior

## Step (with Examples)

- Same as Step (no Examples), plus `- Examples:` block
- Each table: label, blank line, header row, separator row, data rows
- Each table is a separate block; blank line between tables

## Step (system-triggered)

- Triggering-Actor overridden to [System] when the step is system-triggered (e.g. "When **System** receives...")

## Example table

Always add a qualifier in parentheses: `ConceptName (qualifier):`

- **Scenario column:** Required on entity tables. Use kebab-case (e.g. success, invalid-details, not-available).
- **Inherited examples:** Show as `Examples: [Table Name 1, Table Name 2, ...]` — list names, not tables.

## Epic-level example tables

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

---

# Heading Levels

| Level | Use |
|-------|-----|
| `#` | Epic |
| `##` | Child Epic (Every level of nesting at a header level) |
| `###` | Story (Assuming only two levels of epic nesting) |
| `####` | Scenario (Assuming only two levels of epic nesting) |
| `#####` | Steps (Assuming only two levels of epic nesting) |

---

<!-- section: story_synthesizer.output.domain_model -->
# Domain Model Output

Separate from the Interaction Tree. Concepts referenced via `**Concept**` in labels. Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

## Format

```
Concept : <Base Concept if any>
- <type> property
      <collaborating concepts if any>
- <type> operation(<param>, ...)
     <collaborating concepts if any>
- Interactons Interaction Concept used by (root node only)
- examples: list of domain concept tables in interaction tree using this concept
```

---

# Run Output

Each run writes a run log to its own file. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md` (N = run number). Configurable via skill-space config.

## Structure

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

---

# Validation Pass

<!-- section: story_synthesizer.validation.scope_run -->
## Scope: Validate Run

Validate **only the output of the current run**. Ignore previous work. Use when the user says "validate our run" or "check what we just did."

**Required:** Run `python scripts/build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. **Fix them before marking the run complete** — this is part of the build phase.

<!-- section: story_synthesizer.validation.scope_slice -->
## Scope: Validate Slice

Validate **everything in the slice** — all accumulated output for that slice. Use when the user says "validate the slice" or "validate slice 1."

**Required:** Run `python scripts/build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. **Fix them before marking the run complete** — this is part of the build phase.

<!-- section: story_synthesizer.validation.explicit_validate -->
## Explicit Validate (User Request Only)

When the user **explicitly asks to validate** (e.g. "validate", "run validation", "check the output") **outside a build phase** — do **not** fix violations. Run validate, report violations, and leave with the reviewer. Do not edit files in front of the user unless you are in a build phase (run_slice, validate_run, validate_slice).

<!-- section: story_synthesizer.validation.checklist -->
## Validation Checklist

After generating interactions and concepts, verify against the output format in `output/interaction-tree-output.md` and `output/state-model-output.md`.

**Run scanners:** Execute `python scripts/build.py validate` (or `validate <path>`) to run rule-based scanners on the interaction tree and state model. Scanners use regex and native Python only (or grammar/AST when available). When in a build phase (run_slice, validate_run, validate_slice), fix any reported violations before considering the run complete. When the user explicitly asks to validate outside a build phase, report violations only — do not fix.

**Strategy alignment:** Check that nodes include the fields specified by the strategy's **Comprehensiveness Criteria** for the current mode (Discovery, Exploration, Specification). The strategy states which mode(s) apply and what is in scope — e.g. Discovery expects Pre-Condition, Triggering-State, Resulting-State, Trigger, Response; Specification expects Examples, scenarios, failure conditions. Do not require fields that are out of scope for the run.

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

## State Model

**Concept**
- [ ] Format: `Concept : <Base Concept if any>`
- [ ] Properties, operations, collaborating concepts listed
- [ ] `examples:` list of state concept tables from interaction tree
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

When adding corrections to the run log, use the format from `strategy.md`:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix

If failing on the same guidance again, add an extra example to the existing DO/DO NOT block.

---

# Script Invocation

AI guidance for calling abd-story-synthesizer scripts. **Process** requires you to call `get_instructions` before producing synthesis output — use the operations below to select the correct one.

## Get paths (engine_root, skill_space_path)

When you need to know where the skill lives or where output goes, run:

```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_config
```

**Output:** JSON with `engine_root`, `skill_space_path` (and `skill_path` as shorthand), `config_path`, and optionally `strategy_path`, `context_paths`. Use this instead of hunting through docs — the script returns the resolved paths from `conf/abd-config.json`.

**To set `skill_space_path`:** Edit `conf/abd-config.json` and set `"skill_space_path": "/path/to/workspace"` (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/`.

## Strategy and runs

1. **Iterative Strategy** — Strategy runs through every run. First run: create strategy document, build tree and Domain Model, spot patterns. Create output as you go — do not wait for approval before producing tree and Domain Model.
2. **Perform runs** — Each run produces output for a slice. Runs iterate (user reviews → corrections to run log → re-run) until approved. Then next slice. Every run examines all runs for new patterns; if found, add to strategy.

## Strategy passed into API

The strategy is **passed into the API** (not just embedded in markdown). The session/strategy declares **tags in scope** — e.g. `discovery`, `interaction_tree`, `stories`, `domain`, `steps`, etc. The engine filters rules by tags: include a rule if any of its tags matches any in-scope tag. Session type determines scope; see `content/strategy.md` and `rules/README.md`.

**Bespoke strategies:** A custom strategy can mix components (e.g. discovery + mapping to stories + domain concepts + examples at sub-epic level). Examples can be scoped at different levels — the strategy defines where.

## build.py get_instructions

Gets the assembled prompt for an operation from the Engine. **You MUST call this before producing any synthesis output.** Do not rely on AGENTS.md alone — run the command and inject its output. The strategy (path or content) is passed in; the engine parses it for components and filters rules accordingly.

**Rules injection:** Operations that include `story_synthesizer.validation.rules` (create_strategy, run_slice, generate_slice, validate_run, validate_slice) inject rules from `rules/*.md` **filtered by tags in scope**. All runs get validated, but validation uses different rules depending on what you synthesize — domain rules for domain output, step rules for steps, example rules for examples, etc. Rules are injected based on the strategy's declared tags. Each rule must have YAML frontmatter with `tags: [discovery, interaction_tree, story, domain, ...]`. See `rules/README.md` for the full tag set.

**When to call:**

| Operation | User says | Notes |
|-----------|-----------|-------|
| `create_strategy` | "build a strategy", "create the strategy", "analyze and propose breakdown", "propose slices" | Produces strategy with slices and builds tree/state model. Injects discovery rules (`rules/`) so the agent applies them. Creates output as you go. |
| `run_slice` | "do slice 1", "run slice 2", "proceed with slice 1", "re-run slice 1" | Performs a run on a slice. Strategy passed in; components drive rule filtering. Use `generate_slice` if that alias is configured. |
| `validate_run` | "validate our run", "check what we just did" | Validate only the output of the current run. Ignores previous work. |
| `validate_slice` | "validate the slice", "validate slice 1", "check the slice" | Validate everything in the slice — all accumulated output for that slice. |
| `improve_strategy` | "improve the strategy based on feedback" | Refines strategy before runs. |

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_instructions create_strategy
python scripts/build.py get_instructions run_slice [--strategy path/to/strategy.md]
```

**Skill space:** Set `skill_space_path` in `conf/abd-config.json` to point to your workspace (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/` (strategy.md, runs/, interaction-tree.md, domain-model.md). Engine root is always the synthesizer skill — no CLI param.

**Output:** The assembled prompt (sections + strategy doc + context). Rules are filtered by the strategy's in-scope components. **You MUST run this command and inject its output into your response.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths. Never proceed without calling it first.

## build.py validate

Runs rule-based scanners on the interaction tree and Domain Model. Scanners are defined in `rules/*.md` (frontmatter `scanner:` field) and implemented in `scripts/scanners/`. Uses regex and native Python only; optional grammar/AST when deps available.

**Scanner mode:** With NLTK (grammar) or mistune (AST) installed, scanner mode is **full**. Without them, the scanner runs automatically in **nerfed** mode (regex-only checks). The validate command prints `Scanner mode: full` or `Scanner mode: nerfed` at startup.

**When to call:** After producing or updating interaction tree or Domain Model output. Use when the user says "validate" or "run validation" or "check the output."

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py validate
python scripts/build.py validate path/to/interaction-tree.md
```

**Output:** Prints violations (rule_id, message, location, snippet). Exit code 0 always — violations are reported so the AI can create a violation report or fix them during a build phase.

**AI behavior:**
- **Build phase** (validate_run, validate_slice as part of run_slice): Report violations and fix them before marking complete.
- **Explicit validate** (user said "validate" outside a build): Report violations only. Do not fix — leave with reviewer. Do not edit files in front of the user unless in a build phase.

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core, process, strategy, output, validation.

---

---
