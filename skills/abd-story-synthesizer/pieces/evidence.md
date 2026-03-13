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

### 01_analyze_chunks.py

Runs on chunks that already exist from `abd-context-to-memory`. Does NOT re-chunk.

- Validates chunk readiness: chunks present, count, paths, duplicates
- Builds chunk index with stable IDs, source locations, section mapping
- Output: `<workspace>/context/normalized/chunk_index.json`

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

```
<skill_space>/
  context/
    raw/                    # original source files (chunked by abd-context-to-memory)
    normalized/             # chunk_index.json from 01_analyze_chunks
    extracted/              # terms, actions, decisions, variations, states, relationships
    consolidated/           # evidence_graph.json, evidence_summary.md
```

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
python scripts/01_analyze_chunks.py --context-path <path>
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
