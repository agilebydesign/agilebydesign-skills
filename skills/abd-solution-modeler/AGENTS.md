# abd-solution-modeler

Transforms raw context into a validated OO domain model and interaction tree. Pipeline: Guidance → Sketch → Refine.

## Spec

**Full spec:** `docs/requirements.md` — phases, formats, outputs, checkpoints.

**Plan:** `docs/plan.md` — skill structure, dependencies, implementation order.

---

# Process

Pipeline: Guidance → Sketch → Refine. Process is **code-driven** — `pipeline.py` orchestrates phases. AI phases load phase spec (e.g. `concept_guidance_v1.md`) and produce output.

**Match user phrase to phase Trigger** — each phase file has a `## Trigger` section; run that phase when the user says one of those phrases.

**Full spec:** `docs/requirements.md`

---

## Stage 1: Context (Phases 1–5)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 1 | Code | [normalize_context.md](pieces/phases/normalize_context.md) | rule_chunks.json |
| 2 | AI | [concept_guidance_v1.md](pieces/phases/concept_guidance_v1.md) | domain_concept_guidance_v1.md, interaction_tree (epic skeleton) |
| — | **Checkpoint 1** | Verify domain framing: concepts, modules, mechanisms, actors, epics | — |
| 3 | Code | [evidence_extraction.md](pieces/phases/evidence_extraction.md) | terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json |
| 4 | Code | [evidence_graph.md](pieces/phases/evidence_graph.md) | evidence_graph.json |
| — | **Checkpoint 2** | Verify rule coverage: evidence graph covers rules | — |
| 5 | AI | [concept_guidance_v2.md](pieces/phases/concept_guidance_v2.md) | domain_concept_guidance_v2.md, interaction_tree (epics, sub-epics, story names) |

---

## Stage 2: Model (Phases 6–11)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 6 | AI | [interaction_tree_structure.md](pieces/phases/interaction_tree_structure.md) | interaction_tree (structure refined) |
| — | **Checkpoint 3** | Verify structure: epic/sub-epic/story placement | — |
| 7 | AI | [concept_model.md](pieces/phases/concept_model.md) | concept_model.md |
| 8 | AI | [structural_model.md](pieces/phases/structural_model.md) | structural_model.md |
| 9 | AI | [behavior_model.md](pieces/phases/behavior_model.md) | behavior_model.md |
| — | **Checkpoint 4** | Verify ownership correctness: who owns what operations | — |
| 10 | AI | [variation_model.md](pieces/phases/variation_model.md) | variation_model.md |
| 11 | AI | [refined_domain_model.md](pieces/phases/refined_domain_model.md) | refined_domain_model.md, interaction_tree (scenarios, Failure-Modes) |
| — | **Checkpoint 5** | Verify structural validation: modules, boundaries | — |

---

## Stage 3: Validate (Phases 12–13)

| Phase | Actor | Ref | Outputs |
| ----- | ----- | --- | ------- |
| 12 | AI+Human | [scenario_walkthrough.md](pieces/phases/scenario_walkthrough.md) | scenario_walkthroughs.md |
| — | **Checkpoint 6** | Verify behavioral validation: walkthroughs | — |
| 13 | AI | [validated_domain_model.md](pieces/phases/validated_domain_model.md) | validated_domain_model.md, interaction_tree (with Examples) |

---

## Invocation

```bash
python scripts/pipeline.py run <phase>   # Run single phase
python scripts/pipeline.py pipeline      # Run phases 1–N
```

---

## Output Formats

- **Domain Model:** `pieces/domain.md` — Module, Concept format
- **Interaction Tree:** `pieces/interaction_tree.md` — Epic→Story→Scenario→Step (see requirements.md)

---

## Context Preparation

Use **abd-context-to-memory** before Phase 1 if source is documents:

- `index_memory.py --path <source_folder>` — convert, chunk, embed
- Output: `chunk_index.json` (required for evidence extraction)
- Path: `skills/abd-context-to-memory`

**Config:** Set `chunk_index_path` or `context_path` in `conf/abd-config.json`. Or pass `--chunk-index PATH` / `--context-path PATH` when running the pipeline.

---

## Scripts

```bash
python scripts/pipeline.py run <phase>   # Run phase 1–13
python scripts/pipeline.py pipeline     # Run phases 1–N (use --stop N to stop early)
```

**Assemble AGENTS.md from pieces:**

```bash
python scripts/assemble_agents.py
```

