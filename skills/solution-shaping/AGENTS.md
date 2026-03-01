# Solution Shaping

Your task is to **shape** source material into an **Interaction Tree** and **State Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them. In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Shaping means we do not go deeper than the story level; details are flushed out later.

Each rule has a DO with example and a DO NOT with example.

## Process Overview

**You MUST follow this process before producing any output.**

1. **Strategy Phase first** — Analyze the source, propose Epic/Story breakdown and slice order, save the strategy. Do not produce an interaction tree until the strategy is approved.
2. **Work in slices** — Produce 4–7 stories per slice. Get user approval before moving to the next slice.
3. **No full output in one go** — Do not produce a complete interaction tree in a single pass. Iterate slice by slice.

### When the user says

When the user says "create the story map," "proceed," "build it," "generate the output," or similar, you **MUST still begin with the Strategy Phase**. Do not skip to producing the full output.

### Before You Produce Output

**STOP.** Before producing any Interaction Tree or State Model, you MUST:

1. [ ] Complete the Strategy Phase (analyze source, propose breakdown, save strategy to `story/<domain>-shaping-strategy.md`)
2. [ ] Get user approval of the strategy
3. [ ] Run Slice 1 only (4–7 stories) and get approval before continuing

---

# Core Definition

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

# Rules

Each rule has a DO with example and a DO NOT with example.

---

## Derive from source

**DO** derive concepts from the interactions you find in the source; focus on *who* exchanges *what* and *what must be true before and after*.
- Example: Source describes "Customer adds to cart" → interaction has Add to Cart; concepts (Shopping Cart, LineItem) derive from what the source describes.

**DO NOT** invent workflows or mechanics not present in the source.
- Example: Source has no "express checkout" — do not add it; source has no "loyalty points" — do not invent it.

---

## Logical/domain level

**DO** keep everything at logical/domain level.
- Example: "Customer adds Book to Shopping Cart"; "Order created (submitted)".

**DO NOT** describe implementation details or include infrastructure or technical failures.
- Example: "REST API returns 200"; "INSERT INTO orders"; "Database timeout"; "Network unreachable".

---

## Speculation and assumptions

**DO** state an assumption when something is unclear.
- Example: "Assumption: Shipping Address is provided before checkout".

**DO NOT** speculate beyond the provided material or invent mechanics when unclear.
- Example: Inventing workflows, concepts, or steps not in the source; making up how something works instead of stating an assumption.

---

## Hierarchy and parent granularity

**DO** keep parent nodes at appropriate granularity for their level.
- Example: Epic "Build a Character" → Response "System creates valid Character for Campaign".

**DO NOT** leak child-level detail into parent nodes.
- Example: Epic lists "Cart line-item quantity = 2" (that belongs on Story).

---

## Sequential order

**DO** order the tree sequentially — required state creators before consumers; follow actual flow, not topic grouping.
- Example: Create Character → Set Scenario → Start Turn → Perform Action (not: Resolve Checks → Run Combat).

**DO NOT** organize by topic when it violates sequence.
- Example: "All checks together" or "Run Combat" before "Create Character" or "Set Scenario".

---

## Concept scoping

**DO** scope concepts to the Epic or Story that owns them — declare at the lowest common ancestor of all interactions that use the concept. Assign to ONE level only. When the child uses only parent concepts, leave State Concepts blank (inheritance assumed).
- Example: Shopping Cart under Shop for Books; Book Catalog under Browse Books; Account at root if used across both. Epic Make Checks has Check, DifficultyClass, Modifier; each story has State Concepts left blank.

**DO NOT** declare concepts at the wrong level or list every concept at the root. Do not repeat parent concepts on children.
- Example: Shopping Cart at root when only Shop for Books uses it. Epic Make Checks had State Concepts: Check, DifficultyClass, Modifier on Story "Make Standard Check" and "Make Opposed Check" — wrong: those concepts were on the Epic, so repeating them on stories violates "assign to ONE level only".

---

## Failure modes

**DO** limit failure modes to a maximum of 3 per interaction; derive from domain rules, state conditions, or authorization.
- Example: "Insufficient balance"; "Account suspended"; "Cart is empty".

**DO NOT** include infrastructure or technical failures.
- Example: "Database timeout"; "Network unreachable"; "Server crash".

---

## Required state

**DO** declare shared required state on the parent only; list only new or unique required state on children; make required state comprehensive — ask "Would this work if [X] didn't exist?". Assign to ONE level only — if unique to a story, keep on story; if on more than one story, promote to parent. When the child uses only parent concepts/state, leave Required State and State Concepts blank (inheritance assumed).
- Example: Parent: "Books exist in catalog"; Child: "Books match search criteria" (specializes). "Can you search if no books exist?" → required. Epic Make Checks has Check, Modifier, DifficultyClass; all children have State Concepts left blank. PowerPointBudget on 3 of 4 stories → promote to Sub-epic; remove from the 3.

**DO NOT** duplicate shared state on children or omit required preconditions. Do not repeat parent concepts on children. Do not put concepts on individual stories when they apply to multiple — that causes you to omit them on some.
- Example: Child repeats "Books exist" when parent already has it. Epic Make Checks had State Concepts on each story; Story "Make Secret Check" had State Concepts left blank but the model omitted that Check, Modifier, DifficultyClass all apply — wrong: putting concepts on individual stories caused them to be forgotten on Secret Check.

---

## Resulting state

**DO** apply the same inheritance rules to Resulting State as Required State — shared on parent, child-specific on child. At Epic/Sub-epic level, express as a single, high-level outcome; use outcome language only (what is true afterward).
- Example: Parent: "Cart populated"; Child: "Shopping Cart: empty → has-items". Epic: "Character is built and valid within campaign PL and PP limits"; "validation result recorded".

