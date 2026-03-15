## Context Preparation

Use **abd-context-to-memory** before Phase 1 if source is documents:

- `index_memory.py --path <source_folder>` — convert, chunk, embed
- Output: `chunk_index.json` (required for evidence extraction)
- Path: `skills/abd-context-to-memory`

**Config:** Set `chunk_index_path` or `context_path` in `conf/abd-config.json`. Or pass `--chunk-index PATH` / `--context-path PATH` when running the pipeline.
