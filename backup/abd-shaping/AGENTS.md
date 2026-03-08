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

---

# Process Overview

<!-- section: shaping.process.intro -->
Your task is to **shape** source material into an **Interaction Tree** and **State Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them. In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Shaping means we do not go deeper than the story level; details are flushed out later.

Each rule has a DO with example and a DO NOT with example.

**You MUST follow this process before producing any output.**

1. **Strategy Phase first** — Analyze the source, propose Epic/Story breakdown and slice order, save the strategy. Do not produce an interaction tree until the strategy is approved.
2. **Work in slices** — Produce 4–7 stories per slice. Get user approval before moving to the next slice.
3. **No full output in one go** — Do not produce a complete interaction tree in a single pass. Iterate slice by slice.

### When the user says

When the user says "create the story map," "proceed," "build it," "generate the output," or similar, you **MUST still begin with the Strategy Phase**. Do not skip to producing the full output.

### Output Paths (default)

- **Strategy:** `<skill-space>/shaping/strategy.md`
- **Output:** `<skill-space>/shaping/slice-N/` (per slice)

These paths can be configured under the skill-space config (`ace-config.json` or equivalent) so the user can choose where files go and what they are named.

### Before You Produce Output

**STOP.** Before producing any Interaction Tree or State Model, you MUST:

1. [ ] Complete the Strategy Phase (analyze source, propose breakdown, save strategy to `<skill-space>/shaping/strategy.md`)
2. [ ] Get user approval of the strategy
3. [ ] Run Slice 1 only (4–7 stories) and get approval before continuing

## Process Checklist

- [ ] **Strategy Phase complete** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `<skill-space>/shaping/strategy.md`
- [ ] **Strategy approved by user** — Do not produce an interaction tree until then
- [ ] **Slice 1 produced** — 4–7 stories for the first slice
- [ ] **Slice 1 approved** — User reviews; corrections → add DO/DO NOT to strategy (with wrong/correct examples); re-run until approved
- [ ] **Next slice** — Proceed to next slice; repeat until all slices done
- [ ] **Post-shaping review** — Review all corrections; determine what needs to change in rules/instructions

<!-- section: shaping.process.post_shaping.review -->
## Post-Shaping Review

Once all slices are done, have the AI review all corrections in the strategy and determine what needs to change in the rules and/or instructions. Promote those that apply across domains.

---

# Strategy Phase

