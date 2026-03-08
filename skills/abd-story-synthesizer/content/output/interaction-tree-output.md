<!-- section: story_synthesizer.output.interaction_tree -->
# Interaction Tree Output

Format specification reverse-engineered from the Complete Example in `core.md`. See that example for a full reference.

**Constraints:** Any node can have a `Constraints:` collection — qualitative instructions on how the interaction is shaped. Each constraint may be a sentence, a file path, or (most commonly) a markdown reference. Inherited high to low. Typically at epic or story level; may appear in steps.

---

# Epics and Stories View (Hierarchy)

The tree view: Epic → Epic/Story children. Each node shows name, actors, and inherited vs own fields.

# Epic (filled out — has Examples)

- Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- `- Initiating-Actor:` value
- `- Responding-Actor:` value
- `- Constraints:` collection (sentence, file path, or markdown reference; inherited high to low)
- `- Pre-Condition:` full label (Given/And)
- `- Examples:` state table block (see Example Block Format below)

## Epic (not filled out — inherits only)

- Heading: `## Epic: <name using **Domain Concepts**> (<statement>)`
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [full inherited label]
- `- Examples:` [list of inherited state table names]
- `- Initiating-Actor:` [User] (or other actor)
- `- Responding-Actor:` [System] (or other actor)

### Story (filled out — has Initiation, Response, Failure-Modes, Scenarios)

- Heading: `### Story: <name using **Domain Concepts**> (<statement>)` — same pattern as Epic
- `- Pre-Condition:` [inherited]
- `- Failure-Modes:` bullet list (up to 3)
- `- Initiation:` sub-bullets Initiating-Actor, Behavior
- `- Response:` sub-bullets Responding-Actor, Behavior
- `###### Scenario:` name
- `####### Steps`
- Step items (see Story Details View)

### Story (not filled out)

- Heading: `#### Story:` + **Name**
- `- Constraints:` [inherited] or own collection
- `- Pre-Condition:` [inherited]
- `- Examples:` [inherited table names]
- `- Initiating-Actor:` [inherited]
- `- Responding-Actor:` [inherited]

---

# Story Details View (Drill-down)

When a story is expanded: Scenarios, Steps, and per-step Initiation/Response/Examples.

## Step (no Examples)

- `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- `- Constraints:` [inherited] or own (when step-specific)
- `- Initiation:` [inherited], Behavior
- `- Response:` [inherited], Behavior

## Step (with Examples)

- Same as Step (no Examples), plus `- Examples:` block
- Each table: label, blank line, header row, separator row, data rows
- Each table is a separate block; blank line between tables

## Step (system-initiated)

- Initiating-Actor overridden to [System] when the step is system-initiated (e.g. "When **System** receives...")

## Example table

Always add a qualifier in parentheses: `ConceptName (qualifier):`

- **Scenario column:** Required on entity tables. Use kebab-case (e.g. success, invalid-details, not-available).
- **Inherited examples:** Show as `Examples: [Table Name 1, Table Name 2, ...]` — list names, not tables.

## Epic-level example tables

Entity table (scenario + fields):

```
  Qualifier Domain Concept:
  | scenario   | field1 | field2   |
  |------------|--------|----------|
  | success    | val1   | val2     |
  | other-case | val1   | val2     |

  AnotherQualifier Domain Concept:
  | scenario   | field1 | field2 | field3 | field4 | field5 |
  |------------|--------|--------|--------|--------|--------|
  | success    | val1   | val2   | val3   | val4   | val5   |
  | other-case | val1   | val2   | val3   | val4   | val5   |
```

---

# Heading Levels

| Level | Use |
|-------|-----|
| `#` | Epic |
| `##` | Child Epic (Every level of nesting at a header level) |
| `###` | Story (Assuming only two levels of epic nesting) |
| `####` | Scenario (Assuming only two levels of epic nesting) |
| `#####` | Steps (Assuming only two levels of epic nesting) |
