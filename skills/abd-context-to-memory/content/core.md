# Core Definitions

## State Concepts (Add Context to Memory)

- **ContentSource** — Original artifact (PDF, PPTX, DOCX, XLSX, etc.) in supported format
- **Markdown** — Converted artifact; full fidelity; stored alongside original
- **Chunk** — Split unit of markdown for retrieval; by slide, heading, or whole file
- **Memory** — Single memory entry; one per file; points to original and markdown
- **Memories** — Collection of memories; nested by source structure
- **Workspace** — Root path containing content sources and memory output

## Epic: Add Context to Memory

- **Actor**: Developer
- **Supporting**: ace-context-to-memory
- **Required State**: Workspace with content sources
- **Initiation**: Developer requests add to memory (convert and chunk, ingest, refresh)
- **Response**: Skill converts each original to markdown; chunks markdown into memory; each file → one memory; memories nested; each memory points to original and markdown
- **Resulting State**: Memories available for future reference
