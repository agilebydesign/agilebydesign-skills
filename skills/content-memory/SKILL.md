---
name: content-memory
description: >-
  Converts documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunks them
  for agent memory. Use when the user wants to "add to memory", "convert and
  chunk", "ingest content for agent", "refresh memory", or process a folder of
  documents for AI agent context.
---

# Content Memory Pipeline

This skill teaches how to convert source documents to markdown and chunk them for agent memory. The pipeline has two steps: **convert** (documents → markdown + images) and **chunk** (markdown → smaller files for retrieval).

## When to Activate

Activate when the user:
- Asks to "add content to memory" or "refresh memory"
- Wants to convert a folder of documents (PPTX, PDF, DOCX, XLSX) for agent context
- Mentions "convert and chunk", "ingest for agent", or "memory pipeline"
- Has added new files to a content folder and wants them processed

## Pipeline Overview

1. **Convert**: Use `markitdown` to convert supported files to markdown. Images are extracted and referenced.
2. **Chunk**: Split large markdown files by slides (for decks) or headings (for docs). Small files stay as single chunks.

## Step 1: Convert to Markdown

**Dependencies**: `pip install "markitdown[all]"`

**Memory mode** (preserves folder structure under `memory/<name>/`):

```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `<source_path>`: Path to folder containing documents (e.g. `Assets/06 Client Engagements/Active/Scotiabank/CBE`)
- Creates: `memory/<name>/<rel>/converted/` (markdown + images)
- Creates: `memory/<name>/<rel>/chunked/` (empty, for step 2)

**Single-folder mode** (pipeline/intake → pipeline/converted):

```bash
python scripts/convert_to_markdown.py
```

Place source files in `pipeline/intake/`. Output goes to `pipeline/converted/`.

**Supported formats**: `.pdf`, `.pptx`, `.docx`, `.xlsx`, `.xls`, `.html`, `.htm`, `.txt`, `.csv`, `.json`, `.xml`

## Step 2: Chunk Markdown

**Memory mode**:

```bash
python scripts/chunk_markdown.py --memory <memory_name>
```

- `<memory_name>`: Name of the memory folder (e.g. `CBE` from `memory/CBE/`)
- Reads from: `memory/<name>/*/converted/`
- Writes to: `memory/<name>/*/chunked/`

**Pipeline mode**:

```bash
python scripts/chunk_markdown.py
```

- Reads from: `pipeline/converted/`
- Writes to: `pipeline/chunked/`

## Chunking Strategy

- **Slide decks** (markers `<!-- Slide number: N -->`): One chunk per slide
- **Other docs** (>200 lines): Split at `#` or `##` boundaries
- **Small files** (<200 lines): Kept as single chunk

Each chunk includes a source reference for navigation: `<!-- Source: path | file://url -->`

## Key Behaviors

1. **Run convert before chunk** – Chunk reads from converted output.
2. **Handle errors gracefully** – Some files may fail (permissions, format). Log and continue.
3. **Long-running** – Large folders (100+ files) take time. Run in background if needed.
4. **Memory location** – Chunked output lives in `memory/<name>/*/chunked/` or `pipeline/chunked/`.

## Scripts Location

Scripts are in this skill's `scripts/` folder. When installed:
- Project: `.agents/skills/content-memory/scripts/`
- Global: `~/.cursor/skills/content-memory/scripts/` (or agent-specific path)

**Run from the workspace root** (where `memory/` will be created). Set `CONTENT_MEMORY_ROOT` if the workspace root differs from the current directory.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `PermissionError` / `FileConversionException` | File may be locked. Close the document and retry. Script should log and continue. |
| `No markdown in memory/.../converted/` | Run convert step first. |
| `Missing dependency: markitdown` | `pip install "markitdown[all]"` |
| PPTX images not rendering | Optional: `pip install python-pptx`; Windows may need PowerPoint for slide export. |
