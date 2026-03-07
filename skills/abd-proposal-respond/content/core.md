# Core Definitions

<!-- section: proposal.core.definitions -->
## Concepts

- **ProposalSource** — Client RFP, Q&A, requirements (PDF, PPTX, DOCX, XLSX, etc.)
- **Memory** — Converted and chunked content; searchable via RAG (ace-context-to-memory)
- **ResponseFolder** — Output area for response artifacts; created alongside proposal material; symlinked from project
- **Strategy** — Response plan: which questions, in what order, format guidance, DO/DO NOT corrections
- **Accelerator** — A lettered appendix reference (A, B, C, …) that answers cite; typically a framework, method, or approach with source slides. Defined by appendix letter and framework name.
- **Accelerator Table** — Markdown table that defines and accumulates accelerators: appendix letter, framework name, slide file, slide numbers, URL. Each answer reference adds or updates a row; built in real time.

## What This Skill Does

- Convert proposal material to memory (via ace-context-to-memory)
- Create response folder and symlink
- Propose a strategy (question coverage, order, format)
- Answer questions using memory RAG
- **Define and accumulate accelerators** — When answers reference `*See Appendix X (Name)*`, define the accelerator (appendix letter, framework name) and accumulate it in the Accelerator Table with slide file, slide numbers, and URL. Each reference adds or updates a row.
- **Correct** — When user says "correct," add DO/DO NOT to the strategy document; re-run

## Pattern from Shaping (what we reuse)

- **Inject prompt** — Instructions are assembled per operation and injected into the AI prompt
- **Strategy** — A strategy document (`response/strategy.md`) holds the plan and accumulated corrections
- **Correct** — Corrections go into the strategy (DO/DO NOT with wrong/correct examples); do not just fix the answer in place

## Dependency: ace-context-to-memory

- Convert documents to markdown and chunks
- Index for semantic search
- Run `search_memory "<query>"` when answering questions
