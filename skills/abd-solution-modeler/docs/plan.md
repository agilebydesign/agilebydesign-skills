# Plan: Create abd-solution-modeler Skill

Transform raw context into a **validated OO domain model** and **interaction tree**. Pipeline: Guidance → Sketch → Refine. Process is **code-driven** — scripts orchestrate phases; AI produces output when a phase invokes it.

**Full spec:** See [requirements.md](requirements.md) for phases, formats, outputs, and checkpoints.

---

## Dependencies

**abd-context-to-memory** (existing skill) — Use for context preparation. Refer to it; do not recreate.

- Chunk source documents: `index_memory.py` or `index_chunks.py`
- Output: `chunk_index.json` (required for evidence extraction)
- Path: `skills/abd-context-to-memory`

---

## Skill Structure

```
abd-solution-modeler/
├── SKILL.md
├── AGENTS.md
├── conf/
│   └── abd-config.json
├── pieces/
│   ├── process.md          # Orchestration; refers to phase specs
│   ├── domain.md           # Minimal — Module, Concept format (per requirements.md)
│   ├── interaction_tree.md # Minimal — Epic→Story→Scenario→Step (per requirements.md)
│   ├── phases/   # normalize_context.md … validated_domain_model.md (see requirements.md)
├── scripts/
│   ├── pipeline.py         # Orchestrator: run phase N, get_instructions for AI phases
│   ├── extract_*.py        # Evidence extraction (per requirements.md)
│   └── ...
└── docs/
    ├── requirements.md     # Full spec (phases, formats, outputs)
    └── plan.md            # This plan
```

---

## Process (Code-Driven)

**process.md** — References phase specs (e.g. normalize_context.md) per phase.

- Each phase: Human → Script runs → AI produces (when phase is AI) → Human reviews
- **Process is code** — `pipeline.py run <phase>` or `pipeline.py pipeline` runs phases in order
- **No prompt injection** — Phase files contain instructions; scripts invoke them; AI reads phase file and produces output
- Stop for review at checkpoints (see requirements.md)

**Pipeline sections:**

1. **Context** (Phases 1–5) — Prepare context, extract evidence, build graph, concept guidance
2. **Model** (Phases 6–11) — Interaction tree structure → domain model progression (Concept → Structural → Behavior → Variation → Refined)
3. **Validate** (Phases 12–13) — Scenario walkthrough, add Examples

---

## Pieces (Minimal)

**domain.md** — Only: Module format, Domain Concept format, guidelines. Full format in [requirements.md](requirements.md) § Core Modeling Formats.

**interaction_tree.md** — Only: Hierarchy (Epic→Story→Scenario→Step), Trigger/Response/Pre-Condition, domain grounding (`**Concept**`), inheritance. Progression table in [requirements.md](requirements.md) § Interaction Tree Model.

**Phase specs** (e.g. normalize_context.md, concept_guidance_v1.md) — Per-phase: Inputs, Outputs, Instructions (for AI phases), What to run (for code phases). Content from [requirements.md](requirements.md) § Phase N.

---

## Scripts

**pipeline.py** — Orchestrator.

- `pipeline.py run 1` — Run Phase 1 (code)
- `pipeline.py run 2` — Run Phase 2 (AI: load concept_guidance_v1.md, produce output)
- `pipeline.py pipeline` — Run phases 1–N in sequence

**Evidence extraction** — Outputs per [requirements.md](requirements.md) § Phase 3, Phase 4.

**Context** — Use abd-context-to-memory. Scripts call `index_memory.py` or `index_chunks.py` from that skill (or document path for user to run).

---

## Phase Summary

| Phase | Actor | Outputs (see requirements.md for full detail) |
| ----- | ----- | -------------------------------------------- |
| 1 | Code | rule_chunks.json |
| 2 | AI | domain_concept_guidance_v1.md, interaction_tree (epic skeleton) |
| 3 | Code | terms.json, actions.json, decisions.json, states.json, relationships.json, modifiers.json |
| 4 | Code | evidence_graph.json |
| 5 | AI | domain_concept_guidance_v2.md, interaction_tree (epics, sub-epics, story names) |
| 6 | AI | interaction_tree (structure refined) |
| 7 | AI | concept_model.md |
| 8 | AI | structural_model.md |
| 9 | AI | behavior_model.md |
| 10 | AI | variation_model.md |
| 11 | AI | refined_domain_model.md, interaction_tree (scenarios, Failure-Modes) |
| 12 | AI+Human | scenario_walkthroughs.md |
| 13 | AI | validated_domain_model.md, interaction_tree (with Examples) |

---

## Implementation Order

1. Create skill scaffold (SKILL.md, AGENTS.md, conf/, pieces/, scripts/)
2. Create process.md (references phase specs)
3. Create domain.md, interaction_tree.md (minimal; spec in requirements.md)
4. Create phase specs (normalize_context.md … validated_domain_model.md from requirements.md)
5. Implement pipeline.py (run phase, orchestrate)
6. Implement evidence extraction scripts
7. Wire abd-context-to-memory (document or script invocation)

---

## abd-context-to-memory Wiring

**When to run:** Before Phase 1 if source is documents (PDF, PPTX, DOCX, etc.).

**Steps:**

1. Link workspace source (if needed):
   ```bash
   python skills/abd-context-to-memory/scripts/link_workspace_source.py --path <folder>
   ```

2. Convert and chunk (or full pipeline with RAG):
   ```bash
   python skills/abd-context-to-memory/scripts/index_memory.py --path <source_folder>
   ```

3. Output: abd-context-to-memory writes `chunk_index.json` to its default location. For abd-solution-modeler, set `chunk_index_path` or `context_path` in `conf/abd-config.json` to point to the chunk index or markdown folder. All pipeline output goes to `solution_workspace/output_dir` (e.g. `mm3/solution/`).

**Alternative:** If context is already markdown in a folder, Phase 1 (normalize) can read directly from that folder — no abd-context-to-memory required. The plan assumes rule_chunks.json format; adapt Phase 1 script to accept either chunk_index.json (from memory skill) or raw markdown files.
