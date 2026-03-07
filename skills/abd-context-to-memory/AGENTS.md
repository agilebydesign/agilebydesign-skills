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

---

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

---

# Output Structure

## Memory Mode

- **Convert**: `memory/<name>/<rel>/converted/` (markdown + images)
- **Chunk**: `memory/<name>/<rel>/chunked/` (chunked markdown)

## Pipeline Mode (single-folder)

- **Convert**: `pipeline/converted/`
- **Chunk**: `pipeline/chunked/`

## Chunk Source Reference

Each chunk includes: `<!-- Source: path | file://url -->` for navigation.

---

# Script Invocation

Run from workspace root. Set `CONTENT_MEMORY_ROOT` if workspace root differs from current directory.

**Dependencies**: `pip install "markitdown[all]"` (convert)

## link_workspace_source.py

Creates a junction (Windows) or symlink (Unix) so a folder is accessible under `source/`. **Run on request** when adding content to memory and the link does not yet exist.

**Usage:**
```bash
python scripts/link_workspace_source.py --path <folder_path> [--name <link_name>]
python scripts/link_workspace_source.py --workspace <workspace_folder_name> [--name <link_name>]
```

- `--path`: Any folder (absolute or relative to ROOT). Use for arbitrary folders.
- `--workspace`: Shorthand for `workspace/<name>/source` (workspace RFQ folders).
- `--name`: Link name under `source/` (default: last component of target path).

**Examples:**
```bash
python scripts/link_workspace_source.py --path "C:/docs/RFQ materials" --name "JBOM"
python scripts/link_workspace_source.py --path "workspace/Scotia Talent Journey/source" --name "JBOM Agile Support"
python scripts/link_workspace_source.py --workspace "Scotia Talent Journey Based Operating Model" --name "JBOM Agile Support"
```

**When to run:** Before `convert_to_markdown.py --memory` for a folder, if the user requests adding that content to memory and the link is not yet present.

## convert_to_markdown.py

Converts source files to markdown. Creates `memory/<name>/*/converted/`.

**Single file (when user asks for one file):**
```bash
python scripts/convert_to_markdown.py --file <file_path>
```

**Folder (when user explicitly wants folder processed):**
```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `--file`: Process ONLY the specified file. Use when user says "one file", "this file", "just X.pdf". Output: `memory/<filename_stem>/` — subfolder named after the file; all chunks in one place.
- `--memory`: Process all supported files in folder. Tries under `Assets/` first, then workspace root.
- **OneDrive → SharePoint auto-injection:** When source is under a configured OneDrive path (e.g. `OneDrive - Agile by Design`), SharePoint URLs are auto-injected from `sharepoint_mapping.json`. No `--sharepoint-base` needed. Add mappings in `skills/ace-context-to-memory/sharepoint_mapping.json`.
- `--sharepoint-base <url>`: Override or use when source is not in OneDrive. Base URL to the folder (e.g. `https://.../Scotiabank/GTB`). Appends relative path and `?csf=1&web=1` (or `--sharepoint-query`).
- `--sharepoint-query <query>`: Optional. Default `csf=1&web=1`. Add `e=XXX` from a current SharePoint link if needed.

## chunk_markdown.py

Chunks converted markdown. Reads from `memory/<name>/*/converted/`, writes to `memory/<name>/*/chunked/`.

**Usage:**
```bash
python scripts/chunk_markdown.py --memory <memory_name>
```

- `<memory_name>`: Name of folder under `memory/` (e.g. `CBE`)
- Run convert first

## sync_sharepoint_urls.py

Syncs SharePoint URLs in memory chunks. **Run after chunk** when source lines have `source/... | https://...`. Replaces source path with SharePoint URL, fixes malformed URL order (path before query), and adds `wdSlideIndex` (pptx) or `page` (pdf) for direct slide/page links.

**Usage:**
```bash
python scripts/sync_sharepoint_urls.py [--memory <memory_name>]
```

- `--memory`: Optional. Limit to one folder under `memory/`. If omitted, processes all `memory/**/*.md`.
- Run after `chunk_markdown.py`

## add_sharepoint_mapping.py

