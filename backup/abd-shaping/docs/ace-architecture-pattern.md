# ACE Skill Architecture & Implementation Pattern

**Purpose:** Specific architecture, file layout, and implementation conventions for the Agile Context Engine and ace-skills. Story-by-story and epic-by-epic.

**Scope:** This document currently focuses on **Create Ace-Skill** (fixing and creating the skill). We will go into more detail on that first. Everything after the dividing line below is tentative and will be detailed later.

---

## 1. Base Engine

**Applies to:** All epics and skills (Create Ace-Skill, Initialize Agile Context Engine, Gather Context, Use Shape Skill). Base engine is foundational.

The Agile Context Engine is the core — the engine for building and running skills in their entirety. It defines structure, config, and conventions. Ace-skills are built on top of it.

### 1.1 Global Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Root** | `agile-context-engine/` | Engine folder is the root of the skill space. All engine code, config, and skills live under this. Location: `C:\dev\agile-context-engine`. |
| **Code location** | `src/` | Python source under root. |
| **Module/class mapping** | One file per module, one class per concept | `src/skill_space.py` → `class SkillSpace`; `src/ace_skill.py` → `class AceSkill`. |
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

**Implementation:** Reuse `agile_bots/src/bot_path` (BotPath, StoryGraphPaths) in its entirety. Do not reimplement. The engine and ace-skills should depend on that module or a shared copy of it.

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
| `src/` | Defines what an ace-skill is: directory layout, content pieces, rules structure, scripts folder, output paths. Engine owns the schema. |
| `src/ace_skill.py` | `AceSkill.scaffold_spec()` or `Engine.get_skill_scaffold_spec()` — returns the canonical structure (paths, file names, templates). |
| `src/engine.py` | `Engine.scaffold_skill(name, path)` — creates the scaffold on disk using the spec. Engine does the actual file/dir creation. |

The engine is the **single source of truth** for:
- What a skill directory contains
- What gets saved where
- Content piece names (core-definitions, intro, output-structure, shaping-process, validation, script-invocation)
- Output conventions

### Skill Scripts

| Location | Responsibility |
|----------|----------------|
| `skills/ace-build/scripts/scaffold.py` | Parses CLI args (e.g. `--name`, `--path`); calls `Engine.scaffold_skill(name, path)`. Does **not** define structure. |
| `skills/ace-build/scripts/build.py` | Invokes engine build API (or shared build logic). Assembles content per engine conventions. |
| `skills/ace-<name>/scripts/*.py` | Any skill script: parses params, delegates to engine. No structural logic. |

### Script Invocation Markdown (AI Guidance)

Each skill includes **Markdown that instructs the AI on how to call the Python scripts**. The AI reads this to know:

- Which script to run (e.g. `scripts/scaffold.py`, `scripts/build.py`)
- What parameters to pass (e.g. `--name`, `--path`, `--skill-space`)
- When to call (e.g. after content is complete, before strategy creation)
- What to expect (success output, error handling, next steps)

| Location | Purpose |
|----------|---------|
| `skills/ace-build/content/script-invocation.md` (or `scripts/README.md`) | How to invoke scaffold.py, build.py; params, examples, sequencing. |
| `skills/ace-<name>/content/script-invocation.md` | Per-skill script usage when the skill has scripts. Optional if skill has no scripts. |

This Markdown is part of the skill content. The AI reads it before invoking Python and follows it when orchestrating the workflow (e.g. Create Ace-Skill, Gather Context).

### Relationship

```
┌─────────────────────────────────────────────────────────────┐
│  Engine (src/)                                               │
│  - Defines skill structure, paths, conventions               │
│  - scaffold_skill(name, path)                                │
│  - get_skill_scaffold_spec() → { dirs, files, templates }    │
│  - build_skill(skill_path)                                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ calls
                              │
┌─────────────────────────────────────────────────────────────┐
│  Skill Scripts (skills/ace-*/scripts/*.py)                    │
│  - Parse CLI/params                                          │
│  - Call engine.scaffold_skill(...) or engine.build_skill()   │
│  - No structural logic; no duplicate path/file definitions   │
└─────────────────────────────────────────────────────────────┘
```