**DO NOT** duplicate resulting state across levels or use action language in Resulting State. Do not use intermediate steps, granular outcomes, or behavior/action language in Epic/Sub-epic Resulting State.
- Example: "System validates" or "System records" (use outcome: "validation result recorded"). Epic-level wrong: "Character has PP budget allocated"; "Character is fully built; Character has all traits; Character validated against PL".

---

## Structured concepts — include in every slice run

**DO** complete the full workflow for each slice: (1) interactions, then (2) derive concepts from interactions, (3) model concepts in OOAD style (State Model), (4) add inline Concepts blocks under Epics with compact definitions (properties, operations). When editing interactions, also update or add concepts as needed.
- Example: After revising an interaction that touches Check and CheckResult, add or update those concepts in the State Model and add a Concepts block under the Epic with Check, CheckResult, DifficultyClass, Modifier and their key properties/operations.

**DO NOT** edit only the Interaction Tree and skip the State Model or inline Concepts. Do not assume concepts are "done" — interaction changes often imply concept changes.
- Example (wrong): Revising an interaction but not updating the related concept or adding a Concepts block. Right: Update both interaction and concepts; add inline Concepts under the Epic.

---

## Story granularity

**DO** break down by distinct requirements areas, distinct concept structure, or workflow steps; sufficient stories to capture rule detail.
- Example: One story per "View Product" or "Make Payment" when each has distinct logic; break by "Drive Bike" vs "Drive Car" when concept structure differs.

**DO NOT** collapse large rule sections into one story.
- Example: One story for "all effects" or "all attacks" when hundreds of pages warrant many stories.

---

## Supporting actor and Response

**DO** treat Supporting as the system (or subsystem) that responds — use Actor → System exchange; keep Epic-level (and Sub-epic) Response coarse-grained — what is true after the actor initiates at that level.
- Example: "System saves campaign PL"; "System persists budget"; Epic "Build a Character" → "System creates valid Character for Campaign".

**DO NOT** frame Supporting as a human or use human-to-human exchange; do not use story-level or sub-epic-level detail in Epic-level or Sub-epic Response.
- Example: "GM sets and communicates"; "Player tells GM"; Epic "Build a Character" → "System applies cost formula; deducts PP; validates traits" (that belongs in stories).

---

# Required Output Structure

**Workflow:** Start with interactions. Derive concepts from the interactions. Model the concepts in OOAD style (State Model). Add inline Concepts blocks under Epics with compact definitions (properties, operations). Complete this full workflow for each slice.

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

# Shaping Process

The shaping process follows this flow. **Use this checklist** — do not skip steps.

## Process Checklist

- [ ] **Strategy Phase complete** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `story/<domain>-shaping-strategy.md`
- [ ] **Strategy approved by user** — Do not produce an interaction tree until then
- [ ] **Slice 1 produced** — 4–7 stories for the first slice
- [ ] **Slice 1 approved** — User reviews; corrections → add DO/DO NOT to strategy; re-run until approved
- [ ] **Next slice** — Proceed to next slice; repeat until all slices done
- [ ] **Post-shaping review** — Review all corrections; determine what needs to change in rules/instructions

## Flow

1. **Strategy** — Come up with a strategy (Epic/Story breakdown, slice order, assumptions).
2. **Validate strategy up front** — Review and refine the strategy until it looks reasonable. Do not produce an interaction tree until the strategy is approved.
3. **Run first slice** — Produce the first slice of stories (e.g. 4–7 stories). User reviews and corrects.
4. **Corrections feed back into strategy** — When mistakes are found, add **DO** / **DO NOT** rules to the strategy document. Re-run the slice until approved.
5. **Next slice** — Once the slice is approved, proceed to the next slice. Repeat steps 3–4 for each slice.
6. **Slice ordering** — At any point, you may change the ordering of slices and adjust the strategy accordingly.
7. **Post-shaping review** — Once all slices are done, have the AI review all corrections and determine what needs to change in the rules and/or instructions.

When analyzing **existing content**, review and follow the strategy.

## Strategy Criteria

### 1 - Shaping Granularity

**Stories** represent the "stopping point". Each story represents something tangible that a user can recognize while fine-grained enough to implement / deliver as independent work.

**Analyze the source** to determine where complexity lives:
- **Business rules** — Distinct rules or conditions that change behavior warrant separate stories when the interaction differs.
- **System interactions** — Different systems or integration points warrant separate stories when the exchange pattern differs.
- **Workflows** — Different sequences or paths warrant separate stories when steps, actors, or outcomes differ.
- **Structure** — Different concept shapes or taxonomies warrant separate stories when the concept structure changes the interaction.
- **State** — Different state transitions or preconditions warrant separate stories when the required or resulting state differs materially.

State your reasoning so the user can adjust.

### 2 - Shaping Depth

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

## Strategy Phase

1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed Epic/Story breakdown, assumptions, break down strategy, **proposed traversal order (slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `story/<domain>-shaping-strategy.md`.

## Running Slices

1. **Run the first slice** — Produce 4–7 stories for Slice 1. User reviews and corrects.
2. **Corrections → strategy** — When a mistake is found, add a **DO** or **DO NOT** to the strategy document. Re-run the slice until the user approves.
3. **Next slice** — Proceed to the next slice. Repeat for each slice.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

## Post-Shaping Review

Once all slices are done, have the AI review all corrections in the strategy and determine what needs to change in the rules and/or instructions. Promote those that apply across domains.

---
