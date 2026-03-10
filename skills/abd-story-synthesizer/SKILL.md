---
name: abd-story-synthesizer
description: Shape source material into an Interaction Tree and State Model (story map and domain model). Use when synthesizing requirements, deriving epics and stories from source documents, or building a hierarchical structure of actor exchanges and domain concepts.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Story Synthesizer

Shape source material into an **Interaction Tree** and **State Model** — a story map and domain model. Contains rules across Context, Interaction Inheritance, Interaction Hierarchy, and Domain & Interaction categories to guide synthesis of requirements into epics, sub-epics, and stories with associated state concepts. See `rules/README.md` for tag set and filtering; `pieces/session.md` for session types and scope.

## Config Location (IMPORTANT)

**Two config files — each owns different concerns.**

| Location | Contains | Owns |
|----------|----------|------|
| `abd-story-synthesizer/conf/abd-config.json` | Engine config: `skills`, `skills_config`, `skill_space_path` | Which skill space to target |
| `<skill-space>/conf/abd-config.json` (e.g. `mm3e/conf/abd-config.json`) | Skill space config: `context_paths` | Where context lives in this workspace |

The synthesizer skill points to the skill space via `skill_space_path`. The skill space owns its own context — the engine reads `context_paths` from the skill space's config. Run `discover_context` to auto-populate `context_paths` in the skill space's config.

## Source Folder Structure

`abd_content/source/` contains content sources. Workspace RFQ folders are linked in for skill access:

- `source/JBOM Agile Support` — Junction to `workspace/Scotia Talent Journey Based Operating Model/source` (RFQ docs, B&T, Supplier Q&A, etc.)

Use this path when synthesizing from RFQ or JBOM source material.

## When to Apply

Reference these guidelines when:
- Shaping requirements from source documents into a story map
- Deriving epics and stories from user journeys or business flows
- Building an Interaction Tree (hierarchical actor exchanges)
- Modeling domain state concepts (State Model)
- Defining story granularity and slice order

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Context & Scope | HIGH | `context-` |
| 2 | Interaction Inheritance | HIGH | `interaction-inheritance-` |
| 3 | Interaction Hierarchy | HIGH | `interaction-` |
| 4 | Domain & Interaction | HIGH | `domain-`, `interaction-` |
| 5 | Shape & Naming | HIGH | (from story_bot shape) |

## Quick Reference

### 1. Context & Scope (HIGH)

- `context-derive-from-source` — Derive concepts from interactions in the context; do not invent workflows
- `context-speculation-assumptions` — State assumptions when unclear; do not speculate or invent

### 2. Interaction Inheritance (HIGH)

- `interaction-inheritance-pre-condition` — Shared Pre-Condition on parent only; comprehensive preconditions
- `interaction-inheritance-domain-concepts` — Scope concepts to Epic/Story that owns them
- `interaction-inheritance-resulting-state` — Same inheritance as Pre-Condition; outcome language only
- `interaction-inheritance-actors` — Use [User], [System] at every trigger/response
- `interaction-inheritance-examples` — Examples live on interaction; use [inherited] when from parent
- `interaction-inheritance-triggering-state` — Epic holds rules that apply to all children

### 3. Interaction Hierarchy (HIGH)

- `interaction-parent-granularity` — Keep parent nodes at appropriate granularity; do not leak child detail
- `interaction-sequential-order` — Order tree sequentially; required state creators before consumers
- `interaction-story-granularity` — Break down by distinct areas; sufficient stories for rule detail

### 4. Domain & Interaction (HIGH / MEDIUM-HIGH)

- `domain-synchronize-concepts` — Complete full workflow (interactions → concepts → Domain Model) for each slice
- `domain-logical-domain-level` — Keep at logical/domain level; no implementation details
- `interaction-failure-modes` — Max 3 per interaction; domain rules only
- `interaction-supporting-actor-response` — Supporting = system; Actor → System exchange

### 5. Shape & Naming (HIGH)

- `verb-noun-format` — Verb-noun for names, scenario steps, and AC; active voice; base verb forms; business language (merges active_business_and_behavioral_language and use_verb_noun_format_for_story_elements)
- `interaction-story-small-and-testable` — Story = testable outcome; step = implementation detail
- `interaction-outcome-oriented-language` — Outcomes over mechanisms; artifacts over "visualizing"
- `interaction-ensure-vertical-slices` — Vertical slices; end-to-end flows when slice design in scope

## How to Use

Read individual rule files for detailed DO/DO NOT guidance:

```
rules/context-derive-from-source.md
rules/verb-noun-format.md
rules/interaction-inheritance-pre-condition.md
```

Each rule file contains:
- Brief explanation
- DO with example
- DO NOT with example

## Full Compiled Document

For the complete guide with all rules, core definitions, output structure, validation, and synthesis process: `AGENTS.md`

## Build

To regenerate AGENTS.md from pieces:

```bash
cd skills/abd-story-synthesizer
python scripts/build.py
```

Run from the agilebydesign-skills root, or from within the abd-story-synthesizer skill directory.