<!-- section: shaping.strategy.phase -->
1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed Epic/Story breakdown, assumptions, break down strategy, **proposed traversal order (slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `<skill-space>/shaping/strategy.md`.

<!-- section: shaping.strategy.criteria -->
## Strategy Criteria

### 1 - Splitting Criteria

**Stories** represent the "stopping point". Each story represents something tangible that a user can recognize while fine-grained enough to implement / deliver as independent work.

**Determine splitting criteria** — How do we split epics into sub-epics, and sub-epics into stories? Analyze the source to identify criteria that drive the split. Examples of ways to figure out splitting criteria:
- **Business rules** — Distinct rules or conditions that change behavior warrant separate stories when the interaction differs.
- **System interactions** — Different systems or integration points warrant separate stories when the exchange pattern differs.
- **Workflows** — Different sequences or paths warrant separate stories when steps, actors, or outcomes differ.
- **Structure** — Different concept shapes or taxonomies warrant separate stories when the concept structure changes the interaction.
- **State** — Different state transitions or preconditions warrant separate stories when the required or resulting state differs materially.

State your splitting criteria and reasoning so the user can adjust.

### 2 - Depth

When shaping, choose the **depth** of what you produce:
- **Interactions only** — Capture only the interactions themselves, without actors.
- **Interactions + actors** — Interactions with initiating and supporting actors, but nothing more.
- **State concepts without state changes** — Identify and model State Concepts but not Required State and Resulting State for each interaction.
- **Failure modes and responses** — Include or omit Failure Modes and Response behavior.
- **Deeper in some places** — Go deeper in selected areas (steps, examples, acceptance criteria).

Decide and document in the strategy what is in scope.

### 3 - Traversal Order (Slices)

The order in which you work through stories is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

**Ideas for prioritizing slices:**
- Architectural slice — Stories that establish the architecture
- Domain slice — Stories aligned by common business logic
- Integration slice — Stories across integration points
- Workflow slice — End-to-end workflow for a particular use case
- Value slice — Stories that provide the most value if done first
- Risk slice — Stories that de-risk some aspect of the solution

Favour slicing vertically, often by a common theme or category of complexity. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

<!-- section: shaping.strategy.slices.running -->
## Running Slices

1. **Run the first slice** — Produce 4–7 stories for Slice 1. User reviews and corrects.
2. **Corrections → strategy** — When a mistake is found, add a **DO** or **DO NOT** to the strategy document. Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the slice until the user approves
3. **Next slice** — Proceed to the next slice. Repeat for each slice.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

<!-- section: shaping.strategy.corrections -->
## Corrections Format

When adding corrections to the strategy document, each **DO** or **DO NOT** must include:
- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the slice until the user approves.

When analyzing **existing content**, review and follow the strategy.

### Object Model Correction

**DO** — Inject the Engine (or context provider) into components that need it. Use properties over getters. Encapsulate over passing parameters — components pull context from injected dependencies instead of receiving it as method arguments.

- **Example (wrong):** `AbdSkill.get_instructions_for(operation, context)` — context passed as parameter.
- **Example (correct):** AbdSkill has `Engine engine` (injected); `instructions` property; assembles using `engine.workspace`, `engine.strategy_path` when needed.

---

# Required Output Structure

**Output path (default):** `<skill-space>/shaping/` — write the Interaction Tree and State Model in `shaping/slice-N/` per slice. Configurable via skill-space config.

**Workflow:** Start with interactions. Derive concepts from the interactions. Model the concepts in OOAD style (State Model). Add inline Concepts blocks under Epics with compact definitions (properties, operations). Complete this full workflow for each slice.

<!-- section: shaping.output.interaction_tree -->
## A) Interaction Tree

A hierarchical structure of meaningful exchanges between actors. All levels use the same interaction format — they differ only in granularity.

**Hierarchy:**
```
Epic (coarse interaction)
  └─ Epic (finer-grained)
       └─ Story (fine interaction)
            └─ Scenario (optional grouping of steps)
                 └─ Step (atomic interaction to be done at a later state)
```

**Node names:** Use bold for Epic and Story node names (e.g. `- Epic: **Create Ace-Skill**`, `- Story: **Create scaffolding via script**`).

**Interaction format (used at every level):**

| Field | Description |
|-------|-------------|
| Actor | Initiating actor |
| Supporting | Responding actor(s) |
| Required State | Preconditions (inherit from parent; add only new/specialized) |
| State Concepts | Domain concepts involved |
| Initiation | What the initiating actor does (verb-noun) |
| Response | What the supporting actor does (behavior only) |
| Resulting State | Outcome only; use commas for multiple changes |
| Failure Modes | Max 3, rule/state based only |

**Granularity:** Each story must represent something tangible, valuable, and fine-grained enough to implement. Do not collapse large requirements / business rules / complexity into a single story.

<!-- section: shaping.output.state_model -->
## B) State Model

Identify the domain state concepts referenced in the Interaction Tree. Model each concept in OOAD style:

```
Concept : <Base Concept if any>
- <stateful concept returned> property
      <collaborating concepts if any>
- <stateful concept returned> operation(<param>, <param>, ...)
     <collaborating concepts if any>
```

**Format:**
- **Concept** — name; optionally `: BaseConcept` if it extends another
- **Properties** — `<concept type> property` with optional collaborating concepts below
- **Operations** — `<concept type> operation(<params>)` with optional collaborating concepts below
- **Collaborating concepts** — other concepts this property/operation works with or depends on
- **Invariants** — when an invariant applies to a single property or operation, state it under that property or operation

**Scoping:** Declare each concept at the Epic (or Story) that is the root of the smallest subtree where it is used. Concepts used across multiple Epics belong at their common ancestor.

---

# Validation Pass

<!-- section: shaping.validation.checklist -->
## Validation Checklist

After generating interactions and concepts, verify:

**Interactions**
- [ ] Each interaction has Actor, Supporting, Initiation, Response, Required State, State Concepts, Resulting State
- [ ] Response = behavior only (no state language); Resulting State = outcome only (no action language); no overlap between them
- [ ] Each interaction touches at least one state concept
- [ ] Hierarchy respected: Epic → Epic → Story → Scenario → Step
- [ ] **Sequential order:** Required state creators appear before consumers; tree follows actual flow of the system

**Required State**
- [ ] Shared required state on parent only; children list only new or specialized state
- [ ] Required state comprehensive — data exists, state has right value, relationships in place, dependent concepts populated
- [ ] No child-level detail leaked into parent nodes

**Resulting State**
- [ ] Same inheritance rules as Required State; common state on parent, child-specific detail on child

**Failure Modes**
- [ ] Max 3 per interaction
- [ ] From domain rules, state conditions, or authorization only (no infrastructure or technical failures)

**Concepts**
- [ ] Each concept scoped to Epic/Story that owns it (lowest common ancestor of all interactions that use it)
- [ ] Invariants under specific property/operation when they apply to that property/operation only

**Content**
- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level
- [ ] Assumptions stated when unclear (no invented mechanics)
- [ ] **Granularity:** Sufficient stories to capture rule detail; no collapsing of large sections into single stories

---

# Script Invocation

AI guidance for calling ace-shaping scripts.

## get_instructions.py

Gets the assembled prompt for an operation from the Engine. **Call this before producing any shaping output.**

**When to call:** When the user requests:
- `generate_slice` — "do slice 1", "generate the first slice", "proceed with slice 1", etc.
- `create_strategy` — "create the strategy", "analyze and propose breakdown", etc.
- `improve_strategy` — "improve the strategy based on feedback", etc.

**Usage:**
```bash
cd .agents/skills/ace-shaping
python scripts/get_instructions.py generate_slice
```

**Output:** The assembled prompt (sections + strategy doc + context). **Inject this output into your response and follow it.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths.

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage:**
```bash
cd .agents/skills/ace-shaping
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core, process, strategy, output, validation.

---
