 ABD Skill Architecture & Implementation Pattern

**Purpose:** Specific architecture, file layout, and implementation conventions for the Agile Context Engine and abd-skills. Story-by-story and epic-by-epic.

**Scope:** This document currently focuses on **Create Abd-Skill** (fixing and creating the skill). We will go into more detail on that first. Everything after the dividing line below is tentative and will be detailed later.

---

## 1. Base Engine

**Applies to:** All epics and skills (Create Abd-Skill, Initialize Agile Context Engine, Gather Context, Use Shape Skill). Base engine is foundational.

The Agile Context Engine is the core — the engine for building and running skills in their entirety. It defines structure, config, and conventions. Abd-skills are built on top of it.

### 1.1 Global Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Root** | `agilebydesign-skill`  q\]=[`s/` | Skills repo root. Engine and skills live under `skills/`. Location: `c:\dev\agilebydesign-skills`. |
| **Code location** | `skills/abd-story-synthesizer/scripts/` | Engine Python source (self-contained). Other skills have their own scripts. |
| **Module/class mapping** | One file per module, one class per concept | `scripts/abd_skill.py` → `class AbdSkill`; `scripts/engine.py` → `class AgileContextEngine`. |
| **Type safety** | **Yes — pydantic** | Use pydantic for config, strategy, and DTOs. Typed function signatures. Catches config/schema errors early. |
| **Structured data** | **JSON** | Config, strategy metadata, scanner rules, engine state. |
| **Text / instructions / rules** | **Markdown** | Content files, rules, instructions, assembled agent output. |

### 1.1.5 Path (Cross-cutting)

**Applies to:** All epics (file paths used throughout).

**All file-returning properties return Path objects, not strings.**

The Path object represents the file or directory at that path. Use Path for:

- **OS separators** — Different operating systems use different separators; Path handles this.
- **Centralized path logic** — Dispersing path logic across the codebase is error-prone; a single Path abstraction keeps it in one place.
- **Resolution, joining, existence checks** — Path provides resolve(), join, exists(), read_text(), etc.

**Implementation:** When integrating with agile_bots, reuse `agile_bots/src/bot_path` (BotPath, StoryGraphPaths). The engine and abd-skills may depend on that module or a shared copy. For standalone use, Path logic lives in engine scripts.

| Property / Operation | Returns | Notes |
|----------------------|---------|-------|
| Any property that points to a file or directory | `Path` | Never `String` for file paths |
| Path.join(...) | `Path` | Use Path for joining |
| Path.resolve() | `Path` | Absolute, normalized |

---

### 1.2 Engine vs Skill Scripts: Code Sharing and Responsibility

**Principle:** All structural logic lives in the engine. Skill scripts are thin entry points that call engine APIs.

### Centralized Code (Engine)

| Location | Responsibility |
|----------|----------------|
| `skills/abd-story-synthesizer/scripts/` | Defines what an abd-skill is: directory layout, content pieces, rules structure, scripts folder, output paths. Engine owns the schema. |
| `skills/abd-story-synthesizer/scripts/abd_skill.py` | `AbdSkill` — receives Engine; `operation_sections`, `instructions`. |
| `skills/abd-story-synthesizer/scripts/engine.py` | `Engine.scaffold_skill(name, path)`, `Engine.build_skill(path)` — creates scaffold and assembles AGENTS.md. |

The engine is the **single source of truth** for:
- What a skill directory contains
- What gets saved where
- Content piece names (core, process, strategy, output, validation, script-invocation)
- Output conventions

### Skill Scripts

| Location | Responsibility |
|----------|----------------|
| `skills/agile-skill-build/scripts/scaffold.py` | Parses CLI args (e.g. `--name`, `--path`); calls `Engine.scaffold_skill(name, path)`. Does **not** define structure. |
| `skills/agile-skill-build/scripts/build.py` | Invokes engine build API. Assembles content per engine conventions. |
| `skills/abd-<name>/scripts/*.py` | Any skill script: parses params, delegates to engine. No structural logic. |

### Script Invocation Markdown (AI Guidance)

Each skill includes **Markdown that instructs the AI on how to call the Python scripts**. The AI reads this to know:

