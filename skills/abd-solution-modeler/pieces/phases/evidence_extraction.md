# Phase 3 — Guided Evidence Extraction

**Actor:** Code | **Full spec:** [requirements.md](../../docs/requirements.md) § Phase 3

## Purpose

Extract structured domain evidence from rule text using Concept Guidance v1.

This phase converts raw rule text into structured evidence that later phases use
to construct the domain model and interaction model.

The extractor is **domain-agnostic** and must not rely on hard-coded verbs
or domain-specific terminology.

## Trigger

extract evidence, guided extraction, extract terms, extract actions, extract decisions

## Inputs

- `rule_chunks.json` — text chunks extracted from the source material
- `concept_guidance_v1.json` — guidance produced in Phase 2:
  - priority concepts
  - concept aliases
  - priority mechanisms
  - actors
  - variation axes
  - noise filters
  - focus sections

## Outputs

`terms.json`, `actions.json`, `decisions.json`, `states.json`, `relationships.json`, `modifiers.json`

## Run

```bash
python scripts/pipeline.py run 3
```

Script: `scripts/evidence_extraction_guided.py`

```bash
python scripts/evidence_extraction_guided.py -i <rule_chunks.json> -g <concept_guidance_v1.json> -o <output_dir>
```

## Post-extraction (AI self-check)

After the script completes, scan a sample of extracted items (actions, decisions, terms) against concept_guidance_v1:

- **Concept alignment:** Subject or object in priority_concepts (from guidance)
- **Rule prose:** Raw text is mechanical rule content, not structural junk (headings, TOC, chapter labels, all-caps titles)
- **No narrative flavor:** No archetype names, "The X does...", or prose that describes rather than specifies
- **No weak subjects:** No You, It, Perhaps, They as subject/object
- **No prose fragments:** No transitional phrases (Alternatively, Otherwise, Compare) as rule content

If junk found: warn user and suggest fixes (remove from JSON manually, or tighten extractor filters).
