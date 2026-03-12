# Domain-Oriented Reorganization Proposal

**Goal:** Markdown as single source of truth for pieces; references when required; operations linked to pieces to generate instructions; easier to maintain.

---

## Current State

- **content/** — strategy.md, process.md, core.md, run-output.md, validation.md, script-invocation.md (large, overlapping)
- **content/output/** — interaction-tree-output.md, domain-model-output.md
- **rules/** — many .md files with tags
- **AGENTS.md** — monolithic assembled output; build.py merges content/*.md in fixed order
- **Operations** — create_strategy, run_slice, validate_run, etc. — pull from sections via `<!-- section: story_synthesizer.X -->`; config maps operations to section lists

**Problems:** Duplication (slices/runs defined in both process and strategy), unclear ownership (which doc owns what), hard to know what to edit when something changes.

---

## Proposed: Pieces + References + Operation Mapping

### 1. Pieces (single source of truth)

Each **piece** is one markdown file. One concept, one place.

```
pieces/
  session/
    model.md           # Session, Run, Slice — definitions only
    content.md         # Level of Detail, Scope, Variation Analysis, Scaffold
    types.md           # Discovery, Exploration, Specification tables
  process/
    flow.md            # Session-first flow (start session, work in runs, etc.)
    checklist.md       # Process checklist (session created, run 1 produced, …)
  output/
    interaction-tree.md
    domain-model.md
  run/
    run-log.md         # Run log format (Before, After, Corrections)
  validation/
    scope.md           # validate_run vs validate_slice
    checklist.md       # What to check (strategy alignment, tree format, etc.)
  operations/
    scripts.md         # build.py get_instructions, validate, paths
  shared/
    core.md            # Hierarchy, constraints, field definitions (referenced by many)
```

**Reference syntax:** When a piece needs content from another, use a reference instead of duplicating:

```markdown
<!-- ref: shared.core.hierarchy -->
```

Assembler resolves refs: either inline the target, or emit a short "See `pieces/shared/core.md` § Hierarchy".

---

### 2. Operation → Pieces Mapping

Config declares which pieces each operation needs. Engine assembles instructions by loading those pieces (and resolving refs).

```yaml
# conf/operations.yaml (or skill-config.json)
operations:
  create_session:
    pieces:
      - process.flow
      - session.model
      - session.content
      - session.types
    rules: [discovery, story_map, story, domain]  # or from session type

  run_slice:
    pieces:
      - process.flow
      - process.checklist
      - session.model
      - output.interaction-tree
      - output.domain-model
      - run.run-log
    rules: filtered_by_session_tags

  validate_run:
    pieces:
      - validation.scope
      - validation.checklist
    rules: filtered_by_session_tags
```

**Benefits:** Change "what is a slice" → edit `pieces/session/model.md` once. Change "run_slice instructions" → edit the operation's piece list, not scattered docs.

---

### 3. References Between Pieces

| From | References | Purpose |
|------|------------|---------|
| session.content | shared.core | Field definitions, hierarchy, constraints |
| output.interaction-tree | shared.core | Same |
| output.domain-model | shared.core | Same |
| validation.checklist | shared.core | What fields to check |
| process.flow | session.model | Slices, runs — link not duplicate |

**Ref resolution:** Assembler has two modes:
- **Inline** — Replace `<!-- ref: X -->` with content of X (for small refs)
- **Link** — Replace with "See `pieces/X.md`" (for large refs, avoid bloat)

---

### 4. Rules Stay Separate

Rules remain in `rules/*.md` with tags. Operation config says which tags (or "filtered by session"). No change to rules structure — they're already piece-like.

---

### 5. Migration Path

1. **Extract pieces** — Split strategy.md → session/model.md, session/content.md, session/types.md. Split process.md → process/flow.md, process/checklist.md. Same for validation, output, run-output.
2. **Add refs** — Replace duplicated content with `<!-- ref: ... -->`.
3. **Operation config** — Replace hardcoded section lists with piece lists per operation.
4. **Update build.py / engine** — Load pieces by path, resolve refs, assemble. Keep AGENTS.md generation for backward compat (build from pieces).
5. **Retire old content/** — Once pieces + config work, remove strategy.md, process.md as standalone files (or keep as thin wrappers that include pieces).

---

### 6. File Layout (Proposed)

```
abd-story-synthesizer/
  pieces/
    session/
      model.md
      content.md
      types.md
    process/
      flow.md
      checklist.md
    output/
      interaction-tree.md
      domain-model.md
    run/
      run-log.md
    validation/
      scope.md
      checklist.md
    operations/
      scripts.md
    shared/
      core.md
  rules/
    *.md                    # unchanged
  conf/
    operations.yaml         # operation → pieces mapping
    abd-config.json        # paths, skill_space, etc.
  scripts/
    build.py                # loads pieces, resolves refs, assembles
```

---

### 7. Maintenance Wins

| Change | Before | After |
|--------|--------|-------|
| Define "slice" | Edit process.md and strategy.md | Edit `pieces/session/model.md` |
| Add session type | Edit strategy.md, maybe AGENTS.md | Edit `pieces/session/types.md` |
| Change run_slice instructions | Hunt across content/, script-invocation | Edit `conf/operations.yaml` + relevant pieces |
| Add new operation | Add sections to multiple docs | Add operation to config, list pieces |
| Fix hierarchy definition | Edit core.md, hope nothing else breaks | Edit `pieces/shared/core.md`; refs get it everywhere |

---

### 8. Open Questions

- **Ref granularity:** Ref at file level, or section level? e.g. `<!-- ref: shared.core#hierarchy -->`
- **AGENTS.md:** Keep as flattened output for agents that read one file? Or have agents read pieces directly?
- **Backward compat:** Existing `<!-- section: story_synthesizer.X -->` — map to pieces, or phase out?
- **Engine location:** Is the assembler in this skill, or in a shared engine? Affects where `conf/operations.yaml` lives.