- Which script to run (e.g. `scripts/scaffold.py`, `scripts/build.py`)
- What parameters to pass (e.g. `--name`, `--path`, `--skill-space`)
- When to call (e.g. after content is complete, before strategy creation)
- What to expect (success output, error handling, next steps)

| Location | Purpose |
|----------|---------|
| `skills/agile-skill-build/content/script-invocation.md` | How to invoke scaffold.py, build.py; params, examples, sequencing. |
| `skills/abd-<name>/content/script-invocation.md` | Per-skill script usage when the skill has scripts. Optional if skill has no scripts. |

This Markdown is part of the skill content. The AI reads it before invoking Python and follows it when orchestrating the workflow (e.g. Create Abd-Skill, Gather Context).

### Relationship

```
┌─────────────────────────────────────────────────────────────┐
│  Engine (skills/abd-story-synthesizer/scripts/)               │
│  - Defines skill structure, paths, conventions               │
│  - scaffold_skill(name, path)                                │
│  - get_skill_scaffold_spec() → { dirs, files, templates }    │
│  - build_skill(skill_path)                                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ calls
                              │
┌─────────────────────────────────────────────────────────────┐
│  Skill Scripts (skills/abd-*/scripts/*.py)                    │
│  - Parse CLI/params                                          │
│  - Call engine.scaffold_skill(...) or engine.build_skill()   │
│  - No structural logic; no duplicate path/file definitions   │
└─────────────────────────────────────────────────────────────┘
```

### Rules

1. **Common structure for skills is centralized.** Skills do not define the basic structure of a skill, the standard files in a skill, or where the standard things go. They ask the engine. **Skill-specific logic is decentralized** — each skill owns its own domain logic. 
2. **Engine exposes APIs.** `scaffold_skill()`, `build_skill()`, `get_skill_scaffold_spec()`, etc. Scripts call these.
3. **Scripts are entry points.** They adapt CLI/env/params into engine calls. They can be run standalone (e.g. `python scripts/scaffold.py --name abd-foo`) or invoked by AI/tooling.
4. **Engine via path.** Skill scripts add their own `scripts/` to `sys.path` and `from engine import build_skill` (or `scaffold_skill`). Each skill with an engine is self-contained.

---

### 1.3 Root Structure (Engine)

```
agilebydesign-skills/
├── skills/
│   ├── abd-story-synthesizer/  # Engine + synthesizer skill (self-contained)
│   │   ├── scripts/        # Engine Python code
│   │   │   ├── engine.py   # AgileContextEngine
│   │   │   ├── abd_skill.py
│   │   │   ├── config.py
│   │   │   ├── rule_set.py
│   │   │   ├── instructions.py
│   │   │   └── build.py
│   │   ├── conf/
│   │   │   └── abd-config.json
│   │   ├── content/       # Markdown: core, process, strategy, output, validation
│   │   │   ├── core.md
│   │   │   ├── process.md
│   │   │   ├── strategy.md
│   │   │   ├── output.md
│   │   │   ├── validation.md
│   │   │   └── script-invocation.md
│   │   ├── rules/
│   │   │   ├── scanners.json
│   │   │   └── *.md
│   │   ├── AGENTS.md
│   │   ├── SKILL.md
│   │   └── README.md
│   ├── agile-skill-build/  # Scaffold + build skill
│   └── ...
└── README.md
```

**Config path:** Project `conf/abd-config.json` (e.g. `mm3e/conf/abd-config.json`). Engine resolves via `engine_root` so config is always found.

---

### 1.4 Config Format

**File:** `conf/abd-config.json`

```json
{
  "skills": ["."],
  "skills_config": {
    "order": ["."]
  },
  "context_paths": []
}
```

- `skills`: List of skill paths (relative to engine root). Often `["."]` when config lives in the skill. Skill space is derived from skill path (parent of `.agents/skills` or parent of `skills`).
- `skills_config.order`: Optional load/run order.
- `constraints`: Architecture-pattern constraints (e.g. `{"pattern": "must use X", "scope": "Epic"}`).

---

### 1.5 Engine Initialization (Initialize Agile Context Engine)

**Applies to:** Epic **Initialize Agile Context Engine** — Story: *Load registered skills and rule sets*.

Config format and paths are in §1.4 and §1.3.

#### Load registered skills and rule sets

