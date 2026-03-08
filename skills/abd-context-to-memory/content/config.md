# Configuration

**File:** `skill-config.json` (skill root)

## Paths (shareable config)

| Key | Purpose |
|-----|---------|
| `content_memory_root` | Local path to Assets folder. Use `~/OneDrive - Agile by Design/Shared Documents/Assets` so `~` expands to each user's home — config is shareable. |
| `content_memory_sharepoint_url` | SharePoint URL for the same folder. For documentation: sync from this URL; the portable path above will work if OneDrive is in the default location. |
| `skill_space_path` | Project/skill-space root. When set and no folder is specified for `index_memory.py`, the skill automatically runs on `{skill_space_path}/context`. Falls back to `abd-story-synthesizer/conf/abd-config.json` when both skills are deployed. |

**RAG data** is stored at `{content_memory_root}/data/rag/` (index.faiss, embeddings.npy, metadata.json).

**Overrides:**
- `CONTENT_MEMORY_ROOT` — overrides `content_memory_root`
- `SKILL_SPACE_PATH` — overrides `skill_space_path`
