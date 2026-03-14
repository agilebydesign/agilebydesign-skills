---
name: abd-story-synthesizer
description: Build rich OO domain models from context using a 17-step evidence pipeline. Extracts structured evidence with scripts, then uses focused AI passes to discover mechanisms, assign decision ownership, and produce validated object models. Also produces Interaction Trees (story maps). Use when synthesizing requirements into domain models, deriving objects from source documents, or building story maps with domain concepts.
license: MIT
metadata:
  author: agilebydesign
  version: "2.1.0"
---

# Story Synthesizer

Build rich OO domain models from context using a **17-step evidence pipeline**. The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

The skill produces an **Interaction Tree** (story map) and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. The domain model is built through structured evidence extraction (CODE scripts) followed by focused AI modeling passes — never from raw text directly.

## Pipeline Overview

```
CODE: Normalize → Extract terms/actions/decisions/variations/states → Build evidence graph
AI:   Concept scan → Behavior packets → Mechanisms → Decision ownership →
      Object candidates → Relationships → Inheritance test →
      Scenario walkthrough → Anemia critique → Base/inheritance check → Final OO model
```

## Config Location

**Two config files — each owns different concerns.**

| Location | Contains | Owns |
|----------|----------|------|
| `abd-story-synthesizer/conf/abd-config.json` | Engine config: `skills`, `skills_config`, `skill_space_path` | Which skill space to target |
| `<skill-space>/conf/abd-config.json` | Skill space config: `context_paths` | Where context lives in this workspace |

## Rule Categories

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Context & Scope | HIGH | `context-` |
| 2 | Domain OOA | HIGH | `domain-ooa-` |
| 3 | Interaction Inheritance | HIGH | `interaction-inheritance-` |
| 4 | Interaction Hierarchy | HIGH | `interaction-` |
| 5 | Shape & Naming | HIGH | `verb-noun-`, `scaffold-` |

## CRITICAL: Process Order

**Overall Context phases must run in strict order.** Do NOT skip or reorder.

| Phase | Step | Command |
|-------|------|---------|
| 2 | Prepare Context | `index_memory.py --path <context_folder>` (NOT index_chunks when source docs need conversion) |
| 3 | Map Concepts | `build.py get_instructions concept_scan` → produce concept_scan.md |
| 4 | Extract Evidence | `build.py extract_evidence` |

**DO NOT run extract_evidence before concept_scan.** Phase 3 orients Phase 4. Check the checklist; complete Phase 3 before Phase 4.

**Phase 2:** Use `index_memory.py` when source has PDF/PPTX/DOCX — it converts, chunks, and indexes. Use `index_chunks.py` only when chunks already exist.

---

## Operations

| Operation | What it does | Type |
|-----------|-------------|------|
| `create_session` | **Create session strategy file on disk** — run when user says "start session". Does NOT run slice. | CODE |
| `concept_scan` | AI concept scan — discover primitives, mechanisms, authority boundaries | AI |
| `extract_evidence` | Run scripts 01–07 to extract and consolidate evidence | CODE |
| `model_discovery` | AI Pass A (steps 9–14): behavior packets through inheritance test | AI |
| `model_validation` | AI Pass B (steps 15–17): scenario walkthrough, anemia critique, base/inheritance check, final model | AI |
| `create_strategy` | Get instructions to refine strategy (use after create_session if AI needs to adjust) | AI |
| `run_slice` | Synthesize interaction tree for a slice — **only when user says "run slice", "build it", "proceed"** | AI |
| `validate` | Run scanners on output | CODE |
| `correct_run` / `correct_all` | Record and promote corrections | AI |

## Build

```bash
cd skills/abd-story-synthesizer
python scripts/build.py                              # rebuild AGENTS.md
python scripts/build.py create_session [name]        # create strategy file (Phase 5 — do NOT run slice)
python scripts/build.py get_instructions concept_scan # get AI concept scan instructions
python scripts/build.py extract_evidence              # run evidence extraction pipeline
python scripts/build.py get_instructions model_discovery  # get Pass A instructions
python scripts/build.py get_instructions model_validation # get Pass B instructions
python scripts/build.py get_instructions run_slice   # get run slice instructions (Phase 6 — only when user requests)
python scripts/build.py validate                      # run scanners
```
