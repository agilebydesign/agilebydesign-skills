---
name: abd-story-synthesizer
description: Shape source material into an Interaction Tree and State Model (story map and domain model). Use when shaping requirements, deriving epics and stories from source documents, or building a hierarchical structure of actor exchanges and domain concepts.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Story Synthesizer

Shape source material into an **Interaction Tree** and **State Model** — a story map and domain model. Contains rules across Context, Interactions Inheritance, Hierarchy, and State & Interaction categories to guide shaping of requirements into epics, sub-epics, and stories with associated state concepts. See `content/rules-tagging-proposal.md` for tagging by strategy component.

## Source Folder Structure

`abd_content/source/` contains content sources. Workspace RFQ folders are linked in for skill access:

- `source/JBOM Agile Support` — Junction to `workspace/Scotia Talent Journey Based Operating Model/source` (RFQ docs, B&T, Supplier Q&A, etc.)

Use this path when shaping from RFQ or JBOM source material.

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
| 2 | Interactions Inheritance | HIGH | `interactions-inheritance-` |
| 3 | Hierarchy | HIGH | `hierarchy-` |
| 4 | State & Interaction | HIGH | `state-`, `interaction-` |
| 5 | Shape & Naming | HIGH | (from story_bot shape) |

## Quick Reference

### 1. Context & Scope (HIGH)

- `context-derive-from-source` — Derive concepts from interactions in the context; do not invent workflows
- `context-speculation-assumptions` — State assumptions when unclear; do not speculate or invent

### 2. Interactions Inheritance (HIGH)

- `interactions-inheritance-pre-condition` — Shared Pre-Condition on parent only; comprehensive preconditions
- `interactions-inheritance-domain-concepts` — Scope concepts to Epic/Story that owns them
- `interactions-inheritance-resulting-state` — Same inheritance as Pre-Condition; outcome language only
- `interactions-inheritance-actors` — Use [User], [System] at every initiation/response
- `interactions-inheritance-examples` — Examples live on interaction; use [inherited] when from parent
- `interactions-inheritance-initiating-state` — Epic holds rules that apply to all children

### 3. Hierarchy (HIGH)

- `hierarchy-parent-granularity` — Keep parent nodes at appropriate granularity; do not leak child detail
- `hierarchy-sequential-order` — Order tree sequentially; required state creators before consumers
- `hierarchy-story-granularity` — Break down by distinct areas; sufficient stories for rule detail

### 4. State & Interaction (HIGH / MEDIUM-HIGH)

- `state-synchronize-concepts` — Complete full workflow (interactions → concepts → State Model) for each slice
- `state-logical-domain-level` — Keep at logical/domain level; no implementation details
- `interaction-failure-modes` — Max 3 per interaction; domain rules only
- `interaction-supporting-actor-response` — Supporting = system; Actor → System exchange

### 5. Shape & Naming (HIGH)

- `verb-noun-format` — Verb-noun for names, scenario steps, and AC; active voice; base verb forms; business language (merges active_business_and_behavioral_language and use_verb_noun_format_for_story_elements)
- `small-and-testable` — Story = testable outcome; step = implementation detail
- `outcome-oriented-language` — Outcomes over mechanisms; artifacts over "visualizing"
- `ensure-vertical-slices` — Vertical slices; end-to-end flows when slice design in scope

## How to Use

Read individual rule files for detailed DO/DO NOT guidance:

```
rules/context-derive-from-source.md
rules/verb-noun-format.md
rules/interactions-inheritance-pre-condition.md
```

Each rule file contains:
- Brief explanation
- DO with example
- DO NOT with example

## Full Compiled Document

For the complete guide with all rules, core definitions, output structure, validation, and shaping process: `AGENTS.md`

## Build

To regenerate AGENTS.md from content:

```bash
cd skills/abd-story-synthesizer
python scripts/build.py
```

Run from the agilebydesign-skills root, or from within the abd-story-synthesizer skill directory.
