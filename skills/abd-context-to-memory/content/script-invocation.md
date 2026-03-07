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

Converts source files to markdown. Writes .md alongside each source file (same folder).

**Single file (when user asks for one file):**
```bash
python scripts/convert_to_markdown.py --file <file_path>
```

**Folder (when user explicitly wants folder processed):**
```bash
python scripts/convert_to_markdown.py --memory <source_path>
```

- `--file`: Process ONLY the specified file. Use when user says "one file", "this file", "just X.pdf". Output: same folder as the source file.
- `--memory`: Process all supported files in folder. Tries under `Assets/` first, then workspace root.
- **OneDrive → SharePoint auto-injection:** When source is under a configured OneDrive path (e.g. `OneDrive - Agile by Design`), SharePoint URLs are auto-injected from `sharepoint_mapping.json`. No `--sharepoint-base` needed. Add mappings in `skills/abd-context-to-memory/sharepoint_mapping.json`.
- `--sharepoint-base <url>`: Override or use when source is not in OneDrive. Base URL to the folder (e.g. `https://.../Scotiabank/GTB`). Appends relative path and `?csf=1&web=1` (or `--sharepoint-query`).
- `--sharepoint-query <query>`: Optional. Default `csf=1&web=1`. Add `e=XXX` from a current SharePoint link if needed.

## chunk_markdown.py

Chunks converted markdown. Reads .md from source folder, writes to `memory/<name>/` (no chunked subfolder).

**Usage:**
```bash
python scripts/chunk_markdown.py --path <source_folder> [--memory <memory_name>]
```

- `--path`: Source folder containing converted .md files
- `--memory`: Optional. Memory folder name (default: last component of source path)
- Run convert first. Excludes chunked output (__slide_, __section_) from input.

## sync_sharepoint_urls.py

Syncs SharePoint URLs in memory chunks. **Run after chunk** when source lines have `source/... | https://...`. Replaces source path with SharePoint URL, fixes malformed URL order (path before query), and adds `wdSlideIndex` (pptx) or `page` (pdf) for direct slide/page links.

**Usage:**
```bash
python scripts/sync_sharepoint_urls.py [--memory <memory_name>]
```

- `--memory`: Optional. Memory folder name (e.g. `JBOM`). Operates on `memory/<name>/*.md`. If omitted, processes all .md under `memory/`.
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

## markdown_to_excel.py

Generic markdown → Excel. Parses headings, tables, paragraphs; writes to a new workbook.

**Dependencies**: `pip install openpyxl`

**Usage:**
```bash
python scripts/markdown_to_excel.py <input.md> [output.xlsx]
python scripts/markdown_to_excel.py --file <input.md> [--out <output.xlsx>]
```

**When to run:** When user wants to export markdown to Excel. For project-specific formats (e.g. JBOM B&T template), use workspace scripts.

## markdown_to_docx.py

Generic markdown → Word. Uses pypandoc.

**Dependencies**: `pip install pypandoc`. Requires pandoc binary: https://pandoc.org/installing.html

**Usage:**
```bash
python scripts/markdown_to_docx.py <input.md> [output.docx]
python scripts/markdown_to_docx.py --file <input.md> [--out <output.docx>]
```

## markdown_to_pdf.py

Generic markdown → PDF. Uses pypandoc.

**Dependencies**: `pip install pypandoc`. Requires pandoc + a PDF engine (pdflatex, weasyprint, or wkhtmltopdf).

**Usage:**
```bash
python scripts/markdown_to_pdf.py <input.md> [output.pdf]
python scripts/markdown_to_pdf.py --file <input.md> --pdf-engine weasyprint
```

If pdflatex is not installed: `pip install weasyprint` then use `--pdf-engine weasyprint`.

## index_memory.py

Full pipeline: convert → chunk → sync SharePoint → embed. Builds or updates the vector index for semantic search.

**Dependencies**: `pip install -r skills/abd-context-to-memory/requirements-rag.txt` (OpenAI API key for embeddings)

**Usage:**
```bash
python scripts/index_memory.py --path <source_folder>
python scripts/index_memory.py --replace
```

- `--path`: Source folder (e.g. `source/JBOM` or `Assets/04 Service Offering`). Full pipeline: convert → chunk → sync SharePoint → embed. Or chunk + embed if convert already ran.
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

## Layout

- **Converted markdown**: Written to **source folder** (alongside each source file)
- **Chunked content**: Written to **memory/<name>/** (no chunked subfolder). Sync and embed operate on these files.

## Key Behaviors

1. **Run convert before chunk** — Convert writes .md to source folder; chunk reads from source and writes to memory/<name>/.
2. **SharePoint URLs** — When source is in OneDrive, convert auto-injects SharePoint URLs from `sharepoint_mapping.json`. `sync_sharepoint_urls` (in pipeline) makes links shareable and adds slide/page params.
3. **Handle errors gracefully** — Some files may fail. Log and continue.
4. **Long-running** — Large folders (100+ files) take time.
5. **RAG**: Run `index_memory` after adding content; run `search_memory` when user asks for memory retrieval.
