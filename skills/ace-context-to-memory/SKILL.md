---
name: ace-context-to-memory
description: >-
  Takes various content sources, converts them to markdown, chunks them, and
  makes them available for future reference. Use when the user wants to "add to
  memory", "convert and chunk", "ingest for agent", or "refresh memory".
---

# ace-context-to-memory

**Very specific skill.** Does one thing: take content sources → convert to markdown → chunk → refer for future use. Does not need to change as we create new skills.

## Purpose

1. **Take various content sources** — PDF, PPTX, DOCX, XLSX, HTML, etc.
2. **Convert to markdown** — Non-.md files → `.md` in place.
3. **Chunk** — Split markdown into referable chunks (by slide, by heading, or whole file).
4. **Refer for future use** — Chunks live where agents/context can find them; source attribution in each chunk.

Folder layout, workspace sync, and integration with other context (e.g. Vesta 7) are secondary.

## When to Activate

- "Add content to memory", "refresh memory", "ingest for agent"
- "Sync workspace to memory", "convert and chunk"

## Step 1: Convert to Markdown

```bash
python scripts/convert_to_markdown.py --source <path> [--memory <domain>]
python scripts/convert_to_markdown.py --from source/<domain>/<topic>
```

- Writes `.md` in `<folder>/markdown/`
- `.md` files are skipped

## Step 2: Chunk to Memory

```bash
python scripts/chunk_markdown.py --memory <domain> [--incremental]
```

- Reads from: `source/<domain>/` or `memory/<domain>/`
- Writes to: `memory/<domain>/<topic>/`
- `--incremental`: Only chunk new or modified files

## Step 3: Sync Workspace (Convert + Copy + Chunk)

```bash
python scripts/sync_and_chunk.py --workspace <topic> --memory <domain> [--incremental]
```

## Chunking Strategy

- **Slide decks** (`<!-- Slide number: N -->`): One chunk per slide
- **Other docs** (>200 lines): Split at `#` or `##` boundaries
- **Small files** (<200 lines): Single chunk

Each chunk includes: `<!-- Source: path | file://url -->`

## Architecture

- **memory/**: Content and chunks. Markdown in `<folder>/markdown/`.
- **workspace/** (optional): Source content for sync_and_chunk.
- **.content-memory/transformers/** or **memory/<domain>/transformers/**: Project-specific converters.

**Run from workspace root.** Set `CONTENT_MEMORY_ROOT` if needed.

## Scripts

| Script | Purpose |
|--------|---------|
| `convert_to_markdown.py` | Convert to markdown |
| `chunk_markdown.py` | Chunk to memory |
| `sync_and_chunk.py` | Convert + copy + chunk (workspace) |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| No markdown | Run convert; then chunk. Or sync workspace to memory first. |
| Missing markitdown | `pip install "markitdown[all]"` |
