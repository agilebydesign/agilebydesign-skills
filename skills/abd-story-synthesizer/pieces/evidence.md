<!-- section: story_synthesizer.evidence -->
# Evidence Model

Evidence extraction is the disciplined compression step of the pipeline. Scripts extract structured evidence from normalized context without pretending to design the model. These are evidence records, not object candidates.

## Canonical Evidence Structure

All extraction scripts write into a shared structure:

```json
{
  "documents": [],
  "terms": [],
  "actions": [],
  "decisions": [],
  "variations": [],
  "states": [],
  "relationships": [],
  "issues": []
}
```

| Type | Description | Script |
|------|-------------|--------|
| terms | Nouns, concepts — index entries for navigating context | `02_extract_terms.py` |
| actions | Subject-verb-object behavioral facts | `03_extract_actions.py` |
| decisions | Conditional logic (if/when/unless/must/on success/on failure) | `04_extract_decisions.py` |
| variations | Independent behavior axes (mode/type differences) | `05_extract_variations.py` |
| states | Lifecycle hints, condition accumulation, transitions | `06_extract_states.py` |
| relationships | Explicit associations, ownership, containment, dependency | `06_extract_states.py` |
| issues | Ambiguities, conflicts, contradictions | `07_consolidate_evidence.py` |

**Terms are index entries, not classes.** Actions and decisions carry stronger evidence for domain modeling than nouns do.

## Evidence Extraction Scripts

### Chunk index (abd-context-to-memory)

**Chunk index creation lives in `abd-context-to-memory`.** Run `index_memory.py --path <context_folder>` or `index_chunks.py --context-path <chunk_folder>` from that skill. Mandatory before `extract_evidence`.

- Validates chunk readiness: chunks present, count, paths, duplicates
- Builds chunk index with stable IDs, source locations, section mapping
- Output: `<workspace>/story-synthesizer/context/chunk_index.json`

### 02_extract_terms.py

Builds the concept index from normalized chunks.

- Extracts noun phrases, defined terms, section titles, repeated domain vocabulary
- Output: `terms.json` with `term_id`, `name`, `aliases`, `occurrences`

### 03_extract_actions.py

Extracts behavioral facts as subject-verb-object patterns.

- Example: "attacker makes attack check", "target rolls resistance", "effect applies condition"
- Output: `actions.json`

### 04_extract_decisions.py

Captures rule logic from conditional triggers.

- Triggers: if, when, unless, must, may not, on success, on failure
- Example: "if attack roll >= defense → hit"
- Output: `decisions.json`

### 05_extract_variations.py

Detects independent behavior axes.

- Patterns: "close vs ranged", "different types", "depending on", "one of the following"
- Output: `variations.json`

### 06_extract_states.py

Extracts stateful entities and explicit relationships.

- States: lifecycle hints, condition accumulation, transitions
- Relationships: explicit associations, ownership, containment, dependency
- Output: `states.json`, `relationships.json`

### 07_consolidate_evidence.py

Builds the AI-ready evidence graph from all extracted evidence.

- Creates: concept clusters, term→action links, term→decision links, variation links, state links, ambiguity list, conflict list, hotspot detection
- Output: `evidence_graph.json`, `evidence_summary.md`

## File Layout

**Source vs chunks:** Original content (PDF, PPTX, etc.) can live anywhere — track its path. The **chunks** (markdown output from `abd-context-to-memory`) must live in `story-synthesizer/context/`, not alongside the PDF. If no context path is configured, the skill looks in `context/` at workspace root for the **source** to chunk; chunk output goes to `story-synthesizer/context/`.

All processed context and evidence live under `story-synthesizer/`:

```
<workspace>/
  context/                  # original source (PDF, etc.) — default when none set; chunks go to story-synthesizer
  story-synthesizer/
    context/                # processed context
      chunks/               # chunk files (.md from abd-context-to-memory)
      chunk_index.json      # from abd-context-to-memory (index_chunks)
      context_analysis.json # from concept_tracker scan
      glossary.json         # from concept_tracker seed
    evidence/               # all evidence outputs
      terms.json, actions.json, decisions.json, variations.json, states.json, relationships.json
      evidence_graph.json, evidence_summary.md
```

**context_paths** in config points to `story-synthesizer/context/` (where chunks live) for evidence extraction.

## How Evidence Maps to Domain Model

| Evidence Type | Maps To |
|---------------|---------|
| actions | Operations on domain concepts |
| decisions | Policies, invariants, rules owned by concepts |
| variations | Polymorphic families, strategy patterns |
| states | Lifecycle, state machines, condition tracking |
| relationships | Composition, aggregation, association, dependency |
| terms | Index for navigating — NOT directly to classes |

## Running the Pipeline

```bash
# Chunk index: run from abd-context-to-memory first (index_memory.py or index_chunks.py)
python scripts/02_extract_terms.py --chunks <chunk_index.json>
python scripts/03_extract_actions.py --chunks <chunk_index.json>
python scripts/04_extract_decisions.py --chunks <chunk_index.json>
python scripts/05_extract_variations.py --chunks <chunk_index.json>
python scripts/06_extract_states.py --chunks <chunk_index.json>
python scripts/07_consolidate_evidence.py --extracted-path <extracted/>
```

Or use the build script shortcut:

```bash
python scripts/build.py extract_evidence
```
