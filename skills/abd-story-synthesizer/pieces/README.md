# Pieces — Single Source of Truth

Domain-oriented content pieces. Each piece is one markdown file; one concept, one place. Section markers (`<!-- section: ... -->`) enable the engine to selectively include subsections per operation.

| Piece | Sections | Purpose |
|-------|----------|---------|
| `introduction.md` | `introduction` | What the synthesizer does; hierarchy overview |
| `interaction.md` | `interaction.model`, `interaction.inheritance`, `interaction.example` (`.hierarchy`, `.steps`), `interaction.output` (`.hierarchy`, `.details`, `.headings`) | Interaction data model, inheritance rules, complete example, output format |
| `domain.md` | `domain.model`, `domain.example`, `domain.output` | Domain Model, example from interaction tree, output format |
| `process.md` | `process` | Phase flow (1–6), script commands, paths |
| `session.md` | `session`, `session.traversal` | Session content (level of detail, scope, variation analysis, scaffold, slices), traversal order |
| `runs.md` | `runs`, `runs.corrections`, `runs.patterns` | Run lifecycle, run log structure, corrections format, patterns |
| `validation.md` | `validation.checklist` | Validation checklist (interaction tree, domain model, failure modes, content) |

## Section Marker Convention

All markers use prefix `story_synthesizer.` followed by `{piece}.{subsection}`:

```
<!-- section: story_synthesizer.introduction -->
<!-- section: story_synthesizer.interaction.model -->
<!-- section: story_synthesizer.interaction.inheritance -->
<!-- section: story_synthesizer.interaction.example -->
<!-- section: story_synthesizer.interaction.example.hierarchy -->   (epic + story level)
<!-- section: story_synthesizer.interaction.example.steps -->       (scenarios + steps)
<!-- section: story_synthesizer.interaction.output -->
<!-- section: story_synthesizer.interaction.output.hierarchy -->    (epics and stories view)
<!-- section: story_synthesizer.interaction.output.details -->      (story details: steps, examples)
<!-- section: story_synthesizer.interaction.output.headings -->     (heading level table)
<!-- section: story_synthesizer.domain.model -->
<!-- section: story_synthesizer.domain.example -->
<!-- section: story_synthesizer.domain.output -->
<!-- section: story_synthesizer.process -->
<!-- section: story_synthesizer.session -->
<!-- section: story_synthesizer.session.traversal -->
<!-- section: story_synthesizer.runs -->
<!-- section: story_synthesizer.runs.corrections -->
<!-- section: story_synthesizer.runs.patterns -->
<!-- section: story_synthesizer.validation.checklist -->
```

## Operation → Pieces Mapping (suggested)

| Operation | Pieces |
|-----------|--------|
| `create_strategy` | introduction, process, session |
| `run_slice` | introduction, interaction, domain, process, runs |
| `validate_run` | process, validation, runs |
| `validate_slice` | process, validation, runs |
| `improve_strategy` | process, session, runs |

## References

- `domain.md` concepts align with `interaction.md` Complete Example
- `process.md` Phase 2 → `session.md`
- `process.md` Phase 3 → `session.md` (slices), `runs.md` (run lifecycle)
- `process.md` Phase 4 → `validation.md` (checklist)
- `process.md` Phase 5 → `runs.md` § Corrections Format, § When User Gives a Correction
- `process.md` Phase 6 → `session.md` § Patterns, `runs.md` § Patterns
- `validation.md` verifies against `interaction.md` § Output Format and `domain.md` § Output Format
