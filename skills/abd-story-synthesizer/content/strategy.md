# Iterative Strategy

<!-- section: story_synthesizer.strategy.iterative -->
## Purpose

The synthesizer skill helps you take context and synthesize it into **stories** that explain how a user engages with a solution or system(s) to create value. Stories are about **interaction**, but also about **structure**, **state**, and **rules**.

## Process

**Strategy is part of every run.** Early runs focus on strategy and doing enough identification to spot patterns that lay out future slices, order, and size. All runs should examine all runs from the perspective of a new pattern — if found, add the pattern to the strategy. Runs get richer as we go.

1. **First run** — Analyze the source, create the strategy document, build enough of the tree and Domain Model to spot patterns, extrapolate. Save to `<skill-space>/story-synthesizer/strategy.md`.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed initial breakdown, assumptions, **comprehensiveness criteria**, **identification criteria**, **proposed traversal order (slices)**, **patterns** (as found).
3. **Validate until reasonable** — User reviews; refine until approved. Create the tree and Domain Model as you go. Iterative Strategy — it runs through every run.
4. **Every run** — After each run, examine all runs for new patterns. If found, add to the strategy's Patterns section.

### Strategy Document Structure

The strategy document (`strategy.md`) includes the criteria below plus a **Patterns** section. Add patterns as they are found during runs.

**Patterns section format** — For each run that yields a pattern:

| Run | What was built | Pattern found | Applicable to |
|-----|----------------|---------------|---------------|
| run-1 | Qualitative statement (e.g. "wrote steps and examples for all stories under epic X") | Brief pattern description | Scope where pattern applies (can be qualitative) |

**Example:** Run 2 built steps and examples for "Configure Power Effect" stories. Pattern: "Effect-type stories share same step structure — Configure, Validate, Apply." Applicable to: other effect types (Advantages, Skills) under the same epic.

## Interaction Hierarchy

The Strategy document will have **criteria** and **patterns** that refer to slices of the interaction model and domain model. Strategy links to those documents: `core.md` (hierarchy Epic → Story → Scenario → Step, nesting, inheritance, field definitions, story as backbone, stopping points), `output/interaction-tree-output.md`, and `output/domain-model-output.md`.

## Strategy Criteria

Criteria define what the synthesizer produces and how it identifies content from context. Every strategy needs criteria — without them, the AI and validation engine cannot know what to synthesize or which rules to apply.

<!-- section: story_synthesizer.strategy.criteria -->
### 1 - Comprehensiveness Criteria 

**What are we synthesizing context into?** Be specific about what tree and domain elelements we want to synthesize in the strategy. Criteria must specify node types and node attributes — see `core.md` and `output/interaction-tree-output.md` for field definitions.

Criteria can be either bespoke (i want to generate epics with examples...) or defined through "Modes" that represent different stages of refinement.

| Mode | Node levels | Fields per node |
|------|-------------|-----------------|
| **Shaping** | Epics (can nest), Stories. Stopping point: story. | Epic: Name (verb-noun), Initiating-Actor, Responding-Actor, Constraints. Story: same. Short names and actor only for most output. **When identifying patterns and slices:** use Discovery (domain concepts, Pre-Condition, Initiating-State, Resulting-State, Initiation, Response, Domain Model) — you need domain-level detail to distinguish stories and slice boundaries. |
| **Discovery** | Epics, Stories. Same levels as Shaping; stopping point: story. | Epic: Shaping fields + domain concepts (`**Concept**`), Pre-Condition, Initiating-State, Resulting-State, Initiation (Behavior, Initiating-Actor), Response (Behavior, Responding-Actor), Constraints. Story: same. Domain Model with concepts. |
| **Exploration** | Steps (below story). | Step: Initiation, Response, Constraints (when step-specific). Steps not grouped into scenarios. No error conditions or edge cases. Straight and linear. |
| **Walkthrough** | Stories. | Domain walkthrough on stories — no new node fields. |
| **Specification** | Steps, Scenarios (below story). | Step: Initiation, Response, Examples, Constraints (when step-specific). Steps grouped into scenarios. Failure-Modes (failure conditions). |

See `core.md` for constraints, step format, and the full field definitions. The strategy must state which mode(s) apply and what is in scope.

**How rules align:** Tags map this comprehensiveness to rule filtering. The strategy declares which tags are in scope; include a rule if any of its tags matches any in-scope tag. Tags can be declared by mode, by component, or explicitly — tags do everything.

