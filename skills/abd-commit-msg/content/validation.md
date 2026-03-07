# Validation

## Commit Message Checklist

Before executing the commit, verify:

- [ ] **Format:** `shaping.{operation}: {description}` for shaping; `{skill}: {description}` for other abd-skills (no operation)
- [ ] **Shaping operations:** strategy, run.1, run.2, …, improve_strategy, improve_skill — not build/run/prioritize
- [ ] **Scope** from last_commit_scope.md, scope, or inferred from conversation/changed files
- [ ] **Context as scope** — When using abd-skills: which slice, operation, or output section? Chat often reveals this.
- [ ] **Description** uses present tense; describes WHAT changed; references scope when relevant
- [ ] **Length** under 80 characters when possible
- [ ] **No Co-authored-by** trailers

## Scope Inference Checklist

When inferring scope:

- [ ] **Conversation first** — What did the user ask? Which slice? Which strategy section? Which file or memory?
- [ ] **Changed files second** — Paths, directory names, document types
- [ ] **Persist** inferred scope to last_commit_scope.md
- [ ] **Confirm** to user: "Inferred scope as [name] from conversation" or "from changed files"
