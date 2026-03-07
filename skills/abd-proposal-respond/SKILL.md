---
name: abd-proposal-respond
description: >-
  Respond to client proposals (RFP, Q&A, requirements) by converting materials
  to memory, creating a response strategy, and answering questions iteratively.
  Depends on abd-context-to-memory for RAG. Use when responding to proposals,
  creating response plans, answering RFP questions, or iterating on proposal strategy.
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# Ace-Proposal-Respond

Respond to client proposals by converting materials to memory, creating a response strategy, and answering questions in small batches. Uses abd-context-to-memory for RAG. Same iterate-on-strategy pattern as abd-shaping.
_
## When to Apply

- User wants to respond to an RFP, Q&A, or proposal requirements
- Creating a response plan from proposal documents
- Answering client questions using memory (RAG)
- Iterating on strategy with corrections (DO/DO NOT)

## Dependency: abd-context-to-memory

Run `index_memory.py --path <proposal_source>` before answering questions. Use `search_memory.py "<query>"` when drafting answers.

## Process

1. **Setup** — Convert proposal to memory; create response folder; symlink
2. **Strategy first** — Analyze documents; propose response plan; save to `response/strategy.md`
3. **Answer a few questions ONLY** — 3–5 per batch; use RAG; get approval
4. **Accelerators** — When answers reference `*See Appendix X (Name)*`, define and accumulate in the **Accelerator Table** (add/update row: slide file, numbers, URL). When done, run `build_appendix_deck.py` to assemble the appendix deck.
5. **Iterate** — Corrections → add DO/DO NOT to strategy; re-run or proceed

## Operations

| Operation | When |
|-----------|------|
| `create_strategy` | "Create strategy," "propose response plan," "analyze and plan" |
| `answer_questions` | "Answer questions," "answer a few," "next batch" |
| `improve_strategy` | "Correct," "fix that," "wrong" |
| `proceed_slice` | "Proceed," "expand," "next slice" |

## Scripts

- `setup_response.py --proposal <folder>` — Create response folder and symlink
- `build_appendix_deck.py --table <Accelerator_Table.md> [--output <path>]` — Assemble appendix deck from Accelerator Table (requires appendix_config.json or env)

## Build

```bash
cd skills/abd-proposal-respond
python scripts/build.py
```