### Rules

1. **Common structure for skills is centralized.** Skills do not define the basic structure of a skill, the standard files in a skill, or where the standard things go. They ask the engine. **Skill-specific logic is decentralized** — each skill owns its own domain logic. 
2. **Engine exposes APIs.** `scaffold_skill()`, `build_skill()`, `get_skill_scaffold_spec()`, etc. Scripts call these.
3. **Scripts are entry points.** They adapt CLI/env/params into engine calls. They can be run standalone (e.g. `python scripts/scaffold.py --name ace-foo`) or invoked by AI/tooling.
4. **Shared package.** Engine is installable (e.g. `pip install -e .` from engine root). Skill scripts run with engine on `PYTHONPATH` or installed, and call `from agile_context_engine.engine import AgileContextEngine` (or `engine.scaffold_skill`). Scripts never duplicate engine logic.

---

### 1.3 Root Structure (Engine)

```
agile-context-engine/
├── src/                    # Python code
│   ├── __init__.py
│   ├── engine.py           # AgileContextEngine
│   ├── skill_space.py       # SkillSpace
│   ├── ace_skill.py        # AceSkill
│   ├── rule_set.py         # RuleSet
│   ├── context_sources.py  # ContextSources
│   ├── memories.py         # Memories, Memory, Chunk
│   ├── strategy.py         # Strategy
│   ├── slice.py            # Slice
│   └── ...
├── conf/                   # Engine config (outside any skill space)
│   └── ace-config.json
├── skills/                 # Registered ace-skills
│   ├── ace-shaping/        # Example: one skill expanded
│   │   ├── content/        # Markdown: core definitions, process, validation
│   │   │   ├── core-definitions.md
│   │   │   ├── intro.md
│   │   │   ├── output-structure.md
│   │   │   ├── shaping-process.md
│   │   │   └── validation.md
│   │   ├── rules/          # DO/DO NOT rules, scanners
│   │   │   ├── scanners.json
│   │   │   └── *.md
│   │   ├── scripts/        # Build, scaffold, etc.
│   │   │   └── build.py    # Assembles content → AGENTS.md
│   │   ├── AGENTS.md       # Assembled output (built from content)
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── metadata.json
│   ├── ace-context-to-memory/
│   └── ace-build/          # Build-ACE skill
├── pyproject.toml
├── requirements.txt
└── README.md
```

**Config path:** `agile-context-engine/conf/ace-config.json` (relative to engine root). Engine resolves via `engine_path` so config is always found.

---

### 1.4 Config Format

**File:** `conf/ace-config.json`

```json
{
  "skills": ["skills/ace-shaping", "skills/ace-context-to-memory", "skills/ace-build"],
  "skills_config": {
    "order": ["ace-context-to-memory", "ace-shaping"]
  },
  "constraints": []
}
```

- `skills`: List of skill paths (relative to engine root). Skill space is derived from skill path (parent of `.agents/skills`).
- `skills_config.order`: Optional load/run order.
- `constraints`: Architecture-pattern constraints (e.g. `{"pattern": "must use X", "scope": "Epic"}`).

---

### 1.5 Engine Initialization (Initialize Agile Context Engine)

**Applies to:** Epic **Initialize Agile Context Engine** — Story: *Load registered skills and rule sets*.

Config format and paths are in §1.4 and §1.3.

#### Load registered skills and rule sets

