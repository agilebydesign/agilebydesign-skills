# Core Data Model

## What the Story Synthesizer Does

The story synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

Your task is to **synthesize** source material into an **Interaction Tree** and **State Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. Outputs: story map, domain model, acceptance criteria, specifications, walkthroughs.

**Hierarchy:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). Epics group stories; the story is the backbone — the smallest unit that is both valuable and independently deliverable. Each story has Pre-Condition, Initiation, Response, and statement. Scenarios optionally group steps; steps are atomic interactions.

**State** runs alongside. Pre-Condition is what must be true before; Response implies resulting state. Domain concepts (the things that hold state and get operated on) are referenced via `**Concept**` in labels; each must exist in the State Model. Tree and State Model evolve together — no drift.

---

All concepts are defined below. See the output folder: `output/interaction-tree-output.md` and `output/state-model-output.md` for format and presentation.

<!-- section: story_synthesizer.core.interaction -->
## Interaction Model

An interaction is a single meaningful exchange between two actors that results in either a retrieval of state or a change of state.

### Interaction

- **Name** — name of the interaction. **Ground in domain:** Every epic, story, scenario, and step must be grounded in domain language — either in the name or in the statement — using `**Concept**` (double stars, capitalization). Domain concepts must appear in `**Concept**` format so the domain conditions are described.
- **Statement** — one-sentence initiation and response; include state concepts where appropriate.

**Name and statement (all nodes):** Use active verb language. Short name first, longer statement in brackets. Format: `Node: Short Name (Longer statement.)` — e.g. `Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays...)`. Name is always verb-noun or subject-qualifier; statement is always the longer sentence. **Epic statement:** Describe the scope of the epic (broad flows), not a single interaction. **Story/Step statement:** One initiation and response.
- **Impacts** — zero or more (see Impact below)
- **Pre-Condition** — label only. What must be true before. State qualifies through the label. Use `**Concept**` to reference domain concepts; each must exist in the State Model.
- **Initiation** — Initiating-Actor, Behavior (label), Initiating-State. Initiating-State is any state that qualifies the interaction (e.g. selecting an option of a certain type). Labels reference domain concepts; examples live on the interaction.
- **Response** — Responding-Actor, Behavior (label), Resulting-State. Resulting-State is the state that results from the interaction. Labels reference domain concepts; examples live on the interaction.
- **Examples** — collection of tables at the interaction level. One per concept referenced in labels. Pre-Condition, Initiation, and Response reference these through their labels; examples live on the interaction.
- **Failure-Modes** — up to three; how the exchange can fail (rule/state based only)
- **Children** — child interactions of this interaction.

#### Interaction Tree Rules
**Node Hierarchy**
- Epic - Can nest to have epic children or story children. An epic whose parent is an epic is sometimes called a sub-epic. Names are typically simple verb-noun.  
- Story - Smallest unit of testable value that is independently delivered. Names are typically simple verb-noun.  
- Scenario - Groups steps; optional container for a story. Names describe the primary conditions tested in the scenario.  
- Step - Atomic interaction within a scenario. Steps are interactions: often in the form of **Initiation** (When) and **Response** (Then). 

Epic → children (Epics, Stories)  
Story → Scenarios OR Steps
Scenario → Steps  
Step --> lowest interaction for now

**Commonly Generated Fields Vary By Node Type:** 
Any node level can use any field. Exceptions are always possible. The table below lists what we commonly generate for each node.

| Node | Commonly generated | Case By Case Generated |
|------|--------------------|------------------------|
| Epic | Initiating-Actor, Responding-Actor, Name (Verb Noun), Impact | Pre-Condition, Initiating-State, Resulting-State, Examples, Failure-Modes|
| Story | Initiation , Response ; Name (Verb Noun), Examples, Pre-Condition (eg BDD backgroun, Given, And); Failure-Modes, |
| Scenario | Initiation, Response, Pre-Condition (eg BDD Given, And); Examples |
| Step | Initiation, Response,(When, And, Then, And); Examples |

**Nodes inherit attributes from their parents.** 
Child nodes inherit state, examples, pre-conditions, actors, and domain concepts. You can show inherited attributes explicitly in square brackets (e.g. `Initiating-Actor: [User]`, `Examples: [Logged In User, Active Session]`) so readers see which values came from the parent. When you use brackets, update them if the parent changes. **Inheritance applies either way** — even when you don't show brackets, the inherited values still apply to the child. See Hierarchy Inheritance for conventions.

