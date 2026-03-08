# Strategy Phase

<!-- section: story_synthesizer.strategy.phase -->
## Purpose

The synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

## Process

1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed initial breakdown, assumptions, **comprehensiveness criteria**, **identification criteria**, **proposed traversal order criteria(slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `<skill-space>/story-synthesizer/strategy.md`.

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

**What are we synthesizing context into?** Be specific about the typical criteria for each mode. Criteria must match the node types at each level — see `core.md` and `output/interaction-tree-output.md` for field definitions.

| Mode | Node levels | Fields per node |
|------|-------------|-----------------|
| **Shaping** | Epics (can nest), Stories. Stopping point: story. | Epic: Name (verb-noun), Initiating-Actor, Responding-Actor, Constraints. Story: Name (verb-noun), Initiating-Actor, Responding-Actor, Constraints. Short names and actor only. |
| **Discovery** | Epics, Stories. Same levels as Shaping; stopping point: story. | Epic: Shaping fields + domain concepts (`**Concept**`), Pre-Condition, Initiating-State, Resulting-State, Initiation (Behavior, Initiating-Actor), Response (Behavior, Responding-Actor), Constraints. Story: same. State Model with concepts. |
| **Exploration** | Steps (below story). | Step: Initiation, Response, Constraints (when step-specific). Steps not grouped into scenarios. No error conditions or edge cases. Straight and linear. |
| **Walkthrough** | Stories. | Domain walkthrough on stories — no new node fields. |
| **Specification** | Steps, Scenarios (below story). | Step: Initiation, Response, Examples, Constraints (when step-specific). Steps grouped into scenarios. Failure-Modes (failure conditions). |

**Constraints:** Any node can have one or more constraints (sentence, file reference, or markdown reference). Inherited high to low. Typically at epic or story level; may appear in steps.

**Step format:** When steps are in scope, specify the format for step text:
- **When/Then** — strict BDD: Initiation as When, Response as Then (e.g. `When **User** browses countries; Then **System** displays list of **Country** options`).
- **Vanilla steps** — verb-noun: short labels (e.g. `User submits form`, `System validates payment`).

These are artificial distinctions — we can say any of these elements. The strategy must state which mode(s) apply and what is in scope.

### 2 - Identification Criteria

**How do we identify anything in the model?** Come up with criteria ahead of time for what parts of the context map to what we want to build. State your identification criteria and reasoning so the user can adjust. Include examples of wrong vs right identification.

#### Epics vs Stories

An **epic** groups related stories; a **story** is the smallest independently deliverable unit of value. Identify separate stories when any of these differ:

| Discriminator | Meaning | Example |
|---------------|---------|---------|
| **Data structure of the concept** | The domain concept has different attributes, lifecycle, or relationships. | "Configure Physical Product" vs "Configure Digital Product" — different attributes (shipping, weight vs download, license). "Drive Car" vs "Drive Bicycle" vs "Ride Motorcycle" — different operational structure (engine, gears, fuel vs pedals, chain vs throttle, balance). |
| **Different business rules** | The logic, validation, or constraints differ. | "Validate payment legality in U.S." vs "Validate payment legality in Canada" — same outcome (legal payment) but rules, regulations, and laws differ so much by jurisdiction that separate stories are needed. |
| **Different underlying workflow** | The sequence of actions, approvals, or state transitions differs. | "Submit for approval" vs "Auto-approve under threshold" — different workflow paths. |
| **Different channels** | The touchpoint or interface differs (web, mobile, API, batch, etc.). Identify when channel affects behavior or constraints, or when built at different times or by different teams. | "Checkout via web" vs "Checkout via mobile app" — identify if channel affects behavior or constraints, or if web and mobile are delivered in different increments or by separate teams. |
| **Different systems / crossing boundaries** | The interaction crosses a system boundary or involves a different backend. | "Sync inventory from warehouse" vs "Update local stock" — one crosses systems, one is local. |
| **Different resulting state** | The outcome or state change is distinct. | "Successfully process payment" vs "Forward payment to manual intervention" — same initiation (process payment) but the logic differs so much by outcome that separate stories are needed. |
| **Different user roles** | Different actors or authorization levels change the interaction. | "Manager performs transaction" vs "Executive performs transaction" — same transaction type, but Manager requires approval while Executive does not; the role changes the flow. |
| **Different failure modes** | The ways the interaction can fail are distinct. | "Submit claim — rejected for missing docs" vs "Submit claim — rejected for policy exclusion" — same initiation, but failure handling differs so much (upload flow vs no remediation) that separate stories are needed. |
| **Expand distinct outcomes** | Same initiation, but resulting state and logic differ so much that one story would be too coarse. | "Successfully process payment" and "Forward payment to manual intervention" from "process payment." |

#### Steps

A **step** is one atomic initiation and response. Identify separate steps when:

| Discriminator | Meaning | Example |
|---------------|---------|---------|
| **Explicit action-reaction** | One discrete event — a single initiation and its response. | One step = one user action + one system response. Not "User enters details and submits" when validation and submission are separate events. |
| **Actor or response changes** | The initiating or responding actor changes, or a different user action or system response occurs. | **Wrong:** One step "User enters details and submits" when validation and submission are separate system responses. **Correct:** Step 1: "User enters details" (Then system validates). Step 2: "User submits" (Then system confirms). |
| **Enumerate all permutations** | List all validation paths, calculation branches, and edge cases. Cover happy path, error path, and boundary conditions. | **Right:** When valid rank → calculates modifier; When invalid rank → shows error; When boundary rank → handles edge case. **Wrong:** Only "When user enters rank → system saves" (missing validation error, boundary). |


#### Scenarios

A **scenario** groups steps that share a path through the story. Split scenarios when:
- Pre-conditions differ (e.g. new user vs returning user)
- Success vs failure paths
- Different branches of the same workflow

#### Domain Concepts

Concepts are the things that hold state and get operated on. Identify concepts when:
- Different lifecycle (e.g. Draft vs Submitted Order)
- Different ownership or responsibility
- Different persistence or scope
- Different properties or operations

#### Examples

Examples are concrete state tables that illustrate a concept. Identify from:
- Boundary values (min, max, empty)
- Distinct scenarios (success, invalid, not-available)
- Representative combinations from the steps and state

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
