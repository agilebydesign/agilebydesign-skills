# Phase 4 — Evidence Graph

**Actor:** Code | **Full spec:** [requirements.md](../../docs/requirements.md) § Phase 4

## Purpose

Build rule dependency structure.

## Trigger

build evidence graph, evidence graph, rule dependency

## Inputs

Extraction outputs (terms, actions, decisions, states, relationships, modifiers)

## Instructions

Create graph relations:

```
Concept → performs → Action
Action → produces → State
Concept → modifies → Concept
```

## Outputs

`evidence_graph.json`

## Run

```bash
python scripts/pipeline.py run 4
```

Script: `scripts/evidence_graph.py`

## Checkpoint 2

Human validates rule coverage before proceeding.
