# Process Overview

Your task is to build an **Interaction Tree** and **Domain Model** using a pipeline that separates mechanical evidence extraction (CODE) from analytical reasoning (AI).

The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

---

## The Pipeline

```text
Phase 1: Set Skill Space
  - Configure workspace path and context paths

Phase 2: Prepare Context
  - Chunk source documents (abd-context-to-memory)
  - Analyze and index chunks (01_analyze_chunks)

Phase 3: Map Concepts
  - AI concept scan: primitives, mechanisms, authority boundaries, variation axes

Phase 4: Extract Evidence
  - Extract terms, actions, decisions, variations, states, relationships (scripts 02–07)
  - Build evidence graph (07_consolidate_evidence)

Phase 5: Create Session
  - Define level of detail, scope, and slices
  - One session per analysis focus (discovery / exploration / specification)

Phase 6: Run Slice
  - OOAD modeling (per-run): behavior packets → mechanisms → decision ownership → object candidates
  - Model validation (per-run): scenario walkthrough, anemia critique
  - Synthesize: produce interaction tree + domain model
  - Render class diagrams
  - Run scanners

Phase 7: Correct
  - Record corrections in run log
  - Promote to session strategy or skill rules

Phase 8: Adjust
  - Review corrections, update strategy, improve skill
```

---

## Phase 1: Set Skill Space

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "set skill space to X" or "new workspace" | Runs `build.py get_config`, validates paths | Reports paths; checks readiness | Confirms or provides new path |

Configure the skill space path in `abd-domain-synthesizer/conf/abd-config.json` and the context paths in `<skill-space>/conf/abd-config.json`.

```bash
python scripts/build.py get_config
```

---

## Phase 2: Prepare Context

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "prepare context" or provides source docs | Chunks documents, analyzes chunks | Reports chunk count and readiness | Confirms sources |

Chunk source documents into markdown using the `abd-context-to-memory` skill. Then validate and index the chunks.

```bash
python scripts/01_analyze_chunks.py --context-path <path>
```

Output: `<workspace>/normalized/chunk_index.json`

---

## Phase 3: Map Concepts

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "map concepts" or "concept scan" | Invokes `get_instructions concept_scan` | Produces conceptual map | Reviews and adjusts |

AI concept scan on normalized context. Discovers core primitives, interaction phases, authority boundaries, variation axes, rule mechanisms, and implicit concepts. This orients the evidence extraction and later AI passes.

```bash
python scripts/build.py get_instructions concept_scan
```

Output: `<session>/concept_scan.md`. See `pieces/concept_scan.md` for full specification.

---

## Phase 4: Extract Evidence

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "extract evidence" | Runs extraction pipeline (scripts 02–07) | Reports evidence counts and hotspots | Reviews summary |

Run the evidence extraction pipeline. Scripts extract structured evidence from normalized chunks — terms, actions, decisions, variations, states, relationships — then consolidate into an evidence graph.

```bash
python scripts/build.py extract_evidence
```

This runs scripts 02–07 in sequence:
- `02_extract_terms.py` — noun phrases, vocabulary index
- `03_extract_actions.py` — subject-verb-object behavioral facts
- `04_extract_decisions.py` — conditional logic and rules
- `05_extract_variations.py` — behavior axes and mode differences
- `06_extract_states.py` — stateful entities and explicit relationships
- `07_consolidate_evidence.py` — build evidence graph with links, clusters, hotspots

Output: `evidence_graph.json` and `evidence_summary.md` in `<workspace>/consolidated/`. See `pieces/evidence.md` for full specification.

---

## Phase 5: Create Session

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "start session" or "create session" | Invokes `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts |

Create, open, or continue an existing session. The session defines: Level of Detail (discovery/exploration/specification), Scope, and Slices. The evidence graph and concept scan are already available.

See `pieces/session.md` for session content, slice design, and tag definitions.

```bash
python scripts/build.py get_instructions create_strategy
```

---

## Phase 6: Run Slice

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Says "run slice", "build it", "proceed" | Invokes `get_instructions run_slice` | Produces interaction tree + domain model for slice | Reviews and adjusts |

Each slice run executes the full pipeline on slice-scoped evidence. The OOAD modeling steps run on every slice — depth varies by session type, not which steps execute (see `pieces/domain.md` § Depth by Session Type).

### Per-Run OOAD Modeling

Every run that discovers new evidence models it through the OOAD pipeline:

1. **Behavior packet detection** — cluster slice-scoped evidence into coherent mechanisms
2. **Mechanism synthesis** — find real structural seams from packets
3. **Decision ownership** — assign each decision to the concept that should own it
4. **Object candidate formation** — derive candidates from owned behavior and state
5. **Relationship & boundary modeling** — define relationships based on behavior
6. **Inheritance test** — verify substitutability before using inheritance

```bash
python scripts/build.py get_instructions model_discovery
```

See `pieces/domain.md` § Behavior Packet Detection through Inheritance Test.

### Per-Run Model Validation

Attack the candidate model before accepting it:

1. **Scenario / message walkthrough** — verify the model can actually behave
2. **Anemia / centralization critique** — find data bags, fake inheritance, misplaced behavior
3. **Final domain model** — produce the model only after passes stabilize

```bash
python scripts/build.py get_instructions model_validation
```

See `pieces/domain.md` § Model Validation.

### Synthesize

Produce the interaction tree and domain model for the slice. Domain concepts from the OOAD steps sync into the interaction tree via `**Concept**` references.

```bash
python scripts/build.py get_instructions run_slice
```

### Render & Validate

After producing output:
1. **Render diagrams** — update class diagram for domain model changes. See `pieces/diagrams.md`.
2. **Validate** — run `build.py validate`. Fix any violations before marking the run complete. See `pieces/validation.md`.

```bash
python scripts/build.py validate
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions validate_slice
```

---

## Phase 7: Correct

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Reviews output and gives corrections | Invokes `get_instructions correct_run` | Applies corrections to run log | Updates and adjusts |

See `pieces/runs.md` for corrections format and `pieces/correct.md` for the correction layers.

```bash
python scripts/build.py get_instructions correct_run
python scripts/build.py get_instructions correct_all
```

---

## Phase 8: Adjust

| Human | AI / Script | AI | Human → AI |
|-------|-------------|-----|------------|
| Reviews corrections, decides what to promote | Invokes `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts |

See `pieces/correct.md` for the three layers of correction (run → session → skill).

```bash
python scripts/build.py get_instructions improve_strategy
```

---

## Process Checklist

- **Skill space set** — workspace and context paths configured
- **Context prepared** — source docs chunked; chunks analyzed and indexed
- **Concepts mapped** — AI conceptual map in `concept_scan.md`
- **Evidence extracted** — scripts 02–07 complete; `evidence_graph.json` exists
- **Session created** — session file with level of detail, scope, and slices
- **Slice run** — per-run OOAD modeling + validation + interaction tree + domain model produced; diagrams rendered; scanners pass
- **Corrections recorded** — all corrections in run logs; promoted to session/skill as needed
- **Strategy adjusted** — corrections promoted; skill improved
