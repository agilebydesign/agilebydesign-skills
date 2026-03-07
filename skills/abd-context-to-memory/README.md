# ace-context-to-memory

Convert documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunk for agent memory. Supports RAG (vector search) and SharePoint link injection for OneDrive content.

## Quick start

- **Convert**: `pip install "markitdown[all]"` then `python scripts/convert_to_markdown.py --memory <source_path>`
- **RAG**: `pip install -r requirements-rag.txt` then `python scripts/index_memory.py --path <source_folder>`
- **Build**: `python scripts/build.py` to assemble AGENTS.md

Set `CONTENT_MEMORY_ROOT` if workspace root differs from cwd.
