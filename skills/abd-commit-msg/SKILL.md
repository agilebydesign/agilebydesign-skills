---
name: abd-commit-msg
description: Generate meaningful commit messages from scope and changed files. No story_graph — scope from conversation, changed files, and persisted state. Use when user types /commit or requests a commit.
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# Ace Commit Message

Generate meaningful commit messages. **No story_graph** — scope is derived from conversation, changed files, and persisted state (`last_commit_scope.json`, `scope.json`).

## When to Apply

- User types `/commit` or requests a commit
- After completing a meaningful change (auto-commit when configured)
- **Do NOT** commit before completing the user's primary instructions

## Key Concepts

- **Scope** — From last_commit_scope.json, scope.json, conversation, or changed files. Not from story-graph.json.
- **Context as scope** — When using abd-skills (abd-shaping, abd-context-to-memory, etc.), scope includes: which slice, operation, or output section is being worked on. Chat often reveals this.
- **Behavior** — Inferred from changed files (code, tests, shape, prioritization, etc.)
- **Format** — `{behavior}.{action}: {meaningful description based on scope}`

Commit messages should reflect the active abd-skill, operation, and scope — not generic "update project artifacts".

## Output

See `content/output.md` and `docs/ace-commit-msg-output.md` for Interaction Tree and State Model.

## Build

```bash
cd skills/abd-commit-msg
python scripts/build.py
```
