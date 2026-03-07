# RAG Semantic Retrieval

When the user asks about content in memory, run semantic search and inject results into your response.

## Trigger Phrases

Run `search_memory "<query>"` when the user says:

- "use memory", "search memory", "what does memory say"
- "from our content", "from ABD materials", "from our decks"
- "what do we have on [topic]"
- Asks about Agile, training, proposals, service offerings, client engagements, or ABD materials

## Agent Flow

1. **Derive query** — Extract a semantic query from the user's question (topic, concept, or question).
2. **Run search** — From workspace root:
   ```bash
   python .agents/skills/ace-context-to-memory/scripts/search_memory.py "<query>" --k 5
   ```
3. **Inject results** — Use the returned chunks in your response.
4. **Cite sources** — Include path, slide/page when using retrieved content.

## Requirements

- RAG deps: `pip install -r .agents/skills/ace-context-to-memory/requirements-rag.txt`
- `OPENAI_API_KEY` set (for embeddings)
- Index must exist: run `index_memory` after adding content

## Architecture

- **Chunk files** — File-based reference (e.g. "open the Agile Overview deck")
- **Vector index** — Semantic search via `search_memory` for topic-based retrieval

Pipeline: convert → chunk → (1) write chunk files (2) embed + index in FAISS.