Adds a OneDrive → SharePoint mapping so convert can generate shareable links. **Use when convert warns about missing mapping**, or when adding a new OneDrive root.

**Usage:**
```bash
python scripts/add_sharepoint_mapping.py --prefix "OneDrive - Org" --base "<sharepoint_url>"
python scripts/add_sharepoint_mapping.py --path <file_in_onedrive> --base "<sharepoint_url>"
```

- `--prefix`: OneDrive folder name (e.g. `OneDrive - Agile by Design`).
- `--base`: SharePoint URL. Paste the full file URL from the browser; script strips to document library base.
- `--path`: File under OneDrive; prefix is extracted automatically.
- `--query`: Optional. Default `csf=1&web=1`.

**When to run:** When convert prints "WARNING: Source is in OneDrive but no SharePoint mapping is configured."

## index_memory.py

Full pipeline: convert → chunk → sync SharePoint → embed. Builds or updates the vector index for semantic search.

**Dependencies**: `pip install -r skills/ace-context-to-memory/requirements-rag.txt` (OpenAI API key for embeddings)

**Usage:**
```bash
python scripts/index_memory.py --path <source_folder>
python scripts/index_memory.py --memory <memory_name>
python scripts/index_memory.py --replace
```

- `--path`: Source folder (e.g. `Assets/04 Service Offering`). Converts, chunks, embeds. Use for new content.
- `--memory`: Memory name (folder under `memory/`). Chunks must already exist. Embeds and indexes.
- `--replace`: Rebuild entire vector index from all memory (drops existing index).

**When to run:** After adding or updating content; before first semantic search.

## search_memory.py

Semantic search over indexed chunks. Returns top-k matches with source paths.

**Usage:**
```bash
python scripts/search_memory.py "<query>" [--k 5] [--format text|json]
```

- `"<query>"`: Semantic query (topic, concept, question).
- `--k`: Number of chunks to return (default: 5).
- `--format`: `text` (default) or `json`.

**When to run:** When user says "use memory", "search memory", "what does memory say about X", "from our content", "from ABD materials", or asks about Agile/training/proposals/ABD materials. Run from workspace root; inject results into response; cite sources.

See `content/rag-retrieval.md` for trigger phrases and agent flow.

## SharePoint Link Creation (OneDrive)

When content is in OneDrive, local file paths are not shareable. **If you run convert with OneDrive content but no mapping, you'll get a warning with instructions.**

### Add a mapping (when warned or for new OneDrive roots)

1. Open any file from the OneDrive folder in SharePoint/OneDrive web.
2. Copy the URL from the browser address bar.
3. Run:

```bash
python scripts/add_sharepoint_mapping.py --prefix "OneDrive - Agile by Design" --base "<paste_url_here>"
```

Or with a file path (prefix is auto-detected):

```bash
python scripts/add_sharepoint_mapping.py --path "C:/Users/.../OneDrive - Org/Shared Documents/file.pptx" --base "<paste_url_here>"
```

The script derives the base URL from a full file URL, so you can paste the URL as-is.

### Manual config

Edit `sharepoint_mapping.json` in the skill root and add entries to the `mappings` array:

```json
{
  "mappings": [
    {
      "onedrive_prefix": "OneDrive - Agile by Design",
      "sharepoint_base": "https://...sharepoint.com/:f:/r/sites/SiteName/Shared%20Documents",
      "sharepoint_query": "csf=1&web=1"
    }
  ]
}
```

Convert will auto-inject SharePoint URLs for any file under the configured OneDrive prefix. `sync_sharepoint_urls.py` (run automatically in `index_memory --path`) then adds `wdSlideIndex` (pptx) and `page` (pdf) for direct slide/page links.

## Key Behaviors

1. **Run convert before chunk** — Chunk reads from converted output.
2. **SharePoint URLs** — When source is in OneDrive, convert auto-injects SharePoint URLs from `sharepoint_mapping.json`. `sync_sharepoint_urls` (in pipeline) makes links shareable and adds slide/page params.
3. **Handle errors gracefully** — Some files may fail. Log and continue.
4. **Long-running** — Large folders (100+ files) take time.
5. **RAG**: Run `index_memory` after adding content; run `search_memory` when user asks for memory retrieval.

---