| Concept / Behavior | Implementation |
|--------------------|----------------|
| **Skills list** | Read from `conf/ace-config.json` → `skills` array (§1.4) |
| **Per-skill load** | For each path in `skills`, instantiate `AceSkill` at `skills/<path>/` |
| **Rule set load** | Per skill: `rules/*.md` (Markdown), `rules/scanners.json` (JSON). Merge into unified `RuleSet` per skill. |
| **Skill space** | Derived from skill path — parent of `.agents/skills` (or parent of `skills` when in engine). No config. |
| **Output folders** | Create `<skill_space>/<output-folder>/` for each skill; output folder = skill name with `ace-` stripped (e.g. ace-shaping → shaping, ace-context-to-memory → context-to-memory) |
| **Engine API** | `Engine.load()` — reads config, loads skills, derives skill space, creates output dirs |
| **Failure** | Malformed JSON; missing skill path; invalid rule path → report and fail |

---

## 2. Ace-Skill

**Applies to:** Epic Create Ace-Skill;

Ace-skills are built on top of the base engine. They use engine APIs for scaffold, build, and structure.

Some skills will inherit from the base ace_skills when they need to do common things around strategy (e.g. create strategy, load/save strategy, apply rules).

### 2.1 Concept Implementation (Create Ace-Skill)

Domain concepts for Create Ace-Skill, mapped to implementation: exact file path, format. Parameterization where needed (e.g. `<name>`).

#### AceSkill

**Object model:** AceSkill receives `Engine` injected at construction. Uses engine for context (workspace, strategy_path, etc.). No context parameters on instruction assembly — pulls from engine.

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Class | `src/ace_skill.py` → `class AceSkill` |
| `AceSkill.engine` | Injected at construction. Used for context (workspace, strategy_path, slice_index). |
| `AceSkill.path` | `skills/ace-<name>/` |
| `AceSkill.rule_set` | `skills/ace-<name>/rules/` (dir); `rules/scanners.json` (JSON); `rules/*.md` (Markdown) |
| `AceSkill.scripts` | `skills/ace-<name>/scripts/` (dir); each script `scripts/<script>.py` |
| `AceSkill.core_definition`, `intro`, `output_structure`, `shape`, `validation` | `skills/ace-<name>/content/*.md` |
| `AceSkill.operation_sections` | Map: operation → section IDs to inject (create_strategy, generate_slice, improve_strategy, improve_skill) |
| `AceSkill.instructions` | Property. Assembles from `operation_sections` and engine context. No context parameter. |
| `AceSkill.assembled_agent` | See AssembledAgent |
| `AceSkill.build()` | Invokes `Engine.build_skill(path)`; see BuildScript |

