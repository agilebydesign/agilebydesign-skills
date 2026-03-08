---
name: abd-shaping
description: Shape source material into an Interaction Tree and State Model (story map and domain model). Use when shaping requirements, deriving epics and stories from source documents, or building a hierarchical structure of actor exchanges and domain concepts.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
---

# Ace-Shaping

Shape source material into an **Interaction Tree** and **State Model** — a story map and domain model. Contains 11 rules across 4 categories to guide shaping of requirements into epics, sub-epics, and stories with associated state concepts.

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
| 1 | Source & Scope | HIGH | `source-` |
| 2 | Hierarchy | HIGH | `hierarchy-` |
| 3 | State & Structure | HIGH | `state-` |
| 4 | Interaction | MEDIUM-HIGH | `interaction-` |

## Quick Reference

### 1. Source & Scope (HIGH)

- `source-derive-from-source` — Derive concepts from interactions in the source; do not invent workflows
- `source-logical-domain-level` — Keep at logical/domain level; no implementation details
- `source-speculation-assumptions` — State assumptions when unclear; do not speculate or invent

### 2. Hierarchy (HIGH)

- `hierarchy-parent-granularity` — Keep parent nodes at appropriate granularity; do not leak child detail
- `hierarchy-sequential-order` — Order tree sequentially; required state creators before consumers

### 3. State & Structure (HIGH)

- `state-required-state` — Shared state on parent only; comprehensive preconditions
- `state-resulting-state` — Same inheritance as required state; outcome language only
- `state-failure-modes` — Max 3 per interaction; domain rules only
- `state-concept-scoping` — Scope concepts to Epic/Story that owns them
- `state-structured-concepts` — Complete full workflow (interactions → concepts → State Model) for each slice

### 4. Interaction (MEDIUM-HIGH)

- `interaction-supporting-actor-response` — Supporting = system; Actor → System exchange
- `interaction-story-granularity` — Break down by distinct areas; sufficient stories for rule detail

## How to Use

Read individual rule files for detailed DO/DO NOT guidance:

```
rules/source-derive-from-source.md
rules/state-required-state.md
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
cd skills/abd-shaping
python scripts/build.py
```

Run from the agilebydesign-skills root, or from within the abd-shaping skill directory.