| Concept / Behavior | Implementation |
|--------------------|----------------|
| **Skills list** | Read from `conf/abd-config.json` → `skills` array (§1.4) |
| **Per-skill load** | For each path in `skills`, instantiate `AbdSkill` at `skills/<path>/` |
| **Rule set load** | Per skill: `rules/*.md` (Markdown), `rules/scanners.json` (JSON). Merge into unified `RuleSet` per skill. |
| **Skill space** | Derived from skill path — parent of `.agents/skills` (or parent of `skills` when in engine). No config. |
| **Output folders** | Create `<skill_space>/<output-folder>/` for each skill; output folder = skill name with `abd-` stripped (e.g. abd-story-synthesizer → story-synthesizer, abd-context-to-memory → context-to-memory) |
| **Engine API** | `Engine.load()` — reads config, loads skills, derives skill space, creates output dirs |
| **Failure** | Malformed JSON; missing skill path; invalid rule path → report and fail |

---

## 2. Abd-Skill

**Applies to:** Epic Create Abd-Skill;

Abd-skills are built on top of the base engine. They use engine APIs for scaffold, build, and structure.

Some skills will inherit from the base abd_skills when they need to do common things around strategy (e.g. create strategy, load/save strategy, apply rules).

### 2.1 Concept Implementation (Create Abd-Skill)

Domain concepts for Create Abd-Skill, mapped to implementation: exact file path, format. Parameterization where needed (e.g. `<name>`).

#### AbdSkill

**Object model:** AbdSkill receives `Engine` injected at construction. Uses engine for context (workspace, strategy_path, etc.). No context parameters on instruction assembly — pulls from engine.

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Class | `skills/abd-story-synthesizer/scripts/abd_skill.py` → `class AbdSkill` |
| `AbdSkill.engine` | Injected at construction. Used for context (workspace, strategy_path, slice_index). |
| `AbdSkill.path` | `skills/abd-<name>/` |
| `AbdSkill.rule_set` | `skills/abd-<name>/rules/` (dir); `rules/scanners.json` (JSON); `rules/*.md` (Markdown) |
| `AbdSkill.scripts` | `skills/abd-<name>/scripts/` (dir); each script `scripts/<script>.py` |
| `AbdSkill.core_definition`, `intro`, `output_structure`, `shape`, `validation` | `skills/abd-<name>/content/*.md` |
| `AbdSkill.operation_sections` | Map: operation → section IDs to inject (create_strategy, generate_slice, improve_strategy, improve_skill) |
| `AbdSkill.instructions` | Property. Assembles from `operation_sections` and engine context. No context parameter. |
| `AbdSkill.assembled_agent` | See AssembledAgent |
| `AbdSkill.build()` | Invokes `Engine.build_skill(path)`; see BuildScript |

