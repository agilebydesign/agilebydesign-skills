# Phase 1 — Normalize Context

**Actor:** Code | **Full spec:** [requirements.md](../../docs/requirements.md) § Phase 1

## Purpose

Prepare raw materials for reasoning.

## Trigger

normalize context, chunk context, prepare context, convert context to memory

## Inputs

- rulebooks, specs, documentation, code (optional)

## Instructions

- split into logical chunks
- assign stable IDs
- preserve source location
- do not interpret text

## Outputs

`rule_chunks.json`

## Run

```bash
python scripts/pipeline.py run 1
```

Script: `scripts/normalize_context.py`
