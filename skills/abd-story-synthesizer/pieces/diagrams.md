<!-- section: story_synthesizer.diagrams -->
# Class Diagrams

When a run produces or modifies domain model concepts, render the changes to a DrawIO class diagram. One page per foundational model. The diagram is the visual representation of `domain-model.md` — they stay in sync.

## Diagram File

**Path:** `<session>/class diagram.drawio` (alongside `domain-model.md`)

Each foundational model section in `domain-model.md` maps to one page in the diagram. Page names must match section names exactly (e.g., "Resolution System", "Combat System").

## When to Render

- **After producing domain model output** in a run — render new/changed concepts to the diagram
- **After corrections that change domain model** — update the diagram to match
- **After user edits the diagram in DrawIO** — sync back to `domain-model.md` using `sync-to-model`

## Tools

All tools are in `scripts/` in the synthesizer skill. Run from that directory.

```bash
cd skills/abd-story-synthesizer/scripts
python drawio_class_cli.py <command> <drawio-file> [options]
```

### Diagram Management

| Command | Usage |
|---------|-------|
| `init` | `init <file> --page <name>` — create file or add page |
| `inspect` | `inspect <file> [--page <name>]` — JSON: classes, edges, overlaps |
| `sync-to-model` | `sync-to-model <file> [--page <name>] [--model <md-path>]` — sync diagram classes back to domain-model.md with diffs |

### Class CRUD

| Command | Usage |
|---------|-------|
| `add-class` | `add-class <file> --page <page> --name <Name> [--base <Base>] [--props "p1\|p2"] [--ops "o1\|o2"] [--invs "i1\|i2"] [--x N] [--y N]` |
| `update-class` | `update-class <file> --page <page> --name <Name> --add-prop "..." \| --remove-prop "..." \| --add-op "..." \| --remove-op "..." \| --add-inv "..." \| --set-base <Base>` |
| `delete-class` | `delete-class <file> --page <page> --name <Name>` — removes class and all its edges |
| `move` | `move <file> --page <page> --name <Name> --x N --y N` |

### Relationship CRUD

| Command | Style | Usage |
|---------|-------|-------|
| `add-inheritance` | Hollow triangle (straight) | `--child <Child> --parent <Parent>` |
| `add-composition` | Filled diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-aggregation` | Hollow diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-association` | Open arrow (orthogonal) | `--from <Source> --to <Target> [--straight]` |
| `add-dependency` | Dashed open arrow (straight) | `--from <Source> --to <Target> [--label <text>]` |
| `delete-edge` | — | `--from <Source> --to <Target>` |

## Layout Guidelines

- **Inheritance:** Base on top, extensions below. Straight vertical lines preferred.
- **Composition/aggregation:** Orthogonal routing (right-angle corners). Diamond on the owner (parent) side.
- **Association:** Orthogonal routing. Use `--straight` when classes are on the same row to avoid bends.
- **Dependency:** Dashed straight line for creates/uses relationships (e.g., Rollable creates Check).
- **Grid layout:** Position classes in rows — parents row 0, children/dependents row 1+. Avoid all-on-one-row; aim for a square diagram.
- **No overlaps:** After positioning, run `inspect` to check for overlapping classes. Use `move` to fix.
- **No crossing edges:** Position classes so edges don't cross over other classes. Place related classes adjacent.

## UML Relationship Selection

| Relationship | When to use | DrawIO style |
|-------------|-------------|--------------|
| **Inheritance** | Concept extends another (e.g., Ability : Rollable) | Hollow triangle |
| **Composition** | Part cannot exist without whole; collection property (e.g., Character ◆→ Ability via Dictionary) | Filled diamond |
| **Aggregation** | Whole references part but part has independent lifecycle (e.g., Character ◇→ PowerLevel) | Hollow diamond |
| **Association** | Concept uses another in operations (e.g., Check → DC, Check → Degree) | Open arrow |
| **Dependency** | Concept creates instances of another (e.g., Rollable --creates-→ Check) | Dashed arrow |

## Cross-Model Imports

When a concept from one foundational model is referenced in another (e.g., Ability extends Rollable from Resolution System), mark it explicitly in both places.

### Domain Model Convention

Add `[from: Source Module]` after the base class:

```
**Ability** : Rollable [from: Resolution System]
**AttackCheck** : Check [from: Resolution System]
```

### Class Diagram Convention

Add the imported class using `--imported-from`:

```bash
python drawio_class_cli.py add-class <file> --page "Character Trait System" --name Rollable --imported-from "Resolution System" --props "Number modifier" --x 40 --y 620
```

The imported class renders with a dashed border and a `«from: Module»` stereotype label above the name. Add inheritance edges from local classes to the import as normal.

### Keeping Cross-Model References in Sync

When a concept changes in its home model:
1. Update the concept in the home model's page and domain-model.md section
2. Update imported copies in other pages (properties may differ — imports typically show only the key properties)
3. Run `inspect` on pages that import the concept to verify edges still connect

**Imported classes are lightweight copies** — they show the concept name, stereotype, and key properties only. They don't need full operations or invariants (those live in the home model).

## Domain Model Type Conventions

- **Enum types** for constrained options: `EnumType name {value1, value2, ...}` — not `String name (option1/option2)`
- **Derived properties** with invariants: `Number cost` + `Invariant: cost = rank × 2` — not `calculate_cost() → Number`
- **Invariants** for all rules, formulas, and constraints — not embedded in property descriptions or operation signatures

## AI Workflow for Rendering

After producing domain model output for a slice:

1. **Init** page if needed: `init <file> --page "<Model Name>"`
2. **Add classes** with properties, operations, invariants at planned grid positions
3. **Add edges** — inheritance first (defines vertical structure), then composition/aggregation, then associations/dependencies
4. **Inspect** to check for overlaps and edge routing
5. **Move** any classes that overlap or cause edge crossings
6. **Verify** sync: `sync-to-model` should report "no changes" (diagram matches model)

When user edits the diagram in DrawIO:

1. User saves the diagram
2. Run `sync-to-model` to see diffs and apply changes back to `domain-model.md`