**All runs get validated.** Validation is based on what you synthesize — different rules apply to domain concepts, steps, examples, scenarios, etc. If you're only shaping the tree, you get tree rules; if you're building steps and examples, you get step and example rules. These rules must be **injected based on tags in scope** — the engine filters rules by the strategy's declared tags so the AI receives only the rules that apply to what it's producing. Run `get_instructions` before producing output so the correct rules are injected.

| Tag | Description |
|-----|-------------|
| `shaping` | Coarse structure; epics and stories; names and actors only |
| `discovery` | Story-level detail: Initiation, Response, Pre-Condition, Initiating-State, Resulting-State |
| `exploration` | Steps below story; linear, no edge cases |
| `walkthrough` | Domain walkthrough on stories |
| `specification` | Steps, scenarios, examples, failure modes |
| `interaction_tree` | Epic/Story hierarchy; names, actors, constraints |
| `epic` | Epic-level nodes; hierarchy, granularity |
| `story` | Story-level fields: Initiation, Response, Pre-Condition, etc. |
| `domain` | Domain Model — concepts, Properties, Operations |
| `step` | Atomic Initiation/Response; When/Then or verb-noun |
| `step_edge_case` | Steps + Failure-Modes; error paths |
| `example` | Example tables per concept |
| `scenario` | Step grouping by path |

**Example declarations:** Mode-based `tags: [discovery]`; component-based `tags: [interaction_tree, story, domain]`; explicit `tags: [shaping, discovery, interaction_tree, epic, story, domain]`. **When no strategy or new pattern:** default to `tags: [shaping, discovery, interaction_tree, epic, story, domain]`.

### 2 - Identification Criteria

**How do we identify the interactions and state from the context?** Analyze the source to identify criteria that drive the identification. Identify elements based on:
- **Business rules** — distinct rules or conditions change behavior.
- **System interactions** — different systems or integration points change exchange pattern.
- **Workflows** — different sequences or paths change steps, actors, or outcomes.
- **Structure** — different concept shapes or taxonomies change the interaction.
- **State** — different state transitions or preconditions change required or resulting state.

**The process (identification, pattern matching, extrapolating):** Treat strategy like a run — create a few stories, create a few Domain Model samples, get the pattern, then go through memory chunks and say "more of same pattern" → X more stories. Repeat until patterns change. Patterns change in context based on different epics. **Identification criteria:** Different data structure, different business rules, or different workflow → separate story. Same pattern across chunks → "X more stories of this pattern."

**How shaping helps:** The **shaping rules** and **domain rules** that come from the injected instructions (from `get_instructions create_strategy`) guide this process. Apply them across memory chunks to build viable identification criteria and validate your identification against those rules. Come up with criteria ahead of time for what parts of the context map to what we want to build. State your identification criteria and reasoning so the user can adjust. Include examples of wrong vs right identification.

**DO** — When creating strategy, perform thorough verb-noun and OOAD analysis. Create a sampling with a common pattern: a few stories and Domain Model samples until a pattern is clear. Go through memory chunks and say "more of same pattern" → X more stories. Repeat until patterns change. Track potential patterns until you find others of the same; discard if they are one-offs. Patterns change in context based on different epics. We do not want deep OOAD and story analysis of every doc — we do that in runs — but we need enough pattern matching to create viable identification criteria. For example, handbook chapters may represent larger epics, likely with sub-epics. Power Effects, Advantages, bespoke skills, and similar high-complexity concepts often have many individual items that each warrant a separate story — analyze every memory chunk in depth.

- **Example (wrong):** Strategy with 3 epics, 6 slices, and high-level treatment (e.g. "Configure Power Effect" as one story).
- **Example (correct):** Strategy with chunk-by-chunk analysis, verb-noun discovery, Domain Model scaffolding per concept, pattern identification ("Pattern 1: Configure Effect — 24 stories grouped by structural similarity"), and explicit pattern-change boundaries by epic. Each effect type with distinct data structure gets its own story or grouped story.

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
## When User Gives a Correction

**Trigger phrases:** "wrong", "correction", "this is wrong", "strategy is wrong", "too superficial", "fix this", "redo", "try again"

**You MUST:**
1. **Add to run log** — Create or append to `runs/run-N.md` (use `run-0.md` for corrections during the first run / strategy creation). Format:
   - **DO** or **DO NOT:** [the rule]
   - **Example (wrong):** [what was done incorrectly]
   - **Example (correct):** [what it should be]
2. **Apply the correction** — Refine strategy or re-run with corrections as input.
3. **Proactively confirm** — Say: "I've added this to the run log. Correction: [brief summary]. I've applied it."

**First-run corrections:** Use `runs/run-0.md` to capture corrections during strategy creation and initial tree/model building. Same format. The run log feeds future runs.

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
