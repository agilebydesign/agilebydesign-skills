---
name: abd-story-synthesizer
description: Build rich OO domain models from context using a 17-step evidence pipeline. Extracts structured evidence with scripts, then uses focused AI passes to discover mechanisms, assign decision ownership, and produce validated object models. Also produces Interaction Trees (story maps). Use when synthesizing requirements into domain models, deriving objects from source documents, or building story maps with domain concepts.
license: MIT
metadata:
  author: agilebydesign
  version: "2.0.0"
---

# Story Synthesizer

Build rich OO domain models from context using a **17-step evidence pipeline**. The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

The skill produces an **Interaction Tree** (story map) and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. The domain model is built through structured evidence extraction (CODE scripts) followed by focused AI modeling passes — never from raw text directly.

## Pipeline Overview

```
CODE: Normalize → Extract terms/actions/decisions/variations/states → Build evidence graph
AI:   Concept scan → Behavior packets → Mechanisms → Decision ownership →
      Object candidates → Relationships → Inheritance test →
      Scenario walkthrough → Anemia critique → Final OO model
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

## Operations

| Operation | What it does | Type |
|-----------|-------------|------|
| `concept_scan` | AI concept scan — discover primitives, mechanisms, authority boundaries | AI |
| `extract_evidence` | Run scripts 01–07 to extract and consolidate evidence | CODE |
| `model_discovery` | AI Pass A (steps 9–14): behavior packets through inheritance test | AI |
| `model_validation` | AI Pass B (steps 15–17): scenario walkthrough, critique, final model | AI |
| `create_strategy` | Create session with strategy and slices | AI |
| `run_slice` | Synthesize interaction tree for a slice | AI |
| `validate` | Run scanners on output | CODE |
| `correct_run` / `correct_all` | Record and promote corrections | AI |

## Build

```bash
cd skills/abd-story-synthesizer
python scripts/build.py                              # rebuild AGENTS.md
python scripts/build.py get_instructions concept_scan # get AI concept scan instructions
python scripts/build.py extract_evidence              # run evidence extraction pipeline
python scripts/build.py get_instructions model_discovery  # get Pass A instructions
python scripts/build.py get_instructions model_validation # get Pass B instructions
python scripts/build.py validate                      # run scanners
```
