# Overall Context Checklist

**Independent checklist.** Kick off when starting Overall Context. Complete all items before proceeding to Session.

**CRITICAL: Run phases in order.** Phase 2: use `index_memory.py` when source has PDF/PPTX/DOCX — not `index_chunks.py` alone.

Run `python scripts/create-checklist.py overall` to create. Tick (☑) each item when done.

| # | Phase | Step | Done |
|---|-------|------|------|
| 1 | Phase 1 | **Set Skill Space** — workspace and context paths configured | ☐ |
| 2 | Phase 2 | **Prepare Context** — source docs chunked; chunk_index.json exists (use index_memory.py for PDF/PPTX/DOCX) | ☐ |
| 3 | Phase 3 | **Extract Evidence** — evidence_graph.json and evidence_summary.md exist | ☐ |
| 4 | Phase 4 | **Map Concepts** — concept_scan.md produced | ☐ |
| 5 | Phase 5 | **Model Discovery** — `get_instructions model_discovery`; cluster evidence into mechanisms, ownership, candidates | ☐ |
| 6 | Phase 5 | **Model Assessment** — `get_instructions model_validation`; scenario walkthrough, anemia critique, base check | ☐ |
| 7 | Phase 5 | **Persist OOAD foundation** — foundational-model.md and domain/domain-model.md written; do not proceed to Session until stable | ☐ |