#### BuildScript

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `BuildScript.path` | `skills/abd-<name>/scripts/build.py` |
| `BuildScript.run()` | Calls `Engine.build_skill(skill_path)`; engine reads content/*.md, assembles, writes AGENTS.md |

#### AssembledAgent

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `AssembledAgent.path` | `skills/abd-<name>/AGENTS.md` |
| `AssembledAgent.content` | Merged Markdown: core + process + strategy + output + validation (in order) |

#### BuildAbdSkill (agile-skill-build)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Skill root | `skills/agile-skill-build/` |
| Scaffold script | `skills/agile-skill-build/scripts/scaffold.py` |
| Build script (for agile-skill-build itself) | `skills/agile-skill-build/scripts/build.py` |
| Script invocation guidance | `skills/agile-skill-build/content/script-invocation.md` (Markdown) — AI reads to know how to call scaffold.py, build.py |

#### Scaffold spec (engine)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `Engine.get_skill_scaffold_spec()` | Returns structure; no file — in-memory spec. |
| `Engine.scaffold_skill(name, path)` | Creates `skills/abd-<name>/` with: `content/*.md`, `rules/`, `scripts/`, `metadata.json`, `SKILL.md`, `README.md` |
| Content files (scaffold) | `content/core.md`, `process.md`, `strategy.md`, `output.md`, `validation.md`, `script-invocation.md` — empty or template Markdown |
| Metadata | `metadata.json` (JSON) |
| Skill descriptor | `SKILL.md` (Markdown) |

#### Per-skill outputs (created by scaffold or build)

| Artifact | Path | Format |
|----------|------|--------|
| Assembled agent | `skills/abd-<name>/AGENTS.md` | Markdown |
| Metadata | `skills/abd-<name>/metadata.json` | JSON |
| Scanner rules | `skills/abd-<name>/rules/scanners.json` | JSON |
| Rule markdown | `skills/abd-<name>/rules/*.md` | Markdown |

---

### 2.2 Epic: Create Abd-Skill

**Applies to:** Epic **Create Abd-Skill** — Stories: *Create scaffolding via script*, *AI fills content pieces from input*, *User completes missing pieces*, *AI reruns build script*.

Implementation details (paths, scripts, engine APIs, output structure) are in §2.1 Concept Implementation. The only story-specific behavior not covered there:

| Story | Additional behavior |
|-------|---------------------|
| **User completes missing pieces** | AI returns list of missing/incomplete pieces (e.g. `["core", "validation"]`); user edits `content/<piece>.md`; AI re-reads and re-validates. |

### Abd-Skill Directory Layout (output of Create Skill)

```
skills/abd-<name>/
├── content/
│   ├── core.md
│   ├── process.md
│   ├── strategy.md
│   ├── output.md
│   ├── validation.md
│   └── script-invocation.md    # AI guidance: how to call scripts (params, when, what to expect)
├── rules/
│   ├── scanners.json          # or per-scanner JSON
│   └── *.md                   # rule markdown if any
├── scripts/
│   ├── build.py
│   ├── scaffold.py            # (agile-skill-build only)
│   └── ...                    # other scripts
├── AGENTS.md                  # assembled agent file (output of build)
├── SKILL.md                   # skill descriptor
├── README.md
└── metadata.json
```

---

## 3. Instruction Injection

**Applies to:** Epic **Use Story Synthesizer Skill** (Create Strategy, Generate Slices, Improve Strategy); Epic **Initialize Agile Context Engine** (Load registered skills and rule sets — AbdSkill must support `operation_sections` and `instructions`).

Instructions are assembled and **injected** into the AI prompt. The AI doesn't "go read" the rules — they're given. The caller (MCP, CLI, panel, etc.) asks the skill for instructions before the AI runs an operation and injects the assembled markdown into the prompt.

### 3.1 Operations → Stories

| Story | Operation | What it does |
|-------|-----------|--------------|
| Create Strategy | `create_strategy` | Analyze source; propose epic breakdown, slice order, assumptions; save strategy doc |
| Generate Slices | `generate_slice` | Load strategy; produce 4–7 stories; output Interaction Tree + State Model |
| Improve Strategy | `improve_strategy` | Add DO/DO NOT to strategy doc; re-run slice until approved |
| Improve Skill (post-synthesis) | `improve_skill` | Take accumulated corrections; update base skill content/rules |

**Improve strategy** = corrections go into the strategy document. **Improve skill** = strategy doc improvements are applied to the skill's content and rules.

### 3.2 Content Decomposition (Section IDs)

**Applies to:** Epic **Initialize Agile Context Engine** (Load registered skills — skills expose sectioned content); Epic **Use Shape Skill** (all operations — caller assembles per operation).

**Alignment convention:** Section IDs mirror domain. `story_synthesizer.X.Y` → content in file matching X (e.g. `strategy.md` for `story_synthesizer.strategy.*`). **Domain-led** layout: one file per domain.

| File | Section IDs | Content |
|------|-------------|---------|
| **process.md** | `story_synthesizer.process.intro`, `story_synthesizer.process.post_synthesis.review` | Process overview; post-synthesis review |
| **strategy.md** | `story_synthesizer.strategy.iterative`, `story_synthesizer.strategy.criteria`, `story_synthesizer.strategy.slices.running`, `story_synthesizer.strategy.corrections` | Iterative Strategy, criteria, running slices, DO/DO NOT |
| **output.md** | `story_synthesizer.output.interaction_tree`, `story_synthesizer.output.state_model` | Interaction Tree and State Model format |
| **validation.md** | `story_synthesizer.validation.checklist`, `story_synthesizer.validation.rules` | Validation checklist; DO/DON'T rules |
| **core.md** | `story_synthesizer.core.interaction`, `story_synthesizer.core.state_concept` | Interaction and State Concept definitions |
| **rules/** (markdown + JSON) | `story_synthesizer.validation.rules` | DO/DON'T rules, scanner configs; merged into RuleSet |

### 3.3 What to Inject and When

**Applies to:** Epic **Use Story Synthesizer Skill** — Stories: Create Strategy, Generate Slices, Improve Strategy.

| Operation | Inject | Story |
|-----------|--------|-------|
| **create_strategy** | `story_synthesizer.process.intro`, `story_synthesizer.strategy.iterative`, `story_synthesizer.strategy.criteria`, `story_synthesizer.core.interaction`, `story_synthesizer.core.state_concept` | Create Strategy |
| **generate_slice** | `story_synthesizer.process.intro`, `story_synthesizer.strategy.slices.running`, `story_synthesizer.strategy.corrections`, `story_synthesizer.output.*`, `story_synthesizer.validation.checklist`, `story_synthesizer.validation.rules`, `story_synthesizer.core.*`, **strategy doc** (from path) | Generate Slices |
| **improve_strategy** | `story_synthesizer.strategy.corrections`, `story_synthesizer.validation.checklist` (correction format only) | Improve Strategy |
| **improve_skill** | `story_synthesizer.process.post_synthesis.review`, `story_synthesizer.strategy.corrections`, **strategy doc** (from path) | Improve Skill |

**Corrections in generate_slice:** When user feedback implies a reusable rule, AI adds DO/DO NOT during the slice flow; no separate `improve_strategy` call needed.

**Validation:** No separate validate operation. `generate_slice` injects both checklist and rules. AI validates against checklist before presenting; reports status (✓ pass or ⚠ needs attention) in response.

**Scanners:** Programmatic validators live in `rules/` as config. Flow: (1) Generate output. (2) Run scanners. (3) Determine false positives. (4) Inject problems, fixes, and report location into the next prompt. AI addresses real issues in the next iteration.

**Context (always available):** Context source paths, workspace path, strategy path (when exists). Caller provides these; not "injected" as instruction content.

### 3.4 Injection Flow

**Applies to:** Epic **Use Story Synthesizer Skill** — Stories: Create Strategy, Generate Slices, Improve Strategy.

| Step | Caller | Engine / Skill |
|------|--------|----------------|
| 1 | User requests operation (e.g. create strategy, generate slice 1) | — |
| 2 | Asks skill for instructions: `skill.instructions.display_content("create_strategy")` | Skill assembles from `operation_sections` + engine context |
| 3 | Injects assembled markdown + context paths into AI prompt | — |
| 4 | AI runs operation; instructions already in prompt | — |

**When:** Before the AI runs the operation. Caller injects; AI receives — doesn't have to "load" guidelines.

### 3.5 Object Model (AbdSkill, Instructions)

**Applies to:** Epic **Initialize Agile Context Engine** (Load skills — inject Engine into each AbdSkill); Epic **Create Abd-Skill** (AbdSkill structure).

| Concept | Implementation |
|---------|----------------|
| **Engine injection** | AbdSkill receives `Engine` at construction. Uses engine for workspace, strategy_path, slice_index. |
| **operation_sections** | Map: operation → section IDs. Keys: `create_strategy`, `generate_slice`, `improve_strategy`, `improve_skill`. From skill config. |
| **instructions** | Property. Assembles from `operation_sections` and engine context. No context parameter — pulls from engine. |
| **display_content(operation)** | Returns markdown for that operation. Caller injects into prompt. |
| **Context** | Comes from engine (workspace, strategy_path, etc.). No context parameter — injected. |

---

**══════════════════════════════════════════════════════════════**  
**TENTATIVE — To Be Detailed Later**  
**══════════════════════════════════════════════════════════════**

Everything below is placeholder. We will go into more detail on Create Abd-Skill first.

---

## 8. Epic: Gather Context

### Story: Gather context for synthesis run

| Aspect | Implementation |
|--------|----------------|
| **Populate memory** | Invoke abd-context-to-memory (or equivalent): convert → chunk → sync to `<workspace>/context-to-memory/memory/`. |
| **Memory layout** | Each source file → one folder under `memory/`; folder = one `Memory`; chunks as `.md` files with `<!-- Source: path -->`. |
| **ContextSources** | `scripts/context_sources.py` (or equivalent) — `class ContextSources` with `gather(content_sources, workspace, strategy)`. |
| **Memories** | `scripts/memories.py` (or equivalent) — `Memories`, `Memory`, `Chunk`. |
| **Refer** | `Memories.refer()` returns `Chunk[]` for synthesis. |

**Memory path:** `<skill_space>/context-to-memory/memory/<artifact_id>/`  
**Chunk files:** `chunk_001.md`, `chunk_002.md`, … with source attribution in each.

---

## 9. Epic: Use Shape Skill

### Story: Create Strategy

| Aspect | Implementation |
|--------|----------------|
| **Output path** | `<skill_space>/story-synthesizer/strategy.md` |
| **Format** | Markdown. Structure: source analysis, epic breakdown, slice order, assumptions. |
| **Strategy** | `scripts/strategy.py` (or equivalent) — `class Strategy` with `save(path)`, `load(path)`, `update(rules)`. |
| **Metadata (optional)** | `<skill_space>/story-synthesizer/strategy.json` for structured parts (epics, slices) if needed. |

### Story: Generate Slices

| Aspect | Implementation |
|--------|----------------|
| **Output** | Interaction Tree + State Model. |
| **Paths** | `<skill_space>/story-synthesizer/slice-<n>/interaction-tree.md`, `slice-<n>/state-model.md` (or `.json` for structured). |
| **Slice** | `scripts/slice.py` (or equivalent) — `class Slice` with `produce(strategy): (InteractionTree, StateModel)`. |

### Story: Improve Skill

| Aspect | Implementation |
|--------|----------------|
| **Update** | `Strategy.update(rules)` appends DO/DO NOT rules; persists to same strategy path. |
| **Re-run** | Regenerate slice with updated strategy. |

---

## 10. Skill Space Output Layout (Tentative)

```
<skill_space>/
├── story-synthesizer/
│   ├── strategy.md
│   └── slice-1/
│       ├── interaction-tree.md
│       └── state-model.md
├── context-to-memory/
│   └── memory/
│       ├── <artifact_id_1>/
│       │   ├── chunk_001.md
│       │   └── ...
│       └── <artifact_id_2>/
│           └── ...
└── ...                        # user's project files
```

---

## 11. Python Module → Concept Mapping (Tentative)

| Concept | Module | Class |
|---------|--------|-------|
| AgileContextEngine | `skills/abd-story-synthesizer/scripts/engine.py` | `AgileContextEngine` |
| AbdSkill | `skills/abd-story-synthesizer/scripts/abd_skill.py` | `AbdSkill` |
| RuleSet | `skills/abd-story-synthesizer/scripts/rule_set.py` | `RuleSet` |
| AbdConfig | `skills/abd-story-synthesizer/scripts/config.py` | `AbdConfig` |
| Instructions | `skills/abd-story-synthesizer/scripts/instructions.py` | `Instructions` |
| ContextSources | (future) | `ContextSources` |
| Memories | (future) | `Memories`, `Memory`, `Chunk` |
| Strategy | (future) | `Strategy` |
| Slice | (future) | `Slice` |

---

## 12. Pydantic Models (Tentative)

```python
# skills/abd-story-synthesizer/scripts/config.py
from pydantic import BaseModel
from pathlib import Path

class AbdConfig(BaseModel):
    skills: list[str]
    skills_config: dict | None = None
    constraints: list[dict] = []

    class Config:
        extra = "ignore"  # ignore legacy skill_space_path
```

---

## 13. Summary Table (Tentative)

| Artifact | Format | Location |
|----------|--------|----------|
| Engine config | JSON | `skills/abd-story-synthesizer/conf/abd-config.json` (or per-skill `conf/abd-config.json`) |
| Skill content | Markdown | `skills/abd-<name>/content/*.md` (includes script-invocation.md for AI) |
| Scanner rules | JSON | `skills/abd-<name>/rules/*.json` |
| Assembled agent | Markdown | `skills/abd-<name>/AGENTS.md` |
| Strategy | Markdown | `<skill_space>/story-synthesizer/strategy.md` |
| Memory chunks | Markdown | `<skill_space>/context-to-memory/memory/<id>/*.md` |
| Slice output | Markdown / JSON | `<skill_space>/story-synthesizer/slice-<n>/*.md` |
