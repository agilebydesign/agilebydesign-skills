<!-- section: story_synthesizer.context -->
# Context Preparation

Prepared context is a foundational component that needs to be roesent before the skill can run. Check for prepared context when setting up or updating a skill space. Check for prepared context before starting a session or running a skill. Each step cascades: chunking before scanning, scanning before deep analysis.

## Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown using the abd-context-to-memory skill before analysis. The `get_instructions` command validates this automatically — if documents are unchunked or stale, it warns with the command to run.

- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "312 sections; Accounts 12–45, Transactions 46–95, Compliance 150–200; chunk types: account definitions, transaction rules, validation policies."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

## Concept Tracking

Run `concept_tracker.py` to extract terms from chunks and build a cross-reference matrix. Required before foundational models — if not available, stop and report the error.

```bash
python scripts/concept_tracker.py seed --source <domain-model-or-wordlist>   # optional: seed glossary
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <context_analysis.json> --min-units 5
```

**Output:** `context_analysis.json` (first version). Deep analysis extends this same file.

**`context_analysis.json` first version (from concept tracker):**
```json
{
  "context_path": "/workspace/context",
  "total_units": 312,
  "total_terms": 1845,
  "glossary_terms_used": 22,
  "units": [
    { "id": "section_042", "path": "rules/section_042.md", "terms": ["Account", "Transaction", "ValidationRule"] }
  ],
  "term_index": {
    "Account": ["section_012", "section_042", "section_078", "section_155"],
    "Transaction": ["section_042", "section_090", "section_155"]
  },
  "cross_references": [
    { "term": "Account", "unit_count": 145 },
    { "term": "Transaction", "unit_count": 112 }
  ],
  "co_occurrence": [
    { "terms": ["Account", "Transaction"], "count": 98 },
    { "terms": ["Transaction", "ValidationRule"], "count": 74 }
  ]
}
```

## Concept Deep Analysis

The concept tracker finds *what terms exist* and *where they co-occur*, but does NOT reveal mechanical variation. Before writing foundational models or variation analysis, deep-read the source chunks for each candidate model.

1. Use `term_index` from `context_analysis.json` to find which chunks contain each candidate model's key terms
2. For each candidate model, read 3–5 representative chunks
3. Extract the mechanically distinct categories by taking the time to **reading the actual source text again** — not from ai memory
4. Save results back to `context_analysis.json` — add a `deep_analysis` key to the existing file

**Deep analysis extends `context_analysis.json` with:**
```json
{
  "context_path": "...",
  "total_units": 312,
  "total_terms": 1845,
  "term_index": { "..." : "..." },
  "cross_references": [ "..." ],
  "co_occurrence": [ "..." ],
  "deep_analysis": {
    "models": [
      {
        "name": "Transaction Processing",
        "key_terms": ["Account", "Transaction", "ValidationRule"],
        "chunks_read": ["section_042.md", "section_090.md", "section_155.md"],
        "categories": [
          { "name": "Wire Transfer", "description": "Requires SWIFT code, multi-day settlement", "examples": ["domestic wire", "international wire"] },
          { "name": "ACH Transfer", "description": "Batch processing, routing number, same-day or next-day", "examples": ["payroll", "vendor payment"] }
        ]
      }
    ],
    "timestamp": "2026-03-11T15:30:00"
  }
}
```

**Validation pass on "examples" annotations:** After drafting the scaffold, for every annotation that says "X are examples (same flow)," verify from source chunks that all items share the same interaction flow. The test: does the item change who rolls, what DC, what triggers the check, or what the outcome does? If yes — separate story, not example.