#### BuildScript

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `BuildScript.path` | `skills/ace-<name>/scripts/build.py` |
| `BuildScript.run()` | Calls `Engine.build_skill(skill_path)`; engine reads content/*.md, assembles, writes AGENTS.md |

#### AssembledAgent

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `AssembledAgent.path` | `skills/ace-<name>/AGENTS.md` |
| `AssembledAgent.content` | Merged Markdown: core-definitions + intro + output-structure + shaping-process + validation (in order) |

#### BuildAceSkill (ace-build)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| Skill root | `skills/ace-build/` |
| Scaffold script | `skills/ace-build/scripts/scaffold.py` |
| Build script (for ace-build itself) | `skills/ace-build/scripts/build.py` |
| Script invocation guidance | `skills/ace-build/content/script-invocation.md` (Markdown) — AI reads to know how to call scaffold.py, build.py |

#### Scaffold spec (engine)

| Concept / Property / Operator | Implementation |
|------------------------------|----------------|
| `Engine.get_skill_scaffold_spec()` | Returns structure; no file — in-memory spec. |
| `Engine.scaffold_skill(name, path)` | Creates `skills/ace-<name>/` with: `content/*.md`, `rules/`, `scripts/`, `metadata.json`, `SKILL.md`, `README.md` |
| Content files (scaffold) | `content/core-definitions.md`, `intro.md`, `output-structure.md`, `shaping-process.md`, `validation.md`, `script-invocation.md` — empty or template Markdown |
| Metadata | `metadata.json` (JSON) |
| Skill descriptor | `SKILL.md` (Markdown) |

#### Per-skill outputs (created by scaffold or build)

| Artifact | Path | Format |
|----------|------|--------|
| Assembled agent | `skills/ace-<name>/AGENTS.md` | Markdown |
| Metadata | `skills/ace-<name>/metadata.json` | JSON |
| Scanner rules | `skills/ace-<name>/rules/scanners.json` | JSON |
| Rule markdown | `skills/ace-<name>/rules/*.md` | Markdown |

---

### 2.2 Epic: Create Ace-Skill

**Applies to:** Epic **Create Ace-Skill** — Stories: *Create scaffolding via script*, *AI fills content pieces from input*, *User completes missing pieces*, *AI reruns build script*.

Implementation details (paths, scripts, engine APIs, output structure) are in §2.1 Concept Implementation. The only story-specific behavior not covered there:

| Story | Additional behavior |
|-------|---------------------|
| **User completes missing pieces** | AI returns list of missing/incomplete pieces (e.g. `["core-definitions", "validation"]`); user edits `content/<piece>.md`; AI re-reads and re-validates. |

### Ace-Skill Directory Layout (output of Create Skill)

```
skills/ace-<name>/
├── content/
│   ├── core-definitions.md
│   ├── intro.md
│   ├── output-structure.md
│   ├── shaping-process.md
│   ├── validation.md
│   └── script-invocation.md    # AI guidance: how to call scripts (params, when, what to expect)
├── rules/
│   ├── scanners.json          # or per-scanner JSON
│   └── *.md                   # rule markdown if any
├── scripts/
│   ├── build.py
│   ├── scaffold.py            # (ace-build only)
│   └── ...                    # other scripts
├── AGENTS.md                  # assembled agent file (output of build)
├── SKILL.md                   # skill descriptor
├── README.md
└── metadata.json
```

---

## 3. Instruction Injection

**Applies to:** Epic **Use Shape Skill** (Create Shaping Strategy, Generate Slices, Improve Strategy); Epic **Initialize Agile Context Engine** (Load registered skills and rule sets — AceSkill must support `operation_sections` and `instructions`).

Instructions are assembled and **injected** into the AI prompt. The AI doesn't "go read" the rules — they're given. The caller (MCP, CLI, panel, etc.) asks the skill for instructions before the AI runs an operation and injects the assembled markdown into the prompt.

### 3.1 Operations → Stories

| Story | Operation | What it does |
|-------|-----------|--------------|
| Create Shaping Strategy | `create_strategy` | Analyze source; propose epic breakdown, slice order, assumptions; save strategy doc |
| Generate Shaping Slices | `generate_slice` | Load strategy; produce 4–7 stories; output Interaction Tree + State Model |
| Improve Strategy | `improve_strategy` | Add DO/DO NOT to strategy doc; re-run slice until approved |
| Improve Skill (post-shaping) | `improve_skill` | Take accumulated corrections; update base skill content/rules |

**Improve strategy** = corrections go into the strategy document. **Improve skill** = strategy doc improvements are applied to the skill's content and rules.

### 3.2 Content Decomposition (Section IDs)

**Applies to:** Epic **Initialize Agile Context Engine** (Load registered skills — skills expose sectioned content); Epic **Use Shape Skill** (all operations — caller assembles per operation).

**Alignment convention:** Section IDs mirror domain. `shaping.X.Y` → content in file matching X (e.g. `shaping-strategy.md` for `shaping.strategy.*`). **Domain-led** layout: one file per domain.

| File | Section IDs | Content |
|------|-------------|---------|
| **shaping-process.md** | `shaping.process.intro`, `shaping.process.post_shaping.review` | Process overview; post-shaping review |
| **shaping-strategy.md** | `shaping.strategy.phase`, `shaping.strategy.criteria`, `shaping.strategy.slices.running`, `shaping.strategy.corrections` | Strategy phase, criteria, running slices, DO/DO NOT |
| **shaping-output.md** | `shaping.output.interaction_tree`, `shaping.output.state_model` | Interaction Tree and State Model format |
| **shaping-validation.md** | `shaping.validation.checklist`, `shaping.validation.rules` | Validation checklist; DO/DON'T rules |
| **shaping-core.md** | `shaping.core.interaction`, `shaping.core.state_concept` | Interaction and State Concept definitions |
| **rules/** (markdown + JSON) | `shaping.validation.rules` | DO/DON'T rules, scanner configs; merged into RuleSet |

### 3.3 What to Inject and When

**Applies to:** Epic **Use Shape Skill** — Stories: Create Shaping Strategy, Generate Slices, Improve Strategy.

| Operation | Inject | Story |
|-----------|--------|-------|
| **create_strategy** | `shaping.process.intro`, `shaping.strategy.phase`, `shaping.strategy.criteria`, `shaping.core.interaction`, `shaping.core.state_concept` | Create Shaping Strategy |
| **generate_slice** | `shaping.process.intro`, `shaping.strategy.slices.running`, `shaping.strategy.corrections`, `shaping.output.*`, `shaping.validation.checklist`, `shaping.validation.rules`, `shaping.core.*`, **strategy doc** (from path) | Generate Shaping Slices |
| **improve_strategy** | `shaping.strategy.corrections`, `shaping.validation.checklist` (correction format only) | Improve Strategy |
| **improve_skill** | `shaping.process.post_shaping.review`, `shaping.strategy.corrections`, **strategy doc** (from path) | Improve Skill |

**Corrections in generate_slice:** When user feedback implies a reusable rule, AI adds DO/DO NOT during the slice flow; no separate `improve_strategy` call needed.

**Validation:** No separate validate operation. `generate_slice` injects both checklist and rules. AI validates against checklist before presenting; reports status (✓ pass or ⚠ needs attention) in response.

**Scanners:** Programmatic validators live in `rules/` as config. Flow: (1) Generate output. (2) Run scanners. (3) Determine false positives. (4) Inject problems, fixes, and report location into the next prompt. AI addresses real issues in the next iteration.

**Context (always available):** Context source paths, workspace path, strategy path (when exists). Caller provides these; not "injected" as instruction content.

### 3.4 Injection Flow

**Applies to:** Epic **Use Shape Skill** — Stories: Create Shaping Strategy, Generate Slices, Improve Strategy.

| Step | Caller | Engine / Skill |
|------|--------|----------------|
| 1 | User requests operation (e.g. create strategy, generate slice 1) | — |
| 2 | Asks skill for instructions: `skill.instructions.display_content("create_strategy")` | Skill assembles from `operation_sections` + engine context |
| 3 | Injects assembled markdown + context paths into AI prompt | — |
| 4 | AI runs operation; instructions already in prompt | — |

**When:** Before the AI runs the operation. Caller injects; AI receives — doesn't have to "load" guidelines.

### 3.5 Object Model (AceSkill, Instructions)

**Applies to:** Epic **Initialize Agile Context Engine** (Load skills — inject Engine into each AceSkill); Epic **Create Ace-Skill** (AceSkill structure).

| Concept | Implementation |
|---------|----------------|
| **Engine injection** | AceSkill receives `Engine` at construction. Uses engine for workspace, strategy_path, slice_index. |
| **operation_sections** | Map: operation → section IDs. Keys: `create_strategy`, `generate_slice`, `improve_strategy`, `improve_skill`. From skill config. |
| **instructions** | Property. Assembles from `operation_sections` and engine context. No context parameter — pulls from engine. |
| **display_content(operation)** | Returns markdown for that operation. Caller injects into prompt. |

` — context comes from engine.

---

**══════════════════════════════════════════════════════════════**  
**TENTATIVE — To Be Detailed Later**  
**══════════════════════════════════════════════════════════════**

Everything below is placeholder. We will go into more detail on Create Ace-Skill first.

---

## 8. Epic: Gather Context

### Story: Gather context for shaping run

| Aspect | Implementation |
|--------|----------------|
| **Populate memory** | Invoke ace-context-to-memory: convert → chunk → sync to `<workspace>/context-to-memory/memory/`. |
| **Memory layout** | Each source file → one folder under `memory/`; folder = one `Memory`; chunks as `.md` files with `<!-- Source: path -->`. |
| **ContextSources** | `src/context_sources.py` — `class ContextSources` with `gather(content_sources, workspace, strategy)`. |
| **Memories** | `src/memories.py` — `Memories`, `Memory`, `Chunk`. |
| **Refer** | `Memories.refer()` returns `Chunk[]` for shaping. |

**Memory path:** `<skill_space>/context-to-memory/memory/<artifact_id>/`  
**Chunk files:** `chunk_001.md`, `chunk_002.md`, … with source attribution in each.

---

## 9. Epic: Use Shape Skill

### Story: Create Shaping Strategy

| Aspect | Implementation |
|--------|----------------|
| **Output path** | `<skill_space>/shaping/strategy.md` |
| **Format** | Markdown. Structure: source analysis, epic breakdown, slice order, assumptions. |
| **Strategy** | `src/strategy.py` — `class Strategy` with `save(path)`, `load(path)`, `update(rules)`. |
| **Metadata (optional)** | `<skill_space>/shaping/strategy.json` for structured parts (epics, slices) if needed. |

### Story: Generate Shaping Slices

| Aspect | Implementation |
|--------|----------------|
| **Output** | Interaction Tree + State Model. |
| **Paths** | `<skill_space>/shaping/slice-<n>/interaction-tree.md`, `slice-<n>/state-model.md` (or `.json` for structured). |
| **Slice** | `src/slice.py` — `class Slice` with `produce(strategy): (InteractionTree, StateModel)`. |

### Story: Improve Shaping Skill

| Aspect | Implementation |
|--------|----------------|
| **Update** | `Strategy.update(rules)` appends DO/DO NOT rules; persists to same strategy path. |
| **Re-run** | Regenerate slice with updated strategy. |

---

## 10. Skill Space Output Layout (Tentative)

```
<skill_space>/
├── shaping/
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
| AgileContextEngine | `src/engine.py` | `AgileContextEngine` |
| SkillSpace | `src/skill_space.py` | `SkillSpace` |
| AceSkill | `src/ace_skill.py` | `AceSkill` |
| RuleSet | `src/rule_set.py` | `RuleSet` |
| ContextSources | `src/context_sources.py` | `ContextSources` |
| Memories | `src/memories.py` | `Memories` |
| Memory | `src/memories.py` | `Memory` |
| Chunk | `src/memories.py` | `Chunk` |
| Strategy | `src/strategy.py` | `Strategy` |
| Slice | `src/slice.py` | `Slice` |
| BuildScript | `src/build_script.py` | `BuildScript` |
| AssembledAgent | `src/assembled_agent.py` | `AssembledAgent` |

---

## 12. Pydantic Models (Tentative)

```python
# conf/ace_config.py or src/config.py
from pydantic import BaseModel
from pathlib import Path

class AceConfig(BaseModel):
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
| Engine config | JSON | `agile-context-engine/conf/ace-config.json` |
| Skill content | Markdown | `skills/ace-<name>/content/*.md` (includes script-invocation.md for AI) |
| Scanner rules | JSON | `skills/ace-<name>/rules/*.json` |
| Assembled agent | Markdown | `skills/ace-<name>/AGENTS.md` |
| Strategy | Markdown | `<skill_space>/shaping/strategy.md` |
| Memory chunks | Markdown | `<skill_space>/context-to-memory/memory/<id>/*.md` |
| Slice output | Markdown / JSON | `<skill_space>/shaping/slice-<n>/*.md` |
