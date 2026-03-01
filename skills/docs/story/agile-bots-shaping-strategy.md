# Strategy: Agile Context Engine Interactions and State Analysis

**Source:** `agile_bots` — bots/, src/, docs/story/story-graph.json, test/, docs/agile-bots-vs-skills-sh-analysis.md  
**Methodology:** solution-shaping skill (`skills/solution-shaping/AGENTS.md`)  
**Output:** `skills/docs/agile-context-engine-story-map.md` (Interaction Tree + State Model)  
**Domain:** Agile Context Engine — workflow orchestration for AI agents and developers

---

## 1. Source Complexity Analysis

### Where Complexity Lives

| Area | Source | Complexity | Reasoning |
|------|--------|------------|-----------|
| **Instruction assembly** | src/instructions/, bots/.../base_actions/, guardrails | **HIGH** | Multi-level hierarchy: base action + behavior + guardrails + context + scope. Different injection paths per action type. |
| **Scope filtering** | src/scope/, json_scope.py | **MEDIUM** | Story/increment/file filtering; graphLinks enrichment; StoryGraphFilter vs FileFilter. |
| **Guardrails flow** | guardrails/required_context/, guardrails/strategy/, clarification.json, strategy.json | **MEDIUM** | Key questions, evidence, decision criteria, assumptions; save/merge; panel vs CLI. |
| **Diagram sync** | synchronizers/, DrawIO, LayoutData, UpdateReport | **HIGH** | Render story graph → DrawIO; extract DrawIO → story graph; update report; layout persistence. |
| **Bot initialization** | bot_config.json, behavior discovery, action workflow | **LOW-MEDIUM** | Load config, enumerate behaviors, set current behavior/action. |
| **Rules and validation** | rules/*.json, RuleLoader, scanners | **MEDIUM** | Behavior rules; validation context; scanners (optional). |

### Actor Model

- **Actor (Initiating):** Developer — uses CLI or Panel to invoke bot, navigate, get instructions, save guardrails, submit to AI.
- **Supporting:** Bot System — loads config, assembles instructions, persists scope/guardrails, renders/syncs diagrams.
- **Optional:** AI Agent — invokes via MCP tools; same instruction flow, different initiation path.

---

## 2. Behavior Distinction Analysis (Structure Question)

**We must get specific about what we're doing in each behavior** — not assume they're the same because the coding pattern is similar. The question: Is this one thing or separate? That's a structure decision we need to make from the analysis.

### What each behavior does (from source)

| Behavior | Inputs | Outputs | Build does | Validate does |
|----------|--------|---------|------------|---------------|
| **Shape** | User context, vision, requirements | story-graph.json (epics, sub-epics, stories), story-map.md, DrawIO outline | Create epic/sub-epic/story hierarchy | Validate story structure rules |
| **Prioritization** | Story map from shape | Story map with delivery increments | Organize stories into sequenced increments | Validate increment structure |
| **Exploration** | Elaborated stories | Stories with acceptance criteria and scenarios | Document AC and scenarios in story graph | Validate AC/scenario structure |
| **Scenarios** | Stories with AC | Stories with BDD scenarios | Add scenario steps | Validate scenario structure |
| **Tests** | Story specs | Test files | Generate test cases | Validate test coverage |
| **Code** | Story specs, test files | Source code files | Generate production implementation | Validate code quality, domain language |

### Structure question

- **Same pattern, different content?** — All use clarify → strategy → build → validate → render. Same instruction-assembly machinery. Different artifacts.
- **Or structurally distinct?** — Different required state (shape needs nothing; prioritization needs shaped story map; exploration needs elaborated stories; code needs tests). Different resulting state. Different domain concepts (StoryGraph vs Increment vs AcceptanceCriteria vs TestFile vs SourceCode).

**We need to model the distinct interactions** — what exactly happens when Developer invokes shape.clarify vs shape.build vs code.build? What concepts are involved? What state changes? Only then can we decide:
- One epic "Perform Action" with behavior-specific sub-epics (Shape Story Map, Prioritize Delivery, Explore Requirements, Generate Code)?
- Or separate epics per behavior?
- Or something else?

**DO NOT** prematurely collapse behaviors. **DO** analyze each to understand distinct artifacts, required state, resulting state, and concepts. The structure (epic vs sub-epic vs story) follows from that analysis.

---

## 3. Target Solution Direction (Replace Clarify/Strategy; New Data Model)

**Context:** Clarify and strategy in agile_context_engine are largely ineffective — more pain than value. The current scale (this process we're running right now) will be applied to the new solution. We are designing the replacement, not just documenting the existing system.

### Process Replacement

**The strategy → slices → refine-as-we-go process replaces the fixed clarification/strategy approach.** The workflow we're using now (strategy doc, validate, run slice, corrections → strategy, next slice) is the model for how shaping should work — not embedded clarify/strategy steps in every behavior.

**Clarification:** If used at all, it should be a **specific context-gathering skill** in front of the whole process as its own scale — not embedded into all other scales/behaviors.

### Behaviors — Do Not Assume

**We need to figure out the exact behaviors** — do not assume we're using the same ones (shape, code, exploration, etc.) in the new solution. This is part of the analysis and will need AI help. Questions to explore:

### One Skill with Levels vs Multiple Skills?

**Option A — Multiple skills, each with a stopping level:**
- **"Shaping"** — Care about actors, interactions, base data. Stop at story level.
- **"Specifications"** — Stop at steps, add examples to the data, do walkthroughs (CRC model).

**Option B — One skill with level + data:**
- One skill, e.g. **"Interactions and Structure"** — specify the level and add the data. Same machinery, different depth.

**We need to analyze which approach fits.** This is an open question for the story mapping slice.

### Data Model Additions (Target)

The data model is like we have now, with these additions:

| Addition | Description |
|----------|-------------|
| **Steps** | New interaction level in the hierarchy **below stories** |
| **Examples** | Attached to domain model directly AND to interactions where state gets connected |
| **Step → state** | Each step gives a specific example of how the state actually changed |
| **Required state examples** | Required state has examples |
| **Resulting state examples** | Resulting state has examples |
| **Spec by example** | Specification by example without clutter — attached directly to the model |

**Higher-level epics** (at any level in the hierarchy) have **impacts**:
- **Qualitative** — change in user behavior
- **Quantitative** — economic benefit

**Constraints** — applied at any level of the hierarchy. Examples:
- Must run in X time (milliseconds, seconds)
- Must support N (non-functional reqs)
- Must be implemented using architecture pattern X

**Architecture pattern** — looks like an interaction with structure and interactions, but describes how a technology works (e.g. React Native, MERN stack, caching strategy).

### Implementation in Story Mapping Slice

**We need to figure out how to implement these** (steps, examples, impacts, constraints, architecture patterns) as part of our story mapping slice. This is design work to be done during the analysis — not assumed from the current agile_context_engine structure.

---

## 4. Granularity Rules

**Stories must be distinguished by:**
- Different actors or initiation paths (Developer vs AI Agent)
- Different required state (e.g., scope set vs not set; guardrails defined vs not; story graph exists vs not)
- Different state transitions (instructions retrieved vs guardrails saved vs story graph updated vs diagram rendered)
- Different failure modes (missing config vs empty scope vs malformed diagram)
- **Different behaviors when artifacts/concepts/state differ** — shape.build vs code.build touch different concepts

**DO NOT create separate stories for:**
- Implementation details (JSON vs Markdown, CLI vs Panel) — keep at logical level

**DO create separate stories for:**
- Initialize vs Perform Action vs Set Scope vs Work With Story Map — distinct workflows
- Clarify (save answers) vs Strategy (save decisions) — different persisted state
- Render diagram vs Sync diagram to story graph — different outcomes and concepts
- Submit instructions to AI — distinct initiation and outcome
- **Behavior-specific interactions when the domain differs** — e.g., shape.build (creates epic/sub-epic/story) vs code.build (creates source files) — different concepts, different resulting state

---

## 5. Proposed Epic Structure (Sequential Order)

**We do not define architecture upfront** — one skill vs many skills, what's common vs not common, will emerge from the work. We run on shaping explicitly and move farther as we need to. Slice 1 is about shaping and figuring out what belongs here.

**Shaping-focused structure (as far as we go for now):**
```
Initialize Agile Context Engine
Gather Context
Use Shape Skill
     Create Shaping Strategy
     Generate Shaping Slices
     Improve Shaping Skill
....
```

We do not try to figure out the rest (Specify, Test, Code, common vs skill-specific) up front. That comes from Slice 2+ when we decide one-skill-vs-many and slice-as-run semantics.

---

## 6. Proposed Traversal Order (Slices)

**Principle: Dogfood. Build the thing that lets us do the next thing.** Slices are ordered by **de-risking technology** and **getting something working as a native skill** — not by agile_context_engine epic structure. Each slice: define it, then build it.

| Slice | Theme | Define | Build | Rationale |
|-------|-------|--------|-------|-----------|
| **1** | Shaping skill + Python/JSON hybrid | Current shaping skill content; JSON config schema; integration with existing rule set (.cursor/rules, AGENTS.md) | Get shaping skill working with Python/JSON hybrid; add **architecture-pattern constraints** (e.g., must use X, must run in Y time) | **De-risk foundation.** Prove the skill runs with our rules and config. Add constraints from architecture-pattern perspective. |
| **2** | One skill vs many skills | One skill with lots of parameters vs many skills with specific instructions; **steps, examples, linking to tests and code**; slice-as-run semantics | Design decision + schema for steps/examples/links | **Structure decision.** Critical for moving past shaping. Steps, examples, test/code links live here. **Open question:** Is a slice a specific run (shape in before slice done) or do we take a slice to full extent in multiple runs? |
| **3** | Implement slices 1+2 | — | Implement the previous two slices end-to-end | **Build it.** We have enough to implement. |
| **4** | Instruction injection | Proactive, real-time instruction injection; scale-question work; skills default vs custom | Explore and prototype; decide if skills default is good enough (hypothesis: no) | **De-risk instruction flow.** How do we inject instructions more proactively in real time? Do we need scale-question work? |
| **5** | CLI | CLI contract for everything built so far | Introduce CLI; get it working (new steps on existing stories or new stories) | **Interface.** Wrap what we've built in a CLI. |
| **6** | Hierarchy scoping | Scope filtering at epic/sub-epic/story level (renamed from "story scoping") | Set scope; filter by hierarchy | **Filtering.** Scope by hierarchy. |
| **7** | Panel | Panel ↔ skill contract; **architecture constraint: visualize through panel** | Get it back into the panel; works with existing agile_context_engine code | **Integration.** Add constraint: must visualize through panel. |
| **8** | Impacts + other constraints | Qualitative/quantitative impacts on epics; non-functional constraints | Add impacts, other constraints to data model | **Enrichment.** Impacts on epics; other constraints. |

**Order:** Define → Build. Slice 1 gets the skill working with our hybrid. Slice 2 decides structure (one vs many, slice semantics). Slice 3 implements. Slice 4 explores instruction injection. Slices 5–8 add CLI, hierarchy scoping, panel, impacts.

---

### Feedback on Slice Design

| Point | Feedback |
|-------|----------|
| **Slice 1 + architecture constraints** | Good. Adding architecture-pattern constraints early de-risks the "how we build" question. |
| **Slice 2: one vs many + slice-as-run** | The slice-as-run question is structural: if a slice = one run, we get shape in before the slice is "done"; if a slice = full extent, we do multiple runs per slice. Recommend making this an explicit design decision with stories. |
| **Slice 3: implement 1+2** | Clear. Slices 1 and 2 are definition; slice 3 is implementation. |
| **Slice 4: instruction injection** | Worth exploring. If skills default is insufficient, we need to know early. Scale-question work may be the right lever. |
| **Slice 5: CLI** | Fits. CLI wraps what exists; likely new steps on existing stories. |
| **Slice 6: hierarchy scoping** | "Hierarchy scoping" is clearer than "story scoping" — scope can apply at epic, sub-epic, or story level. |
| **Slice 7: panel + constraint** | Adding "must visualize through panel" as an architecture constraint is good — it forces the design to support panel from the start. |
| **Slice 8: impacts** | Impacts and other constraints can come after we have the core flow working. |

---

## 7. Assumptions

- **Scope:** We are shaping the *usage* of the Agile Context Engine system AND designing the **target solution** that replaces it — new data model (steps, examples, impacts, constraints), new process (strategy→slices replaces clarify/strategy), behaviors TBD.
- **Clarify/Strategy:** Being replaced by the strategy→slices→refine process. If context-gathering exists, it is a separate skill in front — not embedded in every behavior.
- **MCP:** AI Agent invocation via MCP tools uses the same instruction flow; initiation differs. We may add a story for "AI Agent invokes bot via MCP" in a later slice if needed.
- **Panel vs CLI:** Treated as same logical interaction (Developer initiates; Bot System responds). No separate stories for UI modality.
- **Existing output:** `agile-context-engine-story-map.md` exists from a previous (non-strategy) run. Slice 1 will get the shaping skill working with Python/JSON hybrid and add architecture-pattern constraints.

---

## 8. Shaping Depth

- **Interactions + actors** — Full format: Actor, Supporting, Required State, State Concepts, Initiation, Response, Resulting State, Failure Modes
- **Inline Concepts** — Add compact Concepts blocks under Epics with properties/operations
- **Failure Modes** — Include; max 3 per interaction; domain/state only

### State Model — Invariants

**DO** state invariants under the property or operation they constrain. Use format: `invariant: <constraint>` directly under that property or operation, as in the skill examples (core-definitions.md, output-structure.md).

**DO NOT** put invariants at the bottom of the concept unless they span multiple properties or the whole concept.

### Context and Concepts — Derive from Skill Process, Not Current Application

**DO** derive State Concepts and context structure from how the skill/process works (strategy phase → source analysis → slice runs → corrections). Ask: What does the shaping process need? What structure supports that?

**DO NOT** mimic agile_bots (or current application) data structures (story-graph.json, clarification.json, workspace test/src/context) unless they align with the skill's process. We are designing the replacement.

### Shaping Mode — Do Not Create; Add to Knowledge

When the user says we need something (e.g. a feature, component, file, artifact) but we are in shaping mode:

**DO NOT** create it — do not implement, scaffold, or code it.

**DO** add it to the knowledge we're creating — capture it in the strategy, story map, state model, or slice as something to be built or defined later.

Shaping mode is about defining and modeling what we need, not building it yet.

---

Please review this strategy. Once approved, I will produce **Slice 1** (4–7 stories: Shaping skill + Python/JSON hybrid — get the skill working with our rules and config; add architecture-pattern constraints).
