# Configuration

**File:** `skill-config.json` (skill root)

## Paths (shareable config)

| Key | Purpose |
|-----|---------|
| `content_memory_root` | Local path to Assets folder. Use `~/OneDrive - Agile by Design/Shared Documents/Assets` so `~` expands to each user's home — config is shareable. |
| `content_memory_sharepoint_url` | SharePoint URL for the same folder. For documentation: sync from this URL; the portable path above will work if OneDrive is in the default location. |

**RAG data** is stored at `{content_memory_root}/data/rag/` (index.faiss, embeddings.npy, metadata.json).

**Override:** Set `CONTENT_MEMORY_ROOT` env var to override the config path.
