<!-- section: story_synthesizer.context -->
# Context Preparation

Prepared context is a foundational component that must be present before the skill can run. Each step cascades: chunking before evidence extraction, evidence extraction before AI passes.

## Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown using the `abd-context-to-memory` skill before any analysis. **Chunk output goes to `story-synthesizer/context/`** — not alongside the PDF. The source (PDF, etc.) stays where it is; only the processed `.md` chunks move into the skill.

- **Source:** Original content can live anywhere. If no path is set, `context/` at workspace root is the default source.
- **Chunks:** Output of chunking → `<workspace>/story-synthesizer/context/chunks/*.md`
- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "312 sections; Accounts 12–45, Transactions 46–95, Compliance 150–200; chunk types: account definitions, transaction rules, validation policies."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

## Evidence Extraction Pipeline

After chunking, run the evidence extraction pipeline to build structured evidence from the normalized chunks. See `pieces/evidence.md` for the full pipeline specification.

```bash
python scripts/build.py extract_evidence
```

Requires `chunk_index.json` from abd-context-to-memory. Runs scripts 02–07 in sequence:
- Chunk index — from abd-context-to-memory (`index_memory.py` or `index_chunks.py`); mandatory
- `02_extract_terms.py` — noun phrases, defined terms, vocabulary index
- `03_extract_actions.py` — subject-verb-object behavioral facts
- `04_extract_decisions.py` — conditional logic and rules
- `05_extract_variations.py` — behavior axes and mode differences
- `06_extract_states.py` — stateful entities and explicit relationships
- `07_consolidate_evidence.py` — build evidence graph with links, clusters, hotspots

**Output:** `evidence_graph.json` and `evidence_summary.md` in `<workspace>/story-synthesizer/evidence/`.

## Concept Tracking (Optional)

The `concept_tracker.py` tool remains available as a supplementary tool for quick term frequency and co-occurrence analysis. It is not required — the evidence extraction pipeline subsumes its function with richer evidence types.

```bash
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <context_analysis.json> --min-units 5
```

## Variation Analysis

The evidence extraction pipeline captures variations (script 05). For deeper analysis, review the extracted variations and formalize: per mechanism, what's consistent, what differs, what extends with new behavior (→ story) vs adds data to same behavior (→ example).

Variation analysis can be saved to `<workspace>/story-synthesizer/context/context_analysis.json` under each model's `variation` key for use in session strategy.
