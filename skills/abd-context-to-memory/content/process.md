# Pipeline Process

## Step 1: Convert to Markdown

**Story: Convert content sources to markdown**

- **Required State**: Content in supported formats (PDF, PPTX, DOCX, XLSX, etc.)
- **Response**: Skill converts original artifact in its entirety to markdown; markdown stored alongside original (same folder)
- **Resulting State**: Markdown converted artifact available alongside original
- **Failure Modes**: Unsupported format; conversion fails; path invalid

**Supported formats**: `.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls`, `.html`, `.htm`, `.txt`, `.csv`, `.json`, `.xml`

## Step 2: Chunk Markdown

**Story: Chunk markdown**

- **Required State**: Markdown available
- **Response**: Skill splits markdown by slide, heading, or whole file; writes chunks with source attribution
- **Resulting State**: Chunks produced; available for reference
- **Failure Modes**: No markdown found; chunk strategy fails

**Chunking strategy**:
- Slide decks (`<!-- Slide number: N -->`): One chunk per slide
- Other docs (>200 lines): Split at `#` or `##` boundaries
- Small files (<200 lines): Kept as single chunk

## Step 3: Sync Workspace to Memory (full pipeline)

**Story: Sync workspace to memory (convert + copy + chunk)**

- **Required State**: —
- **Response**: Skill converts each original to markdown; copies chunks to `<workspace>/context-to-memory/memory/`; each file → one memory; memories nested; each memory points to original and markdown
- **Resulting State**: Memories populated
- **Failure Modes**: Workspace missing; copy fails; chunk fails
