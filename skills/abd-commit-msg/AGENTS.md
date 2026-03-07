# Core Definitions

## CommitScope

The unit of work a commit describes. Scope is inferred from conversation, changed files, and persisted state.

**Scope sources (priority order):**
1. **last_commit_scope.json** — Persisted scope from last meaningful commit or user override
2. **scope.json** — Current working scope (if non-empty)
3. **Conversation** — What the user asked to do; features, areas, artifacts discussed
4. **Changed files** — Paths, directory structure, file names, document content

**Context is also scope.** When working with ace-skills, infer scope from what part of the skill workflow is active:
- **ace-shaping** — Which slice is being run (Slice 1, Slice 2, …); which part of the strategy (create strategy, generate slice, improve strategy); which epic or story in the shaping output is being worked on; strategy doc path
- **ace-context-to-memory** — Which file or folder is being converted/chunked; which memory is being refreshed; pipeline step (convert, chunk, sync)
- **Other ace-skills** — Same pattern: slice, operation, artifact, or output section being worked on

Chat context often reveals this: "running Slice 2", "improving strategy for epic X", "chunking the PDF we just converted", "adding DO/DO NOT to strategy". Use it.

**Scope granularity (most specific wins):**
- Ace-skill context (e.g. "Slice 2", "Create Shaping Strategy", "chunk markdown")
- Feature/area name (e.g. "bot panel", "scope enrichment")
- Document type (e.g. "prioritization", "story map increments")
- Path-derived (e.g. "Invoke Bot" from `test/invoke_bot/`)
- Generic ("project artifacts") when nothing specific found

## Purpose

ace-commit-msg produces **intelligent commit messages** based on what we are doing with ace-shaping, ace-context-to-memory, or any other ace-skill. All ace-skills follow similar structure (content/, rules/, scripts/, output paths). Commit messages should reflect the active skill, operation, and scope — not generic "update project artifacts".

## Behavior

What kind of work the commit represents. Inferred from **changed files** first; fallback to `behavior_action_state.json` if present.

| Changed content | Behavior |
|-----------------|----------|
| ace-shaping output (strategy, slices, interaction tree, state model) | `shaping` |
| ace-context-to-memory (convert, chunk, memory) | `context` |
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

---

# Process

## When to Run

- User types `/commit` or requests a commit
- After completing a meaningful change (auto-commit when configured)
- **CRITICAL:** Do NOT commit before completing the user's primary instructions. If the user's message contains scope, behavior instructions, validation steps, build process, or workflow steps AND "commit", complete those first. The commit rule must not shortcut the actual workflow.

## Process Steps

1. **Read context files** (workspace root):
   - `last_commit_scope.json` — Preferred scope source
   - `scope.json` — Fallback scope
   - `behavior_action_state.json` — Current behavior/action (optional; override from changed files)

2. **Update last scope** (if scope.json changed):
   - If `scope.json` has non-empty `value`, save to `last_commit_scope.json` with timestamp
   - User overrides: "scope is [name]" or "scope is all" → save immediately

3. **Infer behavior from changed files**:
   - Run `git status` and `git diff`
   - Match changed content to behavior (code, tests, shape, prioritization, exploration, scenarios, domain, design)
   - Use `behavior_action_state.json` only if changed files don't clearly match

4. **Infer scope** (when both scope files empty):
   - **First:** Conversation — what did the user ask? What features, areas, artifacts were discussed?
   - **Then:** Changed files — paths, directory names, document types, file names
   - Save inferred scope to `last_commit_scope.json`
   - Last resort: `{behavior}.{action}: Update project artifacts`

5. **Generate commit message**:
   - Format: `{behavior}.{action}: {meaningful description based on scope}`
   - Use present tense; keep concise; reference scope when relevant

6. **Execute**:
   - `git add -A`
   - `git commit -m "message"`
   - **Never** add Co-authored-by trailers

## Scope Inference (No story_graph)

**From conversation:** Epic, sub-epic, story, feature area, document type — whatever the user discussed. Use chat history.

**From changed files:**
- `test/invoke_bot/...` → "Invoke Bot" or "perform action"
- `docs/story/prioritization/*` → "story map increments" or "prioritization"
- `src/panel/*.js` → "bot panel" or "UI components"
- `story-graph.json` diff → parse for epic/story names if present (optional; not required)
- `docs/crc/*` → "CRC documentation"
- Test file name `test_render_drawio_diagrams.py` → "Synchronized Graph" or "DrawIO diagrams"

**Scope is "all":** Use generic description.

---

# Output Structure

## Commit Message Format

**Shaping** (has operations):
```
shaping.{operation}: {meaningful description based on scope}
```

**Other ace-skills** (one skill, no operation concept):
```
{skill}: {meaningful description based on scope}
```

**Examples:**
- `shaping.strategy: Create strategy for Agile Context Engine`
- `shaping.run.1: Add Slice 1 stories for Create Ace-Skill epic`
- `shaping.run.2: Add Slice 2 stories for Initialize Engine`
- `shaping.improve_strategy: Add DO/DO NOT for hierarchy rules`
- `shaping.improve_skill: Promote corrections to base skill rules`
- `context-to-memory: Chunk markdown for workspace memory`
- `context-to-memory: Convert PDF to markdown for agent context`
- `context-to-memory: Sync workspace to memory`

## Scope Output

When scope is inferred or updated, persist to `last_commit_scope.md`.

## Shaping Operations

| Operation | When |
|-----------|------|
| strategy | Create or update strategy doc |
| run.1, run.2, … | Run slice N; produce 4–7 stories |
| improve_strategy | Add DO/DO NOT corrections to strategy |
| improve_skill | Post-shaping; promote corrections to base skill |

**Other ace-skills** (e.g. context-to-memory) have no operation concept — use `{skill}: {description}`.

---

# Validation

## Commit Message Checklist

Before executing the commit, verify:

- [ ] **Format:** `shaping.{operation}: {description}` for shaping; `{skill}: {description}` for other ace-skills (no operation)
- [ ] **Shaping operations:** strategy, run.1, run.2, …, improve_strategy, improve_skill — not build/run/prioritize
- [ ] **Scope** from last_commit_scope.md, scope, or inferred from conversation/changed files
- [ ] **Context as scope** — When using ace-skills: which slice, operation, or output section? Chat often reveals this.
- [ ] **Description** uses present tense; describes WHAT changed; references scope when relevant
- [ ] **Length** under 80 characters when possible
- [ ] **No Co-authored-by** trailers

## Scope Inference Checklist

When inferring scope:

- [ ] **Conversation first** — What did the user ask? Which slice? Which strategy section? Which file or memory?
- [ ] **Changed files second** — Paths, directory names, document types
- [ ] **Persist** inferred scope to last_commit_scope.md
- [ ] **Confirm** to user: "Inferred scope as [name] from conversation" or "from changed files"

---

# Script Invocation

No scripts. Use as Cursor rule (`.cursor/rules/`) or inject AGENTS.md into the AI prompt when user requests a commit. The skill produces instructions only; the AI executes `git add` and `git commit`.

---
