# Process Overview

Your task is to build an **Interaction Tree** and **Domain Model** using a pipeline that separates mechanical evidence extraction (CODE) from analytical reasoning (AI).

The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

**Stop for review (default):** After each phase that produces human-reviewable output (concept scan, evidence summary, foundational model, etc.), **STOP and ask the user to review.** Present the output, then **pose questions** for the user to consider (e.g., completeness, gaps, overlaps, scope, authority). Do not proceed to the next phase until the user explicitly says to continue (e.g., "proceed", "continue", "looks good", "next phase"). The user must override the default by confirming before the AI moves on.

---

## The Pipeline (3 Sections)

**Each stage has its own independent checklist.** Kick off the checklist when you start that stage.

```text
1. OVERALL CONTEXT
   Checklist: overall_context_checklist_template.md → overall-context-checklist.md
   - Phase 1: Set Skill Space
   - Phase 2: Prepare Context
   - Phase 3: Extract Evidence
   - Phase 4: Map Concepts
   - Phase 5: Model Discovery and Assessment (on entire concept map and evidence)
   Outputs: chunk_index.json, evidence graph, concept_scan, foundational-model.md

2. SESSION
   Checklist: session_checklist_template.md → <session>/session-checklist.md
   - Phase 6: Create Session
   Outputs: <session>-strategy.md
   **Before starting:** Go to Overall Context and complete anything not done (chunk index, evidence graph, concept scan, OOAD foundation).
   **STOP HERE. Do NOT run slices until user says "run slice", "build it", or "proceed"**

3. SLICE-RUNS
   Checklist: run_checklist_template.md → <session>/runs/run-N-checklist.md (per slice run)
   - Phase 7: Model Generation (builds on foundation)
   - Phase 8: Validate Rules and Scanners
   - Phase 9: Render Diagrams
   - Phase 10: Make Corrections

  At any time during session and slice-run a user may
    - Improve Strategy from Corrections
    - Improve Skill from Corrections
```

---

# 1. Overall Context

Everything that prepares the workspace before any session. Run once per workspace (or when context changes).

**Kick off checklist:** Run `python scripts/create-checklist.py overall` when starting this stage. This checklist is independent of Session and Slice-Runs.

**CRITICAL:** Create checklist when starting: `create-checklist [overall|session|run]`. Update when step completes: `create-checklist update <path> --step N` or edit the file. A change is not tracked until the checklist is updated.

---

## Phase 1: Set Skill Space


| Human                                          | AI / Script                                 | AI                              | Human → AI                    |
| ---------------------------------------------- | ------------------------------------------- | ------------------------------- | ----------------------------- |
| Says "set skill space to X" or "new workspace" | Runs `build.py get_config`, validates paths | Reports paths; checks readiness | Confirms or provides new path |


Configure the skill space path in `abd-story-synthesizer/conf/abd-config.json` and the context paths in `<skill-space>/conf/abd-config.json`.

```bash
python scripts/build.py get_config
```

---

## Phase 2: Prepare Context


| Human                                          | AI / Script                      | AI                                | Human → AI       |
| ---------------------------------------------- | -------------------------------- | --------------------------------- | ---------------- |
| Says "prepare context" or provides source docs | Chunks documents, indexes chunks | Reports chunk count and readiness | Confirms sources |


Chunk source documents and build chunk index using the `abd-context-to-memory` skill. **Chunk index creation is mandatory** — run `index_memory.py` or `index_chunks.py` from that skill.

**DO NOT use `index_chunks.py` when source has PDF/PPTX/DOCX.** Use `index_memory.py` — it converts, chunks, and indexes. `index_chunks.py` only indexes existing chunks; it does not create them.

```bash
# From abd-context-to-memory skill:
python index_memory.py --path <context_folder>
# or, when chunks already exist:
python index_chunks.py --context-path <chunk_folder> [--output <path>]
```

Output: `<workspace>/story-synthesizer/context/chunk_index.json`

---

## Phase 3: Extract Evidence


| Human                   | AI / Script                              | AI                                   | Human → AI      |
| ----------------------- | ---------------------------------------- | ------------------------------------ | --------------- |
| Says "extract evidence" | Runs extraction pipeline (scripts 02–07) | Reports evidence counts and hotspots | Reviews summary |


Run the evidence extraction pipeline. Scripts extract structured evidence from normalized chunks — terms, actions, decisions, variations, states, relationships — then consolidate into an evidence graph.

```bash
python scripts/build.py extract_evidence
```

Requires `chunk_index.json` from abd-context-to-memory. Runs scripts 02–07 in sequence:

- `02_extract_terms.py` — noun phrases, vocabulary index
- `03_extract_actions.py` — subject-verb-object behavioral facts
- `04_extract_decisions.py` — conditional logic and rules
- `05_extract_variations.py` — behavior axes and mode differences
- `06_extract_states.py` — stateful entities and explicit relationships
- `07_consolidate_evidence.py` — build evidence graph with links, clusters, hotspots

