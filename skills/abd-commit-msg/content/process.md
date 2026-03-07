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
