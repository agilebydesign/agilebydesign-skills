# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, and slices. Context must be prepared before starting a session (see `pieces/context.md`). One run per slice; runs write logs.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes. Each session type defines what a run produces.

| Session Type | What runs produce | Artifacts |
|---|---|---|
| **Discovery** | Story map (epic/story hierarchy, short names only). Foundational object model / domain model (typed state: properties, operations, collaborators). | `story-map.md` (hierarchy of names), `domain-model.md` (foundational models + concepts) |
| **Exploration** | Interaction detail on stories (Trigger, Response, Pre-Condition, domain concepts). Steps below stories. Completes domain model. | `interaction-tree.md` (stories with full fields), `domain-model.md` (completed) |
| **Specification** | Steps grouped into scenarios. Examples (tables per concept). Failure-Modes. | `interaction-tree.md` (scenarios + examples), `domain-model.md` (examples linked) |

#### Validation and Build Rule Tags

The session type determines which rules guide the build and validate the output.

| Tag | Description |
|---|---|
| `discovery` | Story-level: Trigger, Response, Pre-Condition, foundational models |
| `exploration` | Steps below story; linear, no edge cases |
| `specification` | Steps, scenarios, examples, failure modes |
| `interaction_tree` | Epic/Story hierarchy; names, actors, constraints |
| `epic` | Epic-level nodes; hierarchy, granularity |
| `story` | Story-level fields |
| `domain` | Domain Model — concepts, properties, operations |
| `step` | Atomic Trigger/Response |
| `step_edge_case` | Steps + Failure-Modes; error paths |
| `example` | Example tables per concept |
| `scenario` | Step grouping by path |

**Default when no session:** `tags: [discovery, interaction_tree, epic, story, domain]`.

### 2 - Scope

What portion of the analyzed context this session works with. Context must already be prepared (see `pieces/context.md`).

- **All** (default) — entire analyzed context
- **Subset** — specific context categories (e.g., "Payments module only", "User Registration + Authentication")

If no scope is set, ask the user. The AI can suggest scope based on the context analysis (concept report, variation analysis). Default is "all."

**Context readiness check:** Before setting scope, verify context is prepared (chunked, scanned, deep-read, variation analysis). If context is missing or stale, ask the user to prepare it first (see `pieces/context.md`).

### 3 - Slices

Slices define the order of work. Each slice scopes one run. Slice design depends on session type.

**DO NOT slice by epic.** Each slice must build AND use something end-to-end.

#### Discovery Slices

Discovery slices are **big** — scoped to a cross-cutting concern or foundational model from `context_analysis.json`. The variation analysis already identifies the models and their categories; each slice covers one model (or related group of models) and produces all the epics and stories that touch it.

**Slicing by foundational model:** Each model from context analysis becomes a candidate slice. Related models that share state (e.g., Resolution System used by Combat) may be grouped or ordered by dependency.

**Slice checklist:**
- Does the slice cover a complete foundational model or cross-cutting concern?
- Are state dependencies respected (creators before consumers)?
- Is the slice big enough to be coherent but small enough to review?

#### Exploration Slices

Exploration slices can reuse discovery slices or define new ones scoped to specific stories that need steps added.

#### Specification Slices

Specification slices scope to stories that need scenarios, examples, and failure modes.

### 4 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.

**Discovery runs produce:** Complete epics and stories for the slice's scope — Name, Trigger, Response, Pre-Condition, domain concepts, foundational model state (properties, operations, collaborators). Written to `interaction-tree.md` and `domain-model.md`.

**Exploration runs produce:** Steps below existing stories. Domain model completion. Written to the same output files.

**Validation pass on "examples" annotations:** After each run, for every annotation that says "X are examples (same flow)," verify from source chunks that all items share the same interaction flow. The test: does the item change who rolls, what DC, what triggers the check, or what the outcome does? If yes — separate story, not example.