Output: `evidence_graph.json` and `evidence_summary.md` in `<workspace>/story-synthesizer/evidence/`. See `pieces/evidence.md` for full specification.

---

## Phase 4: Map Concepts


| Human                                 | AI / Script                             | AI                      | Human → AI          |
| ------------------------------------- | --------------------------------------- | ----------------------- | ------------------- |
| Says "map concepts" or "concept scan" | Invokes `get_instructions concept_scan` | Produces conceptual map | Reviews and adjusts |


AI concept scan on normalized context. Discovers core primitives, interaction phases, authority boundaries, variation axes, rule mechanisms, and implicit concepts. Orients later AI passes (model discovery, validation).

```bash
python scripts/build.py get_instructions concept_scan
```

Output: `<workspace>/story-synthesizer/concept_scan.md`. See `pieces/concept_scan.md` for full specification.

**STOP for review.** Present the concept scan to the user and pose questions (e.g., completeness, overlaps, scope, authority, variation axes). Do not proceed to Phase 5 until the user confirms (e.g., "proceed", "continue", "looks good").

---

## Phase 5: Model Discovery and Assessment


| Human                                 | AI / Script                                      | AI                                                       | Human → AI          |
| ------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- | ------------------- |
| Says "model discovery" or "OOAD"      | Invokes `model_discovery` and `model_validation` | Produces OOAD analysis and validated domain model foundation | Reviews and adjusts |


**Runs on the entire concept map and evidence** — not per slice. Produces a foundational domain model that slice runs build on. Do this once per workspace (or when context changes).

### Model Discovery (OOAD)

**Behavior packet adequacy:** Packets must specify enough structure to build the model — concepts, flow (who creates what, who receives), and any mapping/composition rules the domain needs. Do not use a minimal one-liner.

1. **Behavior packet detection** — cluster evidence into coherent mechanisms
2. **Mechanism synthesis** — find real structural seams from packets
3. **Decision ownership** — assign each decision to the concept that should own it
4. **Object candidate formation** — derive candidates from owned behavior and state
5. **Relationship & boundary modeling** — define relationships based on behavior
6. **Inheritance test** — verify substitutability and shared protocol; propose base when concepts share acquisition/validation protocol

```bash
python scripts/build.py get_instructions model_discovery
```

**Persist the OOAD analysis** to `<workspace>/story-synthesizer/foundational-model.md`.

### Model Assessment (Validation)

**Verify behavior packets are adequate.** If packets are minimal, reject and redo discovery. **Persist the full assessment** to foundational-model.md. A one-line note is insufficient.

1. **Scenario / message walkthrough** — verify the model can actually behave
2. **Anemia / centralization critique** — find data bags, fake inheritance, misplaced behavior
3. **Base and inheritance check** — find concepts that share protocol and should extend a common base
4. **Final domain model foundation** — produce only after passes stabilize

```bash
python scripts/build.py get_instructions model_validation
```

Output: `<workspace>/story-synthesizer/foundational-model.md`. Slice runs extend this foundation and produce domain-model.md.

---

# 2. Session

Create and configure a session. One session per analysis focus (discovery / exploration / specification). Defines level of detail, scope, and slices. **Do not run any slice here.**

**Kick off checklist:** Run `python scripts/create-checklist.py session <name>` when starting this stage. This checklist is independent of Overall Context and Slice-Runs.

---

## Phase 6: Create Session


| Human                                    | AI / Script           | AI                            | Human → AI          |
| ---------------------------------------- | --------------------- | ----------------------------- | ------------------- |
| Says "start session" or "create session" | Runs `create_session` | Strategy file created on disk | Updates and adjusts |


Create, open, or continue an existing session. The session defines: Level of Detail (discovery/exploration/specification), Scope, and Slices. The evidence graph, concept scan, and OOAD foundation are already available.

**CRITICAL: Phase 6 creates the strategy file only. Do NOT run any slice.** The user must explicitly say "run slice", "build it", or "proceed" before Phase 7 (Model Generation).

**After creating strategy:** Run `get_instructions validate_session --strategy <path>` and validate slices against slice rules before running any slice.

