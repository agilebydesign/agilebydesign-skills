<!-- section: story_synthesizer.context -->
# Context Preparation

Context preparation is a foundational activity — not part of a session. It happens when setting up or updating a skill space. Each step cascades: chunking before scanning, scanning before deep analysis.

## Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown before analysis. The `get_instructions` command validates this automatically — if documents are unchunked or stale, it warns with the command to run.

- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "406 sections; Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

## Concept Tracking

Run `concept_tracker.py` to extract terms from chunks and build a cross-reference matrix. Required before foundational models — if not available, stop and report the error.

```bash
python scripts/concept_tracker.py seed --source <domain-model-or-wordlist>   # optional: seed glossary
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <terms_report.json> --min-units 5
```

**Output:** `terms_report.json` with per-unit terms, term index, cross-references by frequency, and co-occurrence clusters. Use the report to drive foundational model identification.

## Concept Deep Analysis

The concept tracker finds *what terms exist* and *where they co-occur*, but does NOT reveal mechanical variation. Before writing foundational models or variation analysis, deep-read the source chunks for each candidate model.

1. Use `term_index` from `terms_report.json` to find which chunks contain each candidate model's key terms
2. For each candidate model, read 3–5 representative chunks
3. Extract the mechanically distinct categories from the actual source text — not from memory
4. Record which sections were read and what categories were found

**Validation pass on "examples" annotations:** After drafting the scaffold, for every annotation that says "X are examples (same flow)," verify from source chunks that all items share the same interaction flow. The test: does the item change who rolls, what DC, what triggers the check, or what the outcome does? If yes — separate story, not example.
