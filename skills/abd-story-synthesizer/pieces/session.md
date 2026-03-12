# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, and slices. Context must be prepared before starting a session (see `pieces/context.md`). One run per slice; runs write logs.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes. Each session type defines what a run produces.


| Session Type      | What runs produce                                                                                                                                                                                             | Artifacts                                | Tags                                                                       | Slice size                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Story-Map (Epic/story hierarchy; short names only) as first cut of the **interaction tree. ** Foundational object model portion of the **domain model** (typed state: properties, operations, collaborators). | `interaction-tree.md`, `domain-model.md` | `discovery`, `story_map`, `epic`, `story`, `domain`                        | Large — one or more, foundational model or cross-cutting concernd per slice, all the way thin slice of multiple comcepts end to end |
| **Exploration**   | Full story fields: Trigger, Response, Pre-Condition, Triggering-State, Resulting-State, domain concepts, Failure-Modes, Constraints. Steps below stories. Completes domain model.                             | `interaction-tree.md`, `domain-model.md` | `exploration`, `story_map`, `epic`, `story`, `domain`, `step`              | Medium — a group of related stories that share state or workflow                                                                    |
| **Specification** | Steps grouped into scenarios. Examples (tables per concept). Failure-Modes.                                                                                                                                   | `interaction-tree.md`, `domain-model.md` | `specification`, `step`, `step_edge_case`, `scenario`, `example`, `domain` | Small — individual stories or story pairs with shared scenarios                                                                     |


**Default when no session:** `tags: [discovery, story_map, epic, story, domain]`.

### 2 - Scope

What portion of the analyzed context this session works with. Context must already be prepared (see `pieces/context.md`).

- **All** (default) — entire analyzed context
- **Subset** — specific context categories (e.g., "Payments module only", "User Registration + Authentication")

If no scope is set, ask the user. The AI can suggest scope based on the context analysis (concept report, variation analysis). Default is "all."

**Context readiness check:** Before setting scope, verify context is prepared (chunked, scanned, deep-read, variation analysis). If context is missing or stale, ask the user to prepare it first (see `pieces/context.md`).

### 3 - Slices

Slices define the order of work. Each slice scopes one run. Slice design depends on session type.

**DO NOT slice by epic.** Each slice must end to end lfe cycle of  a user, product, service or oter aspect of the user-solution journey

#### Discovery Slices

Discovery slices (slices focused on building the story-map) are **big** — scoped to a cross-cutting concern or foundational model from `context_analysis.json`. The variation analysis already identifies the models and their categories; each slice covers one model (or related group of models) and produces all the epics and stories that touch it.

**Slicing by foundational model:** Each model from context analysis becomes a candidate slice. Related models that share state (e.g., Resolution System used by Combat) may be grouped or ordered by dependency.

**Slice checklist:**

- Does the slice cover a complete foundational model or cross-cutting concern?
- Are state dependencies respected (creators before consumers)?
- Is the slice big enough to be coherent but small enough to review?

#### Exploration Slices

Exploration slices can reuse discovery slices or define new ones scoped to a smaller collection of stories that need details  added.

#### Specification Slices

Specification slices often scope to a couple of stories that need scenarios, examples, and failure modes.

### 4 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.

What each run produces is defined by the session's level of detail (see § 1). A session has one run type — all runs in a session produce the same kind of output.