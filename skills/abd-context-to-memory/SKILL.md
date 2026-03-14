---
name: abd-context-to-memory
description: >-
  Converts documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunks them
  for agent memory. Supports vector RAG search. Use when the user wants to "add
  to memory", "convert and chunk", "ingest content for agent", "refresh memory",
  "use memory", or process a folder of documents for AI agent context.
license: MIT
metadata:
  author: agilebydesign
  version: "1.1.0"
---

# Ace-Context-to-Memory

Converts source documents to markdown and chunks them for agent memory. Pipeline: **convert** (documents → markdown + images) → **chunk** (markdown → smaller files) → **embed** (vector index for semantic search).

## When to Activate

- User asks to "add content to memory" or "refresh memory"
- Wants to convert a folder of documents (PPTX, PDF, DOCX, XLSX) for agent context
- Mentions "convert and chunk", "ingest for agent", or "memory pipeline"
- Has added new files and wants them processed
- **"Use memory" / semantic retrieval:** User says "use memory", "search memory", "what does memory say about X", "from our content", "from ABD materials", "what do we have on [topic]" — run `search_memory "<query>"` and inject results into your response
- **Adding content from any folder:** When adding a folder's content to memory, run `link_workspace_source.py --path <folder>` first (on request) if the link does not yet exist

## CRITICAL: Respect User Scope

- **One file**: When user says "one file", "this file", "just X.pdf", or names a specific file → use `--file <path>`. Process ONLY that file.
- **Folder**: When user says "folder", "all", "everything in X", or explicitly requests a folder → use `--memory <path>`.
- **Do NOT** process entire folders when the user asked for a single file.

## OneDrive Folder Clarification

When the user refers to "OneDrive", "OneDrive folder", "slash OneDrive", or similar without specifying which OneDrive:

- **Ask which OneDrive folder** they mean (e.g. "OneDrive - Agile by Design", "OneDrive - Personal", "OneDrive - Company Name").
- If multiple OneDrive folders exist under the user's home and the configured path is missing or unclear, scripts will list them and prompt for choice — **do not guess**; ask the user to pick.
- If the user's request is ambiguous (e.g. "use OneDrive" or "get to OneDrive"), ask: "Which OneDrive folder do you want to use? For example: OneDrive - Agile by Design, OneDrive - Personal, or another?"

## Source Folder Structure

`source/` (under workspace root) contains content sources. Workspace folders can be linked for skill access:

- `source/<link_name>` — Junction/symlink to your content folder

Use `link_workspace_source.py` to create links before converting.

**Memory root:** When running the full pipeline, ROOT is derived from the source path (parent of source folder). Memory and index are stored alongside the source project — no hardcoded path. Set `CONTENT_MEMORY_ROOT` only when running `--memory` without a source (chunk+embed only).

## Pipeline Overview

1. **Convert**: Use `markitdown` to convert supported files to markdown. Images extracted and referenced. **SharePoint links**: When source is in OneDrive, SharePoint URLs are auto-injected from `sharepoint_mapping.json` so links work for anyone.
2. **Chunk**: Split large markdown by slides (decks) or headings (docs). Small files stay as single chunks.
3. **Index chunks**: Build `chunk_index.json` with stable IDs, paths, and section mapping. **Mandatory for abd-story-synthesizer** — required for evidence extraction. Writes to `<workspace>/story-synthesizer/context/chunk_index.json` when that path exists.
4. **Sync SharePoint URLs**: Replace source paths with SharePoint URLs; fix URL order; add `wdSlideIndex` (pptx) / `page` (pdf) for direct slide/page links. Run automatically in `index_memory --path` pipeline.
5. **Embed + Index** (RAG): Embed chunks with sentence-transformers, store in ChromaDB for semantic search.

## Semantic Search (RAG)

When the user says "use memory", "search memory", "what does memory say about X", "from our content", or asks about ABD materials:

1. Run from workspace root: `python skills/abd-context-to-memory/scripts/search_memory.py "<query>" --k 5`
2. Inject the returned chunks into your response
3. Cite sources (path, slide/page) when using retrieved content

Requires RAG deps: `pip install -r skills/abd-context-to-memory/requirements-rag.txt`

See `content/rag-retrieval.md` for trigger phrases and agent flow.

## Scripts

Run from workspace root. Scripts in `skills/abd-context-to-memory/scripts/`.

**RAG (vector search):**
- `index_memory.py --path <source_folder>` — full pipeline: convert → chunk → sync SharePoint → embed (or chunk + embed if convert already ran)
- `index_memory.py` — when `skill_space_path` is set and no folder specified, runs on `{skill_space_path}/context` automatically
- `index_memory.py --replace` — rebuild entire vector index from all memory
- `search_memory.py "<query>" [--k 5] [--format text|json]` — semantic search; returns top-k chunks

**Convert + chunk + index:**
- `link_workspace_source.py --path <folder> [--name <link_name>]` or `--workspace <folder_name>` — **run on request** when adding content to memory; creates junction/symlink in `source/` so skills can access the folder
- `convert_to_markdown.py --file <file_path>` — **single file only** (use when user asks for one file); writes markdown alongside the source file (same folder)
- `convert_to_markdown.py --memory <source_path>` — folder (all supported files). When source is in OneDrive, SharePoint URLs are auto-injected via `sharepoint_mapping.json`.
- `chunk_markdown.py --path <source_folder> [--memory <memory_name>]` — reads from source, writes to memory/<name>/
- `index_chunks.py --context-path <chunk_folder> [--output <path>]` — build chunk_index.json for abd-story-synthesizer. **Mandatory for context preparation.** Run after chunk. Writes to `<workspace>/story-synthesizer/context/chunk_index.json` by default.
- `embed_and_index.py [--memory <memory_name>] [--replace]` — embed chunks from memory/<name>/ into FAISS index (called by index_memory)
- `sync_sharepoint_urls.py [--memory <memory_name>]` — run after chunk when source has `source/... | https://...`; replaces with SharePoint URL, fixes URL order, adds `wdSlideIndex` (pptx) / `page` (pdf) for direct links
- `add_sharepoint_mapping.py --prefix "OneDrive - X" --base "<url>"` — add OneDrive→SharePoint mapping. Paste URL from browser; script derives base. Use when convert warns about missing mapping.

**Export (markdown → Excel, Word, PDF):**
- `markdown_to_excel.py <input.md> [output.xlsx]` — generic md → Excel (headings, tables, paragraphs)
- `markdown_to_docx.py <input.md> [output.docx]` — md → Word (requires pandoc)
- `markdown_to_pdf.py <input.md> [output.pdf]` — md → PDF (requires pandoc + PDF engine). Use `--pdf-engine weasyprint` if pdflatex not installed.

Requires: `pip install -r requirements-export.txt` (openpyxl, pypandoc). Project-specific exports (e.g. JBOM format) stay in workspace.

**When adding content from a folder to memory:** Run `link_workspace_source.py` first if the link does not yet exist. Examples:
```bash
python scripts/link_workspace_source.py --path "C:/docs/RFQ materials" --name "JBOM"
python scripts/link_workspace_source.py --workspace "Scotia Talent Journey Based Operating Model" --name "JBOM Agile Support"
```

**SharePoint link creation:** When copying content from OneDrive, local paths are not shareable. Configure `sharepoint_mapping.json` (OneDrive prefix → SharePoint base URL). Convert will auto-inject SharePoint URLs so links work for anyone. **If you run convert with OneDrive content but no mapping, you'll get a warning with instructions.** Add the mapping with `add_sharepoint_mapping.py --prefix "OneDrive - X" --base "<paste_url_from_browser>"` (paste any file URL; script derives the base).

See `content/script-invocation.md` for script usage; `content/rag-retrieval.md` for semantic search flow.

## Build

```bash
cd skills/abd-context-to-memory
python scripts/build.py
```