**Inheritance that we often want to call out explicitly through the [inherited thing] notation**
- **Epic from Epic:** Domain concepts. Lower-level epics (sub-epics) often use the inherited domain concepts from their parent epic.
- **Story from Epic:** Initiating-Actor, Responding-Actor, Pre-Condition, Examples based on Pre-Condition, domain concepts.
- **Scenario from Story:** Almost nothing needs to be explicitly stated.
- **Step from Story:** Initiating-Actor and Responding-Actor are often used, eg [User] and [System] from the story or higher. Exception: when a step is system-initiated (e.g. "When **System** receives payment type selection"), that step may override Initiating-Actor.

**Domain grounding:** Every epic, story, scenario, and step must be grounded in domain language. This primarily comes from the interactions (e.g., initiation and response) if they have been defined, but if they have not been defined, then it would come from the  the name or  the statement. When When initiation and response have been defined, the name is based on those, but sometimes we don't define these for a node, and just define the name at first. In either case, all of the above need to be grounded using `**Concept**` (double stars on both sides, capitalization). Avoid generic terms; use `**Country**`, `**PaymentType**`, etc., not "country" or "payment type". Concepts must come from the state model here. Concept identified as part of exploring the interaction tree should be added to the state model and vice versa. When we add things to the state model, we should explore which interactions require those and update accordingly.

Concepts are placed at the level of the interaction hierarchy where they apply to all descendants. Every `**Concept**` must exist in the State Model — no drift.

### State

State qualifies an interaction through its **label** — a description of the condition. The interaction's **Examples** (tables) live on the interaction; example and label reference the domain concepts that correspond to those tables.

### Pre-Condition
 What must be true before the interaction. Label only (may use Given/And BDD format). Examples live on the interaction.

### Initiation 

Who starts the interaction and what they do.

- **Initiating-Actor** — who starts the interaction
- **Behavior** — the label. Describes the action. Use When/And for steps, Given/When/Then for BDD, or verb-noun as appropriate.
- **Initiating-State** — state that qualifies the interaction (e.g. selecting an option of a certain type). Labels reference domain concepts; examples live on the interaction.

### Response (Then)

Who responds and what they do.

- **Responding-Actor** — who responds (typically system, subsystem, or component)
- **Behavior** — the label. Describes the response. Use Given/When/Then for BDD, or verb-noun as appropriate.
- **Resulting-State** — the state that results from the interaction. Labels reference domain concepts; examples live on the interaction.

### Impact

Applies to Epic, Story. An interaction may have an impact; a known result can provide evidence for another impact (tie a hypothesis to a result).

