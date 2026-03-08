# ABD Instruction Injection — Analysis and Object Model

**Purpose:** Map agile_bots behavior/action/instructions to ABD; define AbdSkill operations; specify what to inject and when.

---

## 1. Agile Bots Model (Reference)

| Concept | agile_bots | ABD equivalent |
|---------|------------|----------------|
| **Behavior** | shape, code, tests, etc. | Skill (abd-shaping) |
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
| Create Shaping Strategy | `create_strategy` | Analyze source; propose epic breakdown, slice order, assumptions; save strategy doc |
| Generate Shaping Slices | `generate_slice` | Load strategy; produce 4–7 stories; output Interaction Tree + State Model |
| Improve Shaping Skill (during slices) | `improve_strategy` | Add DO/DO NOT and or examples to existing  DO/DO NOT into strategy doc; re-run slice until approved |
| Improve Shaping Skill (post-shaping) | `improve_skill` | Take accumulated corrections from strategy doc; update base skill (content, rules) so the skill itself improves |

**Improve strategy** = corrections go into the strategy document. **Improve skill** = strategy doc improvements are applied to the skill's content and rules.

**Behavior = skill (abd-shaping).** Actions = these operations.

---

## 3. Content Decomposition (Markdown → Injectable Sections)

**Alignment convention:** Section IDs mirror file structure. `shaping.X.Y` → content lives in a file whose name matches X (e.g. `shaping-strategy.md` for `shaping.strategy.*`). Dot notation = hierarchy within that file.

**Two approaches:** The choice is whether files are organized by **domain** (what the content is about) or by **source file** (where the content lives). Section IDs and the range of referenced files follow from that choice.

| Approach | Primary driver | Files reflect | Section ID pattern | Why it matters |
|----------|----------------|---------------|--------------------|----------------|
| **Domain-led** | Organize by domain concept (strategy, process, output, validation, core) | One file per domain: `shaping-strategy.md`, `shaping-process.md`, `shaping-output.md`, `shaping-validation.md`, `shaping-core.md` | `shaping.{domain}.{topic}` — e.g. `shaping.strategy.phase`, `shaping.process.intro` | Domain coherence: everything about strategy in one place; easier to assemble per operation; consistent meaning. |
| **File-led** | Organize by existing source file | Keep current file layout; section IDs mirror file paths | `shaping.{filename}.{section}` — e.g. `shaping.intro.process`, `shaping.process.strategy_phase` | Minimal file churn: second level = source file; works when files already exist and you don't want to reorganize. |

**Recommended: Domain-led.** Group by domain so `shaping.strategy.*` → `shaping-strategy.md`, `shaping.process.*` → `shaping-process.md`, etc. Easier to pull out later; consistent meaning.

**Proposed file structure (domain-led):**

