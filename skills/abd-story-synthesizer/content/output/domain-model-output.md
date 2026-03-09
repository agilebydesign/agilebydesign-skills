<!-- section: story_synthesizer.output.domain_model -->
# Domain Model Output

Separate from the Interaction Tree. Concepts referenced via `**Concept**` in labels. Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

## Format

```
Concept : <Base Concept if any>
- <type> property
      <collaborating concepts if any>
- <type> operation(<param>, ...)
     <collaborating concepts if any>
- Interactons Interaction Concept used by (root node only)
- examples: list of domain concept tables in interaction tree using this concept
```