**When user says "validate session" or "validate the session":** Run `get_instructions validate_session --strategy <path>` (path = session's strategy file, e.g. `discovery1/discovery1-strategy.md`). Apply those instructions: load rules, validate slices against slice rules. Report pass/fail and any violations. Do NOT run `build.py validate` (scanners).

**When the user corrects strategy, slices, or scope during session creation:** Apply the fix and record the correction in `runs/run-0.md`. See `pieces/runs.md` § When User Gives a Correction. A change is not complete until the correction is recorded.

See `pieces/session.md` for session content, slice design, and tag definitions.

```bash
python scripts/build.py create_session [session_name]
```

Output: `<workspace>/story-synthesizer/<session-name>/<session-name>-strategy.md`

---

# 3. Slice-Runs

Execute one run per slice. Phases 7–10: Model Generation → Validate Rules and Scanners → Render Diagrams → Make Corrections. Each slice run builds on the OOAD foundation from Stage 1. At any time: Improve Strategy or Improve Skill from corrections.

**Kick off checklist:** Run `python scripts/create-checklist.py run <session> <n>` at the start of each slice run. This checklist is independent per run.

---

## Phase 7: Model Generation


| Human                         | AI / Script                          | AI                                                 | Human → AI          |
| ----------------------------- | ------------------------------------ | -------------------------------------------------- | ------------------- |
| Says "run slice", "build it", "proceed" | Invokes `get_instructions run_slice` | Produces interaction tree + domain model for slice | Reviews and adjusts |


**Builds on the OOAD foundation** from Stage 1 (Phase 5). The foundation (foundational-model.md) provides mechanisms, ownership, and validated concepts. Slice runs produce the interaction tree and domain model (domain-model.md) for that slice's scope.

Produce the interaction tree and domain model for the slice. Domain concepts from the foundation sync into the interaction tree via `**Concept**` references.

```bash
python scripts/build.py get_instructions run_slice
```

---

## Phase 8: Validate Rules


| Human         | AI / Script                              | AI                 | Human → AI                   |
| ------------- | ---------------------------------------- | ------------------ | ---------------------------- |
| After Phase 7 | Invokes `get_instructions validate_slice` | Loads rules, validates | Fixes and re-runs until pass |
| Says "validate slice" | Invokes `get_instructions validate_slice` | Loads rules, validates slice output | Reports violations |


**When user says "validate slice" or "validate the slice":** Run `get_instructions validate_slice`. Apply those instructions: load rules, validate interaction-tree and domain-model against rules. Report pass/fail and any violations. Do NOT run `build.py validate` (scanners).

See `pieces/validation.md`.

```bash
python scripts/build.py get_instructions validate_slice
python scripts/build.py get_instructions validate_run
```

---

## Phase 9: Render Diagrams


| Human               | AI / Script           | AI               | Human → AI |
| ------------------- | --------------------- | ---------------- | ---------- |
| After model changes | Updates class diagram | Renders diagrams | Reviews    |


Update class diagram for domain model changes. See `pieces/diagrams.md`.

---

## Phase 10: Make Corrections


| Human                                | AI / Script                            | AI                             | Human → AI          |
| ------------------------------------ | -------------------------------------- | ------------------------------ | ------------------- |
| Reviews output and gives corrections | Invokes `get_instructions correct_run` | Applies corrections to run log | Updates and adjusts |


See `pieces/runs.md` for corrections format and `pieces/correct.md` for the correction layers.

```bash
python scripts/build.py get_instructions correct_run
python scripts/build.py get_instructions correct_all
```

---

## Improve Strategy / Improve Skill (at any time)


| Human                                        | AI / Script                                 | AI                                          | Human → AI          |
| -------------------------------------------- | ------------------------------------------- | ------------------------------------------- | ------------------- |
| Reviews corrections, decides what to promote | Invokes `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts |


**At any time during session and slice-run** a user may Improve Strategy from Corrections or Improve Skill from Corrections. See `pieces/correct.md` for the three layers (run → session → skill).

```bash
python scripts/build.py get_instructions improve_strategy
```

---

## Slice-Run Checklist

**Independent checklist per slice run.** Run `python scripts/create-checklist.py run <session> <n>` at the start of each run. Tick each item when done.


| #    | Phase   | Step                                                              | Done |
| ---- | ------- | ----------------------------------------------------------------- | ---- |
| 1    | Phase 7 | Model Generation — produce interaction tree + domain model for slice (builds on OOAD foundation) | ☐    |
| 2    | Phase 8 | Validate Rules — `get_instructions validate_slice`; apply rules, fix violations | ☐    |
| 3    | Phase 9 | Render Diagrams — update class diagram                            | ☐    |


Phase 10 (Make Corrections) and Improve Strategy / Improve Skill are recorded as needed. See `pieces/run_checklist_template.md` for the full checklist.

---

## Process Checklist

Each stage has an independent checklist. Kick off the checklist when starting that stage.

**1. Overall Context** — `overall-context-checklist.md`

- Phase 1: Skill space set
- Phase 2: Context prepared (chunk_index.json)
- Phase 3: Evidence extracted (evidence_graph.json)
- Phase 4: Concepts mapped (concept_scan.md)
- Phase 5: Model Discovery and Assessment (foundational-model.md)

**2. Session** — `<session>/session-checklist.md`

- Phase 6: Session created (`<session>-strategy.md`)

**3. Slice-Runs** — `<session>/runs/run-N-checklist.md` (per run)

- Phase 7: Model Generation
- Phase 8: Validate Rules and Scanners
- Phase 9: Render Diagrams
- Phase 10: Make Corrections
- Improve Strategy / Improve Skill — at any time from corrections

