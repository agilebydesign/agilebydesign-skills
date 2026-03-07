# Output Structure

## Commit Message Format

**Shaping** (has operations):
```
shaping.{operation}: {meaningful description based on scope}
```

**Other abd-skills** (one skill, no operation concept):
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

**Other abd-skills** (e.g. context-to-memory) have no operation concept — use `{skill}: {description}`.
