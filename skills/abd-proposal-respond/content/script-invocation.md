# Script Invocation

Run from workspace root (abd_content or agile-context-engine). Set `CONTENT_MEMORY_ROOT` if workspace differs from cwd.

## setup_response.py

Creates response folder and symlink for proposal response workflow.

**When to call:** Before creating strategy; when starting a new proposal response.

**Usage:**
```bash
python .agents/skills/abd-proposal-respond/scripts/setup_response.py --proposal <proposal_folder> [--project <project_root>]
```

**Parameters:**
- `--proposal` (required): Folder containing proposal material (e.g. `workspace/jbom response`)
- `--project` (optional): Project root for symlink (default: CONTENT_MEMORY_ROOT or cwd)

**Example:**
```bash
python .agents/skills/abd-proposal-respond/scripts/setup_response.py --proposal "workspace/jbom response"
```

**Output:** Creates `<proposal_folder>/response/` and symlink `<project_root>/response` → response folder.

---

## abd-context-to-memory (dependency)

Convert proposal material to memory and index for RAG. Run before answering questions.

**link_workspace_source.py** — Link proposal folder to source (if not already):
```bash
python .agents/skills/abd-context-to-memory/scripts/link_workspace_source.py --path "workspace/jbom response" --name "JBOM"
```

**index_memory.py** — Full pipeline (convert → chunk → embed):
```bash
python .agents/skills/abd-context-to-memory/scripts/index_memory.py --path "source/JBOM"
```

**search_memory.py** — Semantic search when answering questions:
```bash
python .agents/skills/abd-context-to-memory/scripts/search_memory.py "<query>" --k 5
```

---

## build_appendix_deck.py

Assembles the appendix deck from the Accelerator Table. Run when response is done and accelerators have been accumulated.

**When to call:** After completing answers that reference accelerators; when ready to produce the appendix PowerPoint.

**Usage:**
```bash
python .agents/skills/abd-proposal-respond/scripts/build_appendix_deck.py --table <accelerator_table_path> [--output <pptx_path>]
```

**Parameters:**
- `--table` (required): Path to Accelerator Table.md (e.g. `workspace/jbom response/Accelerator Table.md`)
- `--output` (optional): Output PPTX path. Default: derived from table path (e.g. `Appendix_Accelerators.pptx` in same folder)

**Example:**
```bash
python .agents/skills/abd-proposal-respond/scripts/build_appendix_deck.py --table "workspace/jbom response/Accelerator Table.md"
python .agents/skills/abd-proposal-respond/scripts/build_appendix_deck.py --table "workspace/jbom response/Accelerator Table.md" --output "workspace/jbom response/JBOM_Appendix_Accelerators.pptx"
```

**Config:** Create `appendix_config.json` in the table's directory:
```json
{
  "style_deck": "path/to/PO_Training.pptx",
  "onedrive_root": "C:/Users/.../OneDrive - Org/Shared Documents/Assets",
  "search_roots": ["path/to/Agile Thinking", "path/to/Client Engagements"]
}
```
Or set `APPENDIX_STYLE_DECK`, `APPENDIX_ONEDRIVE_ROOT` env vars.

**Note:** Project-specific builds (e.g. `build_jbom_appendix_deck.py`) may exist with hardcoded style deck and paths. The skill script is a generic entry point; extend or replace per project.

---

## build.py

Assembles content into AGENTS.md.

**Usage:**
```bash
cd skills/abd-proposal-respond
python scripts/build.py
```