- **Type** — user | economic | feasibility
- **Status** — hypothesis (we don't know yet) | result (measured outcome for an existing system)
- **Description**
- **Evidence-Ref** — optional; links to another impact that is a result



## State Model

The State Model holds **modules** (groupings of tightly related concepts) and **domain concepts** — the things that have state and can be operated on. Concepts are referenced in interactions via `**Concept**` in Pre-Condition, Initiation, Response, and Failure-Modes. Every `**Concept**` must exist in the State Model; concepts must be placed at the right level in the hierarchy. No drift between tree and model. Use source entity data, not aggregated/calculated values.

### Module

Grouping of tightly related concepts.

- **name** — module name
- **concepts** — list of tightly related StateConcepts

<!-- section: story_synthesizer.core.state_concept -->
### State Concept

A domain concept that holds state and can be operated on. Referenced in interactions via `**Concept**` in labels. Examples live on the interaction.

- **Name**
- **Module** — optional; grouping of tightly related concepts
- **Base-Concept** — optional
- **Properties** — with optional collaborating concepts and invariants
- **Operations** — with optional collaborating concepts and invariants  ; It should be easy to reverse engineer the interactions in the interaction diagram to at least some level of operations on the state model.
---

## Hierarchy Inheritance

Attributes from a parent node are inherited by child nodes. **Brackets indicate inherited values.** Use `[value]` or `[inherited]` so readers see what applies at each level; if the parent changes, update bracketed values in children.

**Inherited attributes:** Examples, actors. Place concepts at the lowest level where they apply to all descendants. Concepts are indicated by `**Concept**` in labels — no separate list.

**Convention:** `Initiating-Actor: [User]`, `Responding-Actor: [System]` — brackets mean "from parent." Unbracketed values are defined on this node. Use Title Case for field names; hyphens for compound terms (e.g. Pre-Condition); no dot notation.

**Guidelines for inherited values:**
- **Statement by level:** Epic statement describes the *scope* of the epic — the broad flows it encompasses — not a single interaction. Use `**Concept**` to ground in domain. Good: (**User** initiates **PaymentType** flows that vary by **Country**; **System** validates and executes per **Country**.) Bad: (**User** selects **Country** and **PaymentType**; **System** validates.) — that describes one story, not an epic. Story statement: one initiation and response. Step statement: When/Then for that step.
- **Pre-Condition:** Never use `Pre-Condition: [inherited]` alone. Always include the label (bracketed) so readers see what applies.
- **Initiating-Actor / Responding-Actor:** Use `[User]` or `[System]` at every initiation/response so the actor is visible without looking up. Use Title Case; no dot notation (e.g. `Initiating-Actor`, not `initiation.actor`).
- **Examples:** Live on the interaction. Use `[inherited]` when tables come from parent; list the qualitative names (e.g. `[Logged In User, Active User Session, User Payment Type Access]`). Include step-specific or story-specific examples unbracketed.
- **Example table names:** When you have data, you need a label. Name by state or condition — "Selected Country", "Selected PaymentType", "Approved Payment" — not generic labels like "Payment" or "Country". For mapping tables use descriptive names (e.g. "Payment Type Field Types"). When data varies by type, include the type (e.g. "PaymentDetails (wire)"). When multiple tables for the same concept appear in one step, add a qualifier in parentheses (e.g. "Selected PaymentType (selected, not available for country)"). When inherited, list those names: `examples: [Logged In User, Active User Session, User Payment Type Access]`.
- **Example scenario column:** Use a scenario column to map example rows to outcomes. Use kebab-case consistently (e.g. success, invalid-payment-details, payment-type-not-available).
- **Example block format:** Use `===` between tables. No blank lines between tables. Tables require a header separator row (`|---|---|`). Pattern: `Name:\n| col1 | col2 |\n|---|---|\n| data | data |\n===\nNext name:\n| table |`.

**Rule:** Put shared concepts at the epic level; only add story-specific concepts at the story level. Epic holds initiation state for rules that apply to all children (e.g. user access to payment types by country). Epics (including epic children of epics) group; they do not add initiation/response state. Stories inherit Pre-Condition, Initiating-Actor, and Responding-Actor from Epic.

**Placement rule:** Only put something at a level if it applies to every descendant. If a failure mode, concept, or rule applies only to specific scenarios or stories, place it on those nodes — not at the Epic.

---

## Complete Example

A typical reference hierarchy for making a country-specific payment (initiate, make transaction, fulfill). **Concepts** are referenced via `**Concept**` in labels. **Examples** live on the interaction. Pre-Condition, Initiation, and Response qualify through their labels. Epic holds rules that apply to all children (e.g. user access to payment types by country). Epics group; they do not add initiation/response state. Stories inherit from Epic. One story is taken to full detail with scenario and steps. (Other epics and stories not yet filled out.)

**Hierarchy levels:** Epic → Story → Scenario → Step (epics can nest; an epic child of an epic is sometimes called a sub-epic)

**Name and statement:** Active verb language, short name first, statement in brackets (see Interaction).

### Hierarchy

#### Epic: Make **Country**-specific **PaymentType** (**User** initiates **PaymentType** flows that vary by **Country**; **System** validates and executes per **Country**.)
- Initiating-Actor: User
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

  #### Story: **User** Initiates **Country**-Specific **PaymentType** (**User** determines **Country** and **PaymentType**; **System** validates and confirms.)
  - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
  - Failure-Modes:
    - validation errors (invalid **PaymentDetails**)
    - payment type not available for **Country** (see **UserPaymentAccess**)
  - Initiation:
    - Initiating-Actor: [User]
    - Behavior: **User** determines **Country** and **PaymentType**
  - Response:
    - Responding-Actor: [System]
    - Behavior: validates **PaymentDetails** and confirms success

  ##### Scenario: Success — payment validated and confirmed

  ###### Steps

  - Step 1: Browse Country for Payment (When **User** browses countries; Then **System** displays list of **Country** options available for **PaymentType**)
    - Initiation:
      - Initiating-Actor: [User]
      - Behavior: browses countries
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays list of **Country** options available for payment

  - Step 2: Select Country and Display Payment Types (When **User** selects **Country**; Then **System** displays all available **PaymentType** options for that country)
    - Initiation:
      - Initiating-Actor: [User]
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
    - Initiation:
      - Initiating-Actor: [User]
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
    - Initiation:
      - Initiating-Actor: [System]
      - Behavior: receives payment type selection
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays **PaymentDetails** with fields from **PaymentTypeFieldTypes** for the selected **PaymentType**

  - Step 5: Make Payment and Successfully Validate It (When **User** enters valid **PaymentDetails** and submits; Then **System** validates the payment and confirms success)
    - Initiation:
      - Initiating-Actor: [User]
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
    - Initiation:
      - Initiating-Actor: [User]
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
    - Initiation:
      - Initiating-Actor: [User]
      - Behavior: browses countries
    - Response:
      - Responding-Actor: [System]
      - Behavior: displays list of **Country** options available for payment

  - Step 2: Select Country and Attempt Unavailable Payment Type (When **User** selects **Country** where a **PaymentType** is not available; And **User** selects that **PaymentType** and clicks start payment; Then **System** indicates payment type not available for that country)
    - Initiation:
      - Initiating-Actor: [User]
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
    - Initiating-Actor: [User]
    - Responding-Actor: [System]

  #### Story: **User** submits **PaymentDetails** for **Country**-specific **PaymentType**
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Initiating-Actor: [User]
    - Responding-Actor: [System]

  #### Epic: Fulfill **Payment** settlement
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Initiating-Actor: [User]
    - Responding-Actor: [System]

  #### Story: **User** completes **Payment** settlement
    - Pre-Condition: [Given **User** is logged in; And **User** has an active **Session**; And **User** has access to **PaymentType** in **Country** (see **UserPaymentAccess**)]
    - Examples: [Logged In User, Active User Session, User Payment Type Access]
    - Initiating-Actor: [User]
    - Responding-Actor: [System]

---

# Process Overview

<!-- section: story_synthesizer.process.intro -->
Your task is to **synthesize** context into an **Interaction Tree** and **State Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them. In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Synthesis can stop at the story level; details are flushed out later.

Each rule has a DO with example and a DO NOT with example.

**You MUST follow this process.**
When the user says "create the story map," "proceed," "build it," "generate the output," or similar, you **MUST begin with the Strategy Phase**. Do not skip to producing the full output.

1. **Strategy Phase first** — Analyze the source, propose Epic/Story breakdown and slice order, save the strategy. Do not produce an interaction tree until the strategy is approved.
2. **Work in runs** — Each run produces output for a slice (4–7 stories typical). A run may require **multiple iterations**: user reviews, finds mistakes, you add corrections to the **run log**, re-run. Repeat until the user approves. Only then proceed to the next run.
3. **No full output in one go** — Do not produce a complete interaction tree in a single pass. Iterate run by run.
4. **Review and Adjust** - Once all runs are done, have the AI review all corrections collected in the **run log** and determine what needs to change in the rules and/or instructions. Promote those that apply across projects  to the skill's rules.

## Output Paths (default)

- **Strategy:** `<skill-space>/story-synthesizer/strategy.md`
- **Output:** `<skill-space>/story-synthesizer/` — Interaction Tree and State Model (format in `output/interaction-tree-output.md` and `output/state-model-output.md`)
- **Runs:** `<skill-space>/story-synthesizer/runs/` — run logs (one file per run, e.g. `run-1.md`)

**Runs** — Each run is a purposeful loop: it defines how much detail to synthesize, where to stop (epics vs stories vs steps), and produces output. We track runs, not slices. Each run writes a run log. **Corrections go to the run log** (the run's Corrections section), not to the strategy. See `run-output.md` for format;

## Slices and Runs

- **Slice** — A collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope.
- **Run** — A purposeful loop to perform the next increment of our strategy. Each run defines in how much detail we will be synthesizing, where we stop (e.g., at epics or at stories), tracks the output of the step in the process, is used to track progress, and produces a slice of output. A run can stop at epics and not stories — we have explicit control over the stopping point.

### Run Log

Each run writes a **run log** to its own file. The log records Before, After, and Corrections. See `run-output.md` for structure and format.

This gives better granularity for improving things over time — run logs can be fed into an agent, analyzed for patterns, or used to refine the strategy.

### Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the run's stopping point (e.g., 4–7 stories if stopping at stories; epics and sub-epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a **DO** or **DO NOT** to the **run log** (the run's Corrections section). Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the slice; update the run log with the new Before/After and any additional corrections; repeat until the user approves
3. **Next slice** — Proceed to the next slice. Same pattern: produce → review → corrections to run log → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

These paths can be configured under the skill-space config (`abd-config.json` or equivalent) so the user can choose where files go and what they are named.

## Process Checklist

- [ ] **Strategy Phase complete** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `<skill-space>/story-synthesizer/strategy.md`
- [ ] **Strategy approved by user** — Do not produce an interaction tree until then
- [ ] **Run 1 produced** — Output for first slice; run log written to `runs/run-1.md`
- [ ] **Run 1 iterated to approval** — User reviews; when mistakes are found, add DO/DO NOT to the **run log** Corrections section (with wrong/correct examples); re-run taking corrections into account; repeat until user approves
- [ ] **Post-synthesis review** — Review all corrections collected in run log; determine what needs to change in rules/instructions; promote reusable corrections to strategy and/or skill
- [ ] **Next run** — Proceed to next slice;or conduct another run to go deeper on same slice; same iteration pattern (produce → review → corrections to run log → re-run until approved)

---

# Strategy Phase

<!-- section: story_synthesizer.strategy.phase -->
## Purpose

The synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

## Process

1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed initial breakdown, assumptions, **comprehensiveness criteria**, **identification criteria**, **proposed traversal order criteria(slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `<skill-space>/story-synthesizer/strategy.md`.

## Slices and Runs

- **Slice** — A collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope.
- **Run** — A purposeful loop to perform the next increment of our strategy. Each run defines in how much detail we will be synthesizing, where we stop (e.g., at epics or at stories), tracks the output of the step in the process, is used to track progress, and produces a slice of output. A run can stop at epics and not stories — we have explicit control over the stopping point.

### Run Log

Each run writes a **run log** to its own file. The log records Before, After, and Corrections. See `run-output.md` for structure and format.

This gives better granularity for improving things over time — run logs can be fed into an agent, analyzed for patterns, or used to refine the strategy.

## Interaction Hierarchy

Interactions exist at **all levels** of the hierarchy. **Hierarchy:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). The hierarchy goes from high-level epic (coarse interaction) down through nested epics to stories, and below stories to scenarios and steps. Domain concepts are often inherited: sub-epics use inherited concepts from their parent epic; stories very rarely define domain concepts — they inherit from the epic. See `core.md` for inheritance patterns and Initiating-State / Resulting-State.

### The Story as Backbone

The **story** is the backbone of all the work above and below it. It is the central unit that everything connects to.

- **Above the story:** Epics and sub-epics exist only to **group stories together**. They are organizational structure, not the primary unit of value.
- **Below the story:** All steps, examples, and scenarios **belong to the story**. The story is the central spoke — everything below it hangs off the story.

**What a story is:** A story is something we can reasonably discuss as a valuable tactical interaction between the user and the system (or between systems). It is something that can be developed in a small amount of time — typically a couple of days for a developer (or a couple of hours for AI :). It is the smallest unit that is both valuable and independently deliverable. It needs to be testable, which means it must have a recognizable behavior that a user or stakeholder would recognize. Not necessarily always user-facing, but at least recognizable as a tangible business state that's changed or logic has been executed here.

**Stopping point:** The story is typically the stopping point **for Shaping and Discovery**. For Exploration, Walkthrough, and Specification, we go below the story (to steps, examples, scenarios). With slices and runs, *we have explicit control on the stopping point*: a run on a slice of a couple of epics can have criteria to only identify other epics and not stories. The stopping point is configurable.

## Impacts

An interaction may have an **impact**. Impacts apply at any level of the hierarchy. See `core.md` for the full Impact data model (types, status, evidence linking).

**Example:** Epic "User checks out" has impact hypothesis: "Reduces cart abandonment by 15%." Story "Apply discount code" has result: "In pilot, 12% of users who applied a code completed checkout." The result becomes evidence for the hypothesis.

## Strategy Criteria

<!-- section: story_synthesizer.strategy.criteria -->
### 1 - Comprehensiveness Criteria

**What are we synthesizing context into?** Be specific about the typical criteria for each mode:

| Mode | What we produce |
|------|-----------------|
| **Shaping** | Epics (can nest), Stories. Short names and actor. |
| **Discovery** | Shaping (or take what was shaped) + domain concepts (`**Concept**`), Pre-Condition, Initiating-State, Resulting-State, Initiation (Behavior, Initiating-Actor), Response (Behavior, Responding-Actor). |
| **Exploration** | Steps, not grouped into scenarios. No error conditions or edge cases. Straight and linear. |
| **Walkthrough** | Domain walkthrough on stories. |
| **Specification** | Examples. Steps grouped into scenarios. Failure conditions. |

These are artificial distinctions — we can say any of these elements. The strategy must state which mode(s) apply and what is in scope.

### 2 - Identification Criteria

**How do we identify anything in the model?** Come up with criteria ahead of time for what parts of the context map to what we want to build.

- **Stories:** How do we find epics vs stories? What distinguishes an epic (including nested epics) from a story?
- **Steps:** What constitutes a good step? Too many vs too few?
- **Examples:** How do we identify examples from the steps and the state?
- **Domain objects and relationships:** How do we identify concepts, their properties, and their relationships?

State your identification criteria and reasoning so the user can adjust. Include examples of wrong vs right identification.

**Example (wrong):** Treating "User logs in" and "User logs out" as one story because they share the same actor.
**Example (correct):** Separate stories — different initiation, different resulting state, different failure modes.

### 3 - Traversal Order (Slices)

The order in which you work through slices is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

**Ideas for prioritizing slices:**
- Architectural slice — Stories that establish the architecture
- Domain slice — Stories aligned by common business logic
- Integration slice — Stories across integration points
- Workflow slice — End-to-end workflow for a particular use case
- Value slice — Stories that provide the most value if done first
- Risk slice — Stories that de-risk some aspect of the solution

Favour slicing vertically, often by a common theme or category of complexity. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

<!-- section: story_synthesizer.strategy.slices.running -->
## Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the run's stopping point (e.g., 4–7 stories if stopping at stories; epics and sub-epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a **DO** or **DO NOT** to the **run log** (the run's Corrections section). Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the slice; update the run log with the new Before/After and any additional corrections; repeat until the user approves
3. **Next slice** — Proceed to the next slice. Same pattern: produce → review → corrections to run log → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

<!-- section: story_synthesizer.strategy.corrections -->
## Corrections Format

When adding corrections to the run log (Corrections section), each **DO** or **DO NOT** must include:
- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the slice until the user approves. Corrections stay in the run log; the post-synthesis review promotes reusable ones to strategy or rules.

When analyzing **existing content**, review and follow the strategy.

### Object Model Correction

**DO** — Inject the Engine (or context provider) into components that need it. Use properties over getters. Encapsulate over passing parameters — components pull context from injected dependencies instead of receiving it as method arguments.

- **Example (wrong):** `AbdSkill.get_instructions_for(operation, context)` — context passed as parameter.
- **Example (correct):** AbdSkill has `Engine engine` (injected); `instructions` property; assembles using `engine.workspace`, `engine.strategy_path` when needed.

### Skill Update Workflow

**DO** — Update the abd-story-synthesizer skill in `agilebydesign-skills/skills/abd-story-synthesizer/` first (core); then copy those updates to test installations as needed.

- **Example (wrong):** Editing the skill only in a test project; creating standalone scripts in test without updating core; core and test copies drift.
- **Example (correct):** Edit `agilebydesign-skills/skills/abd-story-synthesizer/`; run build; copy updated files to the test project's copy.

---

<!-- section: story_synthesizer.output.interaction_tree -->
# Interaction Tree Output

Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

---

# Epics and Stories View (Hierarchy)

The tree view: Epic → Epic/Story children. Each node shows name, actors, and inherited vs own fields.

# Epic (filled out — has Examples)

- Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- `- Initiating-Actor:` value
- `- Responding-Actor:` value
- `- Pre-Condition:` full label (Given/And)
- `- Examples:` state table block (see Example Block Format below)

## Epic (not filled out — inherits only)

- Heading: `## Epic: <name using **Domain Concepts**> (<statement>)`
- `- Pre-Condition:` [full inherited label]
- `- Examples:` [list of inherited state table names]
- `- Initiating-Actor:` [User] (or other actor)
- `- Responding-Actor:` [System] (or other actor)

### Story (filled out — has Initiation, Response, Failure-Modes, Scenarios)

- Heading: `### Story: <name using **Domain Concepts**> (<statement>)` — same pattern as Epic
- `- Pre-Condition:` [inherited]
- `- Failure-Modes:` bullet list (up to 3)
- `- Initiation:` sub-bullets Initiating-Actor, Behavior
- `- Response:` sub-bullets Responding-Actor, Behavior
- `###### Scenario:` name
- `####### Steps`
- Step items (see Story Details View)

### Story (not filled out)

- Heading: `#### Story:` + **Name**
- `- Pre-Condition:` [inherited]
- `- Examples:` [inherited table names]
- `- Initiating-Actor:` [inherited]
- `- Responding-Actor:` [inherited]

---

# Story Details View (Drill-down)

When a story is expanded: Scenarios, Steps, and per-step Initiation/Response/Examples.

## Step (no Examples)

- `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- `- Initiation:` [inherited], Behavior
- `- Response:` [inherited], Behavior

## Step (with Examples)

- Same as Step (no Examples), plus `- Examples:` block
- Each table: label, blank line, header row, separator row, data rows
- Each table is a separate block; blank line between tables

## Step (system-initiated)

- Initiating-Actor overridden to [System] when the step is system-initiated (e.g. "When **System** receives...")

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

<!-- section: story_synthesizer.output.state_model -->
# State Model Output

Separate from the Interaction Tree. Concepts referenced via `**Concept**` in labels. Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

## Format

```
Concept : <Base Concept if any>
- <type> property
      <collaborating concepts if any>
- <type> operation(<param>, ...)
     <collaborating concepts if any>
- Interactons Interaction Concept used by (root node only)
- examples: list of state concept tables in interaction tree using this concept
```

---

# Run Output

Each run writes a run log to its own file. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/runs/run-N.md` (N = run number). Configurable via skill-space config.

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
The DOs and DON'Ts added during this run. Each time the user finds a mistake, add a new correction here (do not add to strategy). Each correction includes:
- The rule
- Example (wrong)
- Example (correct)
```

Run logs are used to track progress, feed into agents, analyze patterns, or refine the strategy. The post-synthesis review promotes reusable corrections from run logs to the strategy or skill rules.

---

# Validation Pass

<!-- section: story_synthesizer.validation.checklist -->
## Validation Checklist

After generating interactions and concepts, verify against the output format in `output/interaction-tree-output.md` and `output/state-model-output.md`.

---

## Interaction Tree

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Initiating-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state
- [ ] Examples: state table block or `Examples: [Table Name 1, ...]` when inherited

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Initiation, Response present
- [ ] Initiation: sub-bullets Initiating-Actor, Behavior (no state language in Behavior)
- [ ] Response: sub-bullets Responding-Actor, Behavior (no action language in outcome)
- [ ] Scenario and Steps when in scope

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Initiation and Response with [inherited] when from parent
- [ ] System-initiated steps override Initiating-Actor to [System]

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

AI guidance for calling abd-story-synthesizer scripts.

## build.py get_instructions

Gets the assembled prompt for an operation from the Engine. **Call this before producing any shaping output.**

**When to call:** When the user requests:
- `generate_slice` — "do slice 1", "generate the first slice", "proceed with slice 1", etc.
- `create_strategy` — "create the strategy", "analyze and propose breakdown", etc.
- `improve_strategy` — "improve the strategy based on feedback", etc.

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_instructions generate_slice
```

**Output:** The assembled prompt (sections + strategy doc + context). **Inject this output into your response and follow it.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths.

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
