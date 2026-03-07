# Core Definitions

## CommitScope

The unit of work a commit describes. Scope is inferred from conversation, changed files, and persisted state.

**Scope sources (priority order):**
1. **last_commit_scope.json** — Persisted scope from last meaningful commit or user override
2. **scope.json** — Current working scope (if non-empty)
3. **Conversation** — What the user asked to do; features, areas, artifacts discussed
4. **Changed files** — Paths, directory structure, file names, document content

**Context is also scope.** When working with abd-skills, infer scope from what part of the skill workflow is active:
- **abd-shaping** — Which slice is being run (Slice 1, Slice 2, …); which part of the strategy (create strategy, generate slice, improve strategy); which epic or story in the shaping output is being worked on; strategy doc path
- **abd-context-to-memory** — Which file or folder is being converted/chunked; which memory is being refreshed; pipeline step (convert, chunk, sync)
- **Other abd-skills** — Same pattern: slice, operation, artifact, or output section being worked on

Chat context often reveals this: "running Slice 2", "improving strategy for epic X", "chunking the PDF we just converted", "adding DO/DO NOT to strategy". Use it.

**Scope granularity (most specific wins):**
- Ace-skill context (e.g. "Slice 2", "Create Shaping Strategy", "chunk markdown")
- Feature/area name (e.g. "bot panel", "scope enrichment")
- Document type (e.g. "prioritization", "story map increments")
- Path-derived (e.g. "Invoke Bot" from `test/invoke_bot/`)
- Generic ("project artifacts") when nothing specific found

## Purpose

abd-commit-msg produces **intelligent commit messages** based on what we are doing with abd-shaping, abd-context-to-memory, or any other ace-skill. All abd-skills follow similar structure (content/, rules/, scripts/, output paths). Commit messages should reflect the active skill, operation, and scope — not generic "update project artifacts".

## Behavior

What kind of work the commit represents. Inferred from **changed files** first; fallback to `behavior_action_state.json` if present.

| Changed content | Behavior |
|-----------------|----------|
| abd-shaping output (strategy, slices, interaction tree, state model) | `shaping` |
| abd-context-to-memory (convert, chunk, memory) | `context` |
| Application/source code | `code` |
| Test files | `tests` |
| Story structure (epics, sub-epics, stories) | `shaping` |
| slices | `shaping` |
| steps | `exploration` |
| scenarios | `scenarios` |

## Action

The operation performed. From `current_action` (e.g. `render`, `build`, `validate`) or inferred (`build` for code/tests, `fix` for corrections).

## CommitMessage

The generated message. Format: `{behavior}.{action}: {meaningful description based on scope}`

- Present tense verbs
- Under 80 characters when possible
- Describe WHAT changed in relation to scope