| File | Section IDs | Content |
|------|-------------|---------|
| **shaping-process.md** | `shaping.process.intro`, `shaping.process.post_shaping.review` | Process overview; post-shaping review (promote corrections to skill) |
| **shaping-strategy.md** | `shaping.strategy.phase`, `shaping.strategy.criteria`, `shaping.strategy.slices.running`, `shaping.strategy.corrections` | Strategy phase, criteria, running slices, DO/DO NOT corrections |
| **shaping-output.md** | `shaping.output.interaction_tree`, `shaping.output.state_model` | Interaction Tree and State Model format |
| **shaping-validation.md** | `shaping.validation.checklist`, `shaping.validation.rules` | Validation checklist; DO/DON'T rules (from rules/) |
| **shaping-core.md** | `shaping.core.interaction`, `shaping.core.state_concept` | Interaction and State Concept definitions |
| **rules/** (markdown + JSON) | `shaping.validation.rules` | DO/DON'T rules, scanner configs; merged into RuleSet; sibling to checklist under validation |

**Decomposition for injection:**

| Section ID | Source | Content |
|------------|--------|---------|
| `shaping.process.intro` | shaping-process.md | Process overview, when-user-says, before-you-produce |
| `shaping.process.post_shaping.review` | shaping-process.md | Post-Shaping Review: review corrections; determine changes to rules/instructions; promote cross-domain rules |
| `shaping.strategy.phase` | shaping-strategy.md | Strategy Phase (analyze, present, validate, save) |
| `shaping.strategy.criteria` | shaping-strategy.md | Splitting criteria, depth, traversal order |
| `shaping.strategy.slices.running` | shaping-strategy.md | Run slice, corrections, next slice |
| `shaping.strategy.corrections` | shaping-strategy.md | Corrections → DO/DO NOT with examples |
| `shaping.output.interaction_tree` | shaping-output.md | Interaction format, hierarchy |
| `shaping.output.state_model` | shaping-output.md | State Model format |
| `shaping.validation.checklist` | shaping-validation.md | Full validation checklist |
| `shaping.validation.rules` | rules/ (markdown + JSON) | DO/DON'T rules, scanner configs; loaded via RuleSet; sibling to checklist under validation |
| `shaping.core.interaction` | shaping-core.md | Interaction definition |
| `shaping.core.state_concept` | shaping-core.md | State Concept definition |

---

## 4. What to Inject and When

| Operation | Inject | Rationale |
|-----------|--------|-----------|
| **create_strategy** | `shaping.process.intro`, `shaping.strategy.phase`, `shaping.strategy.criteria`, `shaping.core.interaction`, `shaping.core.state_concept` | AI needs process overview, strategy phase steps, splitting/depth/traversal criteria, and domain language. No output-structure or validation yet — we're not producing output. |
| **generate_slice** | `shaping.process.intro`, `shaping.strategy.slices.running`, `shaping.strategy.corrections`, `shaping.output.interaction_tree`, `shaping.output.state_model`, `shaping.validation.checklist`, `shaping.validation.rules`, `shaping.core.interaction`, `shaping.core.state_concept`, **strategy doc** (from path) | AI produces output; needs output format, validation checklist + rules, and the approved strategy. **Corrections top of mind** — when user feedback implies reusable rule, AI adds DO/DO NOT during slice flow; no separate improve_strategy call. |
| **improve_strategy** | `shaping.strategy.corrections`, `shaping.validation.checklist` (correction format only) | AI adds DO/DO NOT to strategy doc; needs correction format and example requirements. |
| **improve_skill** | `shaping.process.post_shaping.review`, `shaping.strategy.corrections`, **strategy doc** (from path) | AI reviews strategy corrections; needs correction format and the strategy doc with accumulated DO/DO NOT; determines what to change in skill content/rules; promotes rules that apply across domains. |

**Validation approach:** No separate validate operation. `generate_slice` injects both `shaping.validation.checklist` and `shaping.validation.rules`. Rules = DO/DON'T guidance the AI follows when generating. Checklist = verify output before presenting. Assembled instructions include: *Before presenting any slice output, validate against the checklist and report status (✓ pass or ⚠ needs attention per item) in your response.* The AI's validation report is the user notification — no engine call.

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
     From shaping-core.md, shaping-process.md, shaping-strategy.md, shaping-output.md, shaping-validation.md
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

From Create Shaping Strategy steps:

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
| **Behavior = ?** | Skill (abd-shaping) |
| **Actions = ?** | Operations: create_strategy, generate_slice, improve_strategy, improve_skill |
| **What do we inject?** | Sectioned content (`shaping.*` section IDs) from shaping-process, shaping-strategy, shaping-output, shaping-validation, shaping-core, and rules — per operation |
| **When?** | When the AI is about to run that operation. Caller requests instructions, injects into prompt. |
| **Object model** | AbdSkill gets Engine injected; has `operation_sections` (map) and `instructions` (property). Instructions assembles from map + engine context. No parameters — encapsulate over passing. |
