# ABD Instruction Injection — Analysis and Object Model

**Purpose:** Map agile_bots behavior/action/instructions to ABD; define AbdSkill operations; specify what to inject and when.

---

## 1. Agile Bots Model (Reference)

| Concept | agile_bots | ABD equivalent |
|---------|------------|----------------|
| **Behavior** | shape, code, tests, etc. | Skill (abd-story-synthesizer) |
| **Action** | clarify, strategy, build, validate, render | Operation (create_strategy, generate_slice, improve_strategy, improve_skill) |
| **Instructions** | Assembled per action; injected on submit | Assembled per operation; injected when AI runs that operation |

**agile_bots instruction assembly:**
- Base instructions (from action_config)
- Guardrails (key questions, evidence, decision criteria)
- Clarification data (saved answers)
- Strategy data (saved decisions)
- Scope (story graph when applicable)
- Context paths

**Key insight:** Instructions are assembled and **injected** into the AI prompt. The AI doesn't "go read" the rules — they're given.

---

## 2. Use Shape Skill → Operations

**Use Shape Skill** has stories that map to **operations** (actions):

| Story | Operation | What it does |
|-------|-----------|--------------|
| Create Strategy | `create_strategy` | Analyze source; propose epic breakdown, slice order, assumptions; save strategy doc |
| Generate Slices | `generate_slice` | Load strategy; produce 4–7 stories; output Interaction Tree + State Model |
| Improve Skill (during slices) | `improve_strategy` | Add DO/DO NOT and or examples to existing DO/DO NOT into strategy doc; re-run slice until approved |
| Improve Skill (post-synthesis) | `improve_skill` | Take accumulated corrections from strategy doc; update base skill (content, rules) so the skill itself improves |

**Improve strategy** = corrections go into the strategy document. **Improve skill** = strategy doc improvements are applied to the skill's content and rules.

**Behavior = skill (abd-story-synthesizer).** Actions = these operations.

---

## 3. Content Decomposition (Markdown → Injectable Sections)

**Alignment convention:** Section IDs mirror file structure. `story_synthesizer.X.Y` → content lives in a file whose name matches X (e.g. `strategy.md` for `story_synthesizer.strategy.*`). Dot notation = hierarchy within that file.

**Two approaches:** The choice is whether files are organized by **domain** (what the content is about) or by **source file** (where the content lives). Section IDs and the range of referenced files follow from that choice.

| Approach | Primary driver | Files reflect | Section ID pattern | Why it matters |
|----------|----------------|---------------|--------------------|----------------|
| **Domain-led** | Organize by domain concept (strategy, process, output, validation, core) | One file per domain: `strategy.md`, `process.md`, `output/*.md`, validation, `core.md` | `story_synthesizer.{domain}.{topic}` — e.g. `story_synthesizer.strategy.iterative`, `story_synthesizer.process.intro` | Domain coherence: everything about strategy in one place; easier to assemble per operation; consistent meaning. |
| **File-led** | Organize by existing source file | Keep current file layout; section IDs mirror file paths | `story_synthesizer.{filename}.{section}` — e.g. `story_synthesizer.intro.process`, `story_synthesizer.process.strategy_iterative` | Minimal file churn: second level = source file; works when files already exist and you don't want to reorganize. |

**Recommended: Domain-led.** Group by domain so `story_synthesizer.strategy.*` → `strategy.md`, `story_synthesizer.process.*` → `process.md`, etc. Easier to pull out later; consistent meaning.

**Proposed file structure (domain-led):**

| File | Section IDs | Content |
|------|-------------|---------|
| **process.md** | `story_synthesizer.process.intro`, `story_synthesizer.process.post_synthesis.review` | Process overview; post-synthesis review (promote corrections to skill) |
| **strategy.md** | `story_synthesizer.strategy.iterative`, `story_synthesizer.strategy.criteria`, `story_synthesizer.strategy.slices.running`, `story_synthesizer.strategy.corrections` | Iterative Strategy, criteria, running slices, DO/DO NOT corrections |
| **output/*.md** | `story_synthesizer.output.story_map`, `story_synthesizer.output.state_model` | Interaction Tree and State Model format |
| **validation** | `story_synthesizer.validation.checklist`, `story_synthesizer.validation.rules` | Validation checklist; DO/DON'T rules (from rules/) |
| **core.md** | `story_synthesizer.core.interaction`, `story_synthesizer.core.state_concept` | Interaction and State Concept definitions |
| **rules/** (markdown + JSON) | `story_synthesizer.validation.rules` | DO/DON'T rules, scanner configs; merged into RuleSet; sibling to checklist under validation |

**Decomposition for injection:**

| Section ID | Source | Content |
|------------|--------|---------|
| `story_synthesizer.process.intro` | process.md | Process overview, when-user-says, before-you-produce |
| `story_synthesizer.process.post_synthesis.review` | process.md | Post-Synthesis Review: review corrections; determine changes to rules/instructions; promote cross-domain rules |
| `story_synthesizer.strategy.iterative` | strategy.md | Iterative Strategy (create, update, refine; runs through every run) |
| `story_synthesizer.strategy.criteria` | strategy.md | Splitting criteria, depth, traversal order |
| `story_synthesizer.strategy.slices.running` | strategy.md | Run slice, corrections, next slice |
| `story_synthesizer.strategy.corrections` | strategy.md | Corrections → DO/DO NOT with examples |
| `story_synthesizer.output.story_map` | output/*.md | Interaction format, hierarchy |
| `story_synthesizer.output.state_model` | output/*.md | State Model format |
| `story_synthesizer.validation.checklist` | validation | Full validation checklist |
| `story_synthesizer.validation.rules` | rules/ (markdown + JSON) | DO/DON'T rules, scanner configs; loaded via RuleSet; sibling to checklist under validation |
| `story_synthesizer.core.interaction` | core.md | Interaction definition |
| `story_synthesizer.core.state_concept` | core.md | State Concept definition |

---

## 4. What to Inject and When

| Operation | Inject | Rationale |
|-----------|--------|-----------|
| **create_strategy** | `story_synthesizer.process.intro`, `story_synthesizer.strategy.iterative`, `story_synthesizer.strategy.criteria`, `story_synthesizer.core.interaction`, `story_synthesizer.core.state_concept` | AI needs process overview, iterative strategy, splitting/depth/traversal criteria, and domain language. Creates strategy + tree + state model as you go. |
| **generate_slice** | `story_synthesizer.process.intro`, `story_synthesizer.strategy.slices.running`, `story_synthesizer.strategy.corrections`, `story_synthesizer.output.story_map`, `story_synthesizer.output.state_model`, `story_synthesizer.validation.checklist`, `story_synthesizer.validation.rules`, `story_synthesizer.core.interaction`, `story_synthesizer.core.state_concept`, **strategy doc** (from path) | AI produces output; needs output format, validation checklist + rules, and the approved strategy. **Corrections top of mind** — when user feedback implies reusable rule, AI adds DO/DO NOT during slice flow; no separate improve_strategy call. |
| **improve_strategy** | `story_synthesizer.strategy.corrections`, `story_synthesizer.validation.checklist` (correction format only) | AI adds DO/DO NOT to strategy doc; needs correction format and example requirements. |
| **improve_skill** | `story_synthesizer.process.post_synthesis.review`, `story_synthesizer.strategy.corrections`, **strategy doc** (from path) | AI reviews strategy corrections; needs correction format and the strategy doc with accumulated DO/DO NOT; determines what to change in skill content/rules; promotes rules that apply across domains. |

**Validation approach:** No separate validate operation. `generate_slice` injects both `story_synthesizer.validation.checklist` and `story_synthesizer.validation.rules`. Rules = DO/DON'T guidance the AI follows when generating. Checklist = verify output before presenting. Assembled instructions include: *Before presenting any slice output, validate against the checklist and report status (✓ pass or ⚠ needs attention per item) in your response.* The AI's validation report is the user notification — no engine call.

**Scanners:** Programmatic validators (structure, schema, etc.) live in `rules/` as config. Flow: (1) Generate output. (2) Run scanners against the output. (3) Determine false positives. (4) Inject into the next prompt: what the problems were, what the fixes are, and where to look in the report for more detail. The AI addresses real issues in the next iteration. No separate scanner operation — it augments the existing flow when available.

**Context (always available, not "injected" as instructions):**
- Context source paths (from engine)
- Workspace path
- Strategy path (when exists)

---

## 5. AbdSkill Object Model Updates

### Current AbdSkill (content properties only)

```
AbdSkill
- Path path
- RuleSet rule_set
- String core, process, strategy, output, validation
     From core.md, process.md, strategy.md, output/*.md, validation
- AssembledAgent assembled_agent
- AbdSkill build(): AssembledAgent
```

### Proposed AbdSkill (add operations for instruction assembly)

Inject the Engine into AbdSkill so it can refer to context (workspace, strategy path, etc.) without passing parameters. Favor properties over getters; encapsulate over passing parameters.

```
AbdSkill
- Engine engine
     Injected at construction. AbdSkill uses it for context (workspace, strategy_path, etc.).
- Path path
- RuleSet rule_set
- String core, process, strategy, output, validation
- AssembledAgent assembled_agent

- Map<Operation, SectionIds> operation_sections
     operation → section IDs (or file refs) to inject. From skill config. Keys: create_strategy, generate_slice, improve_strategy, improve_skill.

- Instructions instructions
     Property. References operation_sections. When assembled for an operation, grabs context from engine (workspace, strategy_path, slice_index) and returns markdown. No parameters — context comes from engine.

- AbdSkill build(): AssembledAgent
     Assembles content for AGENTS.md (full skill); used for "read the skill" mode
```

### Instructions (property, not factory)

```
Instructions
- Map<Operation, SectionIds> operation_sections
     From AbdSkill.operation_sections — operation → sections to inject
- String display_content(operation)
     Assembles sections for operation; injects context from engine; returns markdown
- String[] sections_included
     Section IDs that were assembled (for debugging)
```

Assembly: Instructions uses engine.workspace, engine.strategy_path, engine.slice_index (when applicable) to build display_content. No context parameter — it pulls from the injected engine.

### Engine role

- **Engine** holds workspace, strategy_path, context paths. Injected into AbdSkill at construction.
- **Caller** asks skill for instructions: `skill.instructions.display_content("create_strategy")` or equivalent. Skill assembles using engine context.
- **When:** Before the AI runs an operation. Caller injects the assembled markdown into the prompt.

---

## 6. Injection Flow (Steps 2–4 Revised)

From Create Strategy steps:

| Step | Current | Revised |
|------|---------|---------|
| 2 | AI → Engine: Requests context from memories | AI → Engine: Requests context source paths **and** instructions for `create_strategy` |
| 3 | Engine → AI: Returns context | Engine → AI: Returns (1) context source paths, (2) assembled instructions (inject) |
| 4 | AI: Reads context; loads skill guidelines | AI: Reads context from paths; **instructions already in prompt** (injected) — no need to "load" guidelines |

**When injection happens:** Before the AI runs the operation. The caller asks the skill for instructions (e.g. `skill.instructions.display_content("create_strategy")`); the skill assembles using engine context and returns markdown. Caller injects into the prompt. The AI receives them — doesn't have to remember to read them.

---

## 7. Summary

| Question | Answer |
|----------|--------|
| **Behavior = ?** | Skill (abd-story-synthesizer) |
| **Actions = ?** | Operations: create_strategy, generate_slice, improve_strategy, improve_skill |
| **What do we inject?** | Sectioned content (`story_synthesizer.*` section IDs) from process, strategy, output, validation, core, and rules — per operation |
| **When?** | When the AI is about to run that operation. Caller requests instructions, injects into prompt. |
| **Object model** | AbdSkill gets Engine injected; has `operation_sections` (map) and `instructions` (property). Instructions assembles from map + engine context. No parameters — encapsulate over passing. |
