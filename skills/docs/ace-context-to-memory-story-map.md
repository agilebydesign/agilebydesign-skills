# Interaction Tree and State Model — ace-context-to-memory

**Source:** `ace-context-to-memory` skill — SKILL.md, scripts  
**Methodology:** ace-shaping skill  
**Domain:** ace-context-to-memory — content sources → markdown → chunks → refer for future use  
**Assumption:** Developer initiates; ace-context-to-memory responds. Integration (e.g. Vesta 7) is separate.

---

## A) Interaction Tree

```
Epic: Add Context to Memory
     Actor: Developer
     Supporting: ace-context-to-memory
     Required State: Workspace with content sources
     State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
     Initiation: Developer requests add to memory (convert and chunk, ingest, refresh)
     Response: Skill converts each original artifact in full to markdown (alongside original, within workspace); chunks markdown into memory; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
     Resulting State: Memories available for future reference
│
├─ Story: Convert content sources to markdown
│    Required State: Content sources available (PDF, PPTX, DOCX, etc.)
│    State Concepts: ContentSource, Markdown
│    Initiation: Developer requests conversion (or step 1 of pipeline)
│    Response: Skill converts original artifact in its entirety to markdown; markdown stored alongside original (same folder)
│    Resulting State: Markdown converted artifact available alongside original artifact
│    Failure Modes: Unsupported format; conversion fails; path invalid
│
├─ Story: Chunk markdown
│    Required State: Markdown available
│    State Concepts: Markdown, Chunk
│    Initiation: Developer requests chunking (or step 2 of pipeline)
│    Response: Skill splits markdown by slide, heading, or whole file; writes chunks with source attribution
│    Resulting State: Chunks produced; available for reference
│    Failure Modes: No markdown found; chunk strategy fails
│
└─ Story: Sync workspace to memory (convert + copy + chunk)
     Required State: Workspace with content
     State Concepts: ContentSource, Markdown, Chunk, Memory, Memories, Workspace
     Initiation: Developer requests sync workspace to memory
     Response: Skill converts each original to markdown in full (alongside original); copies chunks to <workspace>/ace-output/ace-context-to-memory/memory/; each file → one memory; memories nested; each memory points to original artifact and markdown converted artifact
     Resulting State: Memories populated; available for reference
     Failure Modes: Workspace missing; copy fails; chunk fails
```

---

## B) State Model

Concepts scoped to the smallest subtree where they are used.

### ContentSource, Markdown, Chunk, Memory, Memories, Workspace (Epic: Add Context to Memory)

```
ContentSource
- String path
     Path to source file or folder
     invariant: supported format (PDF, PPTX, DOCX, XLSX, HTML, etc.)
- String format
     File extension / type
- Markdown convert(): Markdown
     ContentSource
     Converts to markdown in place

Markdown
- String path
     Path to .md file
     invariant: alongside original artifact (same folder as source)
- String content
     Full content converted to markdown
     invariant: includes <!-- Source: path | file://url --> when converted
- String artifact_ref
     Original artifact this markdown was converted from
     invariant: path to PDF, PPTX, DOCX, etc.
- Chunk[] chunk(): Chunk[]
     Markdown
     Splits by slide, heading, or whole file

Chunk
- String path
     Path to chunk file
     invariant: <workspace>/ace-output/ace-context-to-memory/memory/<folder>/<stem>__<label>.md
- String content
     Chunk content
     invariant: includes <!-- Source: path | file://url --> for attribution
- String source_ref
     Original source path and location (slide/section)
     invariant: <!-- Source: path, location | url -->

Memory
- String path
     Folder in <workspace>/ace-output/ace-context-to-memory/memory/
     invariant: each folder = one memory
- Chunk[] chunks
     Chunked markdown for one specific file
     invariant: all chunks from same original artifact
- String artifact_ref
     Original artifact (source file: PDF, PPTX, DOCX, etc.)
     invariant: path or file://url to the file that was added
- String markdown_ref
     Markdown converted artifact (full file, alongside original)
     invariant: same folder as original; entire content converted to markdown
- Memory[] children
     Nested memories
     invariant: memories are nested (folder hierarchy)

Memories
- String root_path
     <workspace>/ace-output/ace-context-to-memory/memory/ subfolder
     invariant: under workspace
- Memory[] memories
     All memory folders (nested)
- Chunk[] refer(): Chunk[]
     Chunks available for agents/context to find

Workspace
- String path
     Folder (root of project/IDE or subfolder)
     invariant: everything gets packed into this workspace
- String name
     Workspace identifier
     invariant: derived from path
```

---

## C) Inline Concepts (Epic: Add Context to Memory)

| Concept | Properties | Operations |
|---------|------------|------------|
| **ContentSource** | path, format | convert(): Markdown |
| **Markdown** | path, content | chunk(): Chunk[] |
| **Chunk** | path, content, source_ref | — |
| **Memory** | path, chunks, artifact_ref, markdown_ref, children | — |
| **Memories** | root_path, memories | refer(): Chunk[] |
| **Workspace** | path, name | — |

---

## Notes

- **Very specific skill:** ace-context-to-memory does one thing: take content → convert → chunk → memories. Does not need to change as we create new skills.
- **Memories structure:** Each folder in the memory subfolder = one Memory. A Memory = chunked markdown for one specific file. Memories are nested. Each memory points to (1) original artifact and (2) markdown converted artifact.
- **Conversion in place:** The original artifact is converted in its entirety to markdown; the markdown file is stored alongside the original (same folder). Chunks are derived from that markdown and stored in memory.
- **Triad:** Memory ↔ Original Artifact ↔ Markdown Converted Artifact. Each memory links to both: the source file (artifact_ref) and the full markdown version (markdown_ref, alongside original).
- **Chunking strategy:** Slide decks → one chunk per slide; docs >200 lines → split at # or ##; small files → single chunk.
- **Source attribution:** Each chunk includes `<!-- Source: path | file://url -->` for traceability.
- **Integration:** How chunks are added to context (e.g. Vesta 7) is separate; this skill produces referable chunks.
- **Workspace:** All skill operations happen in the context of a workspace — a folder (likely at root of project/IDE, or a subfolder). Everything gets packed into that workspace. Workspace path in engine config (engine knows where to find it).
- **Skill outputs:** Always at <workspace>/ace-output/<skill>/. This skill's memory: <workspace>/ace-output/ace-context-to-memory/memory/.
