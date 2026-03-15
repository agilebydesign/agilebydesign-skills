# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, and slices. Context must be prepared before starting a session (see `pieces/context.md`). One run per slice; runs write logs.

**Session location:** `<workspace>/story-synthesizer/<session-name>/`. Strategy: `<session-name>-strategy.md`. Runs: `runs/run-N.md`, `runs/run-N-validation.md`, `runs/run-N-checklist.md`. OOAD foundation is produced in Stage 1 (Phase 5) at workspace level: `story-synthesizer/foundational-model.md`. Slice runs produce `domain-model.md`.

## Session Naming

When the user says "run a session called X" (e.g. "run a session called discovery") and does **not** provide a custom name, name the session `X<unique number>` so it does not collide with existing sessions. Examples: `discovery1`, `discovery2`, `exploration1`. If the user specifies a name (e.g. "run a session called my-campaign-discovery"), use that name instead.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes. Each session type defines what a run produces.

**Pipeline mapping:**

| Session Type      | Pipeline phases | Interaction detail | Domain model detail |
| ----------------- | --------------- | ------------------ | ------------------- |
| **Discovery**     | 2, 5, 6 (skeleton) | Epic/story hierarchy; short names only | Foundational concepts; names + interactions only |
| **Exploration**   | 6 (full), 7–9   | Trigger, Response, Pre-Condition; Steps; Failure-Modes, Constraints | Complete: properties, operations, collaborators |
| **Specification** | 6 (full), 12    | Steps in scenarios; Examples (tables per concept); Failure-Modes | Refinements from walkthrough |

| Session Type      | What runs produce                                                                                                                                                                                             | Artifacts                                | Tags                                                                       | Slice size                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Story-Map (Epic/story hierarchy; short names only) as first cut of the **interaction tree.** Foundational object model portion of the **domain model** (typed state: properties, operations, collaborators). | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `discovery`, `story_map`, `epic`, `story`, `domain`                        | Large — one or more, foundational model or cross-cutting concern per slice, all the way thin slice of multiple concepts end to end |
| **Exploration**   | Full story fields: Trigger, Response, Pre-Condition, Triggering-State, Resulting-State, domain concepts, Failure-Modes, Constraints. Steps below stories. Completes domain model.                             | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `exploration`, `story_map`, `epic`, `story`, `domain`, `step`              | Medium — a group of related stories that share state or workflow                                                                    |
| **Specification** | Steps grouped into scenarios. Examples (tables per concept). Failure-Modes.                                                                                                                                   | `story-synthesizer/interactions/interaction-tree.md`, `story-synthesizer/domain/domain-model.md` | `specification`, `step`, `step_edge_case`, `scenario`, `example`, `domain` | Small — individual stories or story pairs with shared scenarios                                                                     |


**Default when no session:** `tags: [discovery, story_map, epic, story, domain]`.

### 2 - Scope

What portion of the analyzed context this session works with. Context must already be prepared (see `pieces/context.md`).

- **All** (default) — entire analyzed context
- **Subset** — specific context categories (e.g., "Payments module only", "User Registration + Authentication")

If no scope is set, ask the user. The AI can suggest scope based on the context analysis (concept report, variation analysis). Default is "all."

**Context readiness check:** Before setting scope, verify context is prepared (chunked, scanned, deep-read, variation analysis). If context is missing or stale, ask the user to prepare it first (see `pieces/context.md`).

### 3 - Slices

Slices define the order of work. Each slice scopes one run. Slice design depends on session type.

**Apply slice rules** when designing slices. Run `get_instructions create_strategy` to load rules. After creating strategy, run `get_instructions validate_session --strategy <path>` to validate slices against slice rules.

**When user says "validate session" or "validate the session":** Run `get_instructions validate_session --strategy <path>` (path = session's strategy file). Apply those instructions: load rules, validate slices against slice rules (size, cross-cutting, foundation inclusion). Report pass/fail and any violations.

**Epics from context (not slices):** Do not name epics after slices. Epics and sub-epics come from the larger context (goal, domain, concept map, evidence). Place slice stories under appropriate sub-epics. See [interaction-epics-from-context](../rules/interaction-epics-from-context.md).

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

**During session creation (before any slice runs):** When the user corrects strategy, slices, or scope, apply the fix and record the correction in `runs/run-0.md`. See `pieces/runs.md` § When User Gives a Correction.

What each run produces is defined by the session's level of detail (see § 1). A session has one run type — all runs in a session produce the same kind of output.