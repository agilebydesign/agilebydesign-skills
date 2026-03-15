---
name: abd-solution-modeler
description: >-
  Transforms raw context into a validated OO domain model and interaction tree.
  Pipeline: Guidance → Sketch → Refine. Use when the user wants to "model domain",
  "build interaction tree", "extract domain from rules", or "solution model".
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# abd-solution-modeler

Transforms raw context (rules, requirements, documentation) into a **validated OO domain model** and **interaction tree**. Pipeline: Guidance → Sketch → Refine. Process is code-driven — scripts orchestrate phases; AI produces output when a phase invokes it.

## When to Activate

- User asks to "model domain", "build interaction tree", "extract domain from rules"
- Wants to "solution model" from rulebooks, specs, or documentation
- Has context and wants to produce validated OOAD model + interaction tree

## Dependencies

**abd-context-to-memory** — Use for context preparation (chunk, index). Run before Phase 1 if source is documents. See `docs/plan.md` for wiring.

## Spec and Plan

- **Full spec:** `docs/requirements.md` — phases, formats, outputs, checkpoints
- **Implementation plan:** `docs/plan.md` — skill structure, dependencies, implementation order

## Pipeline

1. **Context** (Phases 1–5) — Normalize, extract evidence, build graph, concept guidance
2. **Model** (Phases 6–11) — Interaction tree structure → domain model progression
3. **Validate** (Phases 12–13) — Scenario walkthrough, add Examples

## Scripts

Run from workspace root. Scripts in `skills/abd-solution-modeler/scripts/`.

- `pipeline.py run <phase>` — Run phase N (1–13)
- `pipeline.py pipeline` — Run phases 1–N in sequence
- `assemble_agents.py` — Assemble AGENTS.md from content pieces. Run after editing `pieces/*.md`.
