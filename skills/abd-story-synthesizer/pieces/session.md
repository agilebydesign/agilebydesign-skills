# Sessions

**A session executes a sequence of runs that follow the same strategy.** Before synthesizing, set up a session (create new or continue existing). Sessions define level of detail, scope, variation analysis, scaffold, slices, and focus; saved as an MD file. One run per slice; runs write logs. See sections below for details.

## Session Content

A session has:

### 1 - Level of Detail

How deep the synthesis goes for each node. Discovery focuses on epics and stories; Exploration adds steps below stories; Specification adds steps, scenarios, and examples. The predefined session types have predefined node levels and fields (see table below). You can also define a custom level of detail.


| Session Type      | Node levels                                       | Fields per node                                                                                                                                                                                                                                                                   |
| ----------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Epics (can nest), Stories. Stopping point: story. | Epic: Name (verb-noun), Triggering-Actor, Responding-Actor, Constraints, domain concepts (`**Concept`**), Pre-Condition, Triggering-State, Resulting-State, Trigger (Behavior, Triggering-Actor), Response (Behavior, Responding-Actor). Story: same. Domain Model with concepts. |
| **Exploration**   | Steps (below story).                              | Step: Trigger, Response, Constraints (when step-specific). Steps not grouped into scenarios. No error conditions or edge cases. Straight and linear.                                                                                                                              |
| **Specification** | Steps, Scenarios (below story).                   | Step: Trigger, Response, Examples, Constraints (when step-specific). Steps grouped into scenarios. Failure-Modes (failure conditions).                                                                                                                                            |


See `core.md` for constraints, step format, and full field definitions.  

#### Validation and Build Rule Tags

The node levels and fields chosen to be generated (e.g. Epics, Stories, Steps, Examples) determine which rules guide the build and validate the output. Tags exist for elements and fields (`epic`, `story`, `step`, `example`, `domain`) and for session types (`discovery`, `exploration`, `specification`). A Discovery session generating epics and stories means all rules tagged with `discovery`, `epic`, `story`, `interaction_tree`, `domain` will be used; a Specification session adds `specification`, `step`, `scenario`, `example`, `step_edge_case`.

**How rules are injected:** The session/strategy declares tags in scope. When `get_instructions` is called, the engine filters rules from `rules/*.md` by matching any in-scope tag. Each rule file must have YAML frontmatter with `tags: [discovery, interaction_tree, story, domain, ...]`. Rules apply to both the build phase (guiding synthesis output) and validation (checking output against rules). See `rules/README.md` for the full tag set.


| Tag                | Description                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| `discovery`        | Story-level detail: Trigger, Response, Pre-Condition, Triggering-State, Resulting-State |
| `exploration`      | Steps below story; linear, no edge cases                                                |
| `specification`    | Steps, scenarios, examples, failure modes                                               |
| `interaction_tree` | Epic/Story hierarchy; names, actors, constraints                                        |
| `epic`             | Epic-level nodes; hierarchy, granularity                                                |
| `story`            | Story-level fields: Trigger, Response, Pre-Condition, etc.                              |
| `domain`           | Domain Model — concepts, Properties, Operations                                         |
| `step`             | Atomic Trigger/Response; When/Then or verb-noun                                         |
| `step_edge_case`   | Steps + Failure-Modes; error paths                                                      |
| `example`          | Example tables per concept                                                              |
| `scenario`         | Step grouping by path                                                                   |


**Default when no session:** `tags: [discovery, interaction_tree, epic, story, domain]`.

### 2 - Scope

What portion of the context we are working with. Scope is not just a list — it **categorizes** the context. Scope drives which slices get synthesized.

- **Raw context** — If we have nothing built yet: all context, or a subset. Categorize it (e.g. index, chunk types, section mapping). Example: "406 sections; Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251; chunk types: effect definitions, advantage definitions, skill definitions, combat rules."
- **Existing structure** — If we have built output: "these stories", "all these epics", "Epic 2 and its sub-epics".

**Chunking:** Not all context will be chunked, but chunking makes variation analysis much easier. When context is chunked, use the chunk inventory (index, types) to drive scope.

**Bespoke strategies:** A custom strategy can mix components beyond the predefined session types (e.g. discovery + examples at sub-epic level, or exploration + domain concepts). The strategy defines which tags are in scope; the engine filters rules accordingly. Examples can be scoped at different levels — the strategy defines where.

### 3 - Variation Analysis

Identify differences in the scope that allow you to synthesize the elements that go into the interaction tree and Domain Model. The analysis informs when to group context into a single story and the patterns used to create different stories. **Perform enough interaction and OOAD analysis** to identify differences that could come from any of:

- **Business rules** — distinct rules or conditions change behavior.
- **System interactions** — different systems or integration points change exchange pattern.
- **Workflows** — different sequences or paths change steps, actors, or outcomes.
- **Structure** — different concept shapes or taxonomies change the interaction.
- **State** — different state transitions or preconditions change required or resulting state.

**Go over all context in enough detail** to understand how to identify all items. For instance, if doing Discovery and the context is a game rulebook, go chapter by chapter and examine the rulebook for every different rule: is it more of the same (part of same story), or different (new story)?

**The AI is empowered to create a more detailed interaction tree and domain model at whatever detail it needs to identify a pattern.** Once it has done so, it can create the rest of stories using that pattern without detailing everything. The same holds for other session types: e.g. a Specification session might go through a couple of stories and attached domain to see how to write good examples, then not need to create the rest to know what examples stories would have — just name them.

#### Variation Analysis Structure

The session's Variation Analysis section should follow this structure (with more or less detail as needed):

**1. Context Inventory / Scope**

- Source paths, chunk index (if chunked), chunk types
- Map to structure: e.g. "Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251"

**2. Analysis — Interaction**

- **Verbs** — User/System actions (Configure, Add, Choose, Apply, Resolve, Roll, Track, Create, Assign, etc.)
- **Nouns** — Domain concepts (Character, Campaign, Effect, Modifier, etc.)
- **What is consistent, what is different** — Common interactions for potentially very different data. E.g. "Configure Effect" applies to Affliction, Damage, Weaken — same workflow, different parameters per effect type.

**3. Analysis — Domain**

- Combine nouns into domain concept scaffolding
- Per-concept: properties, lifecycle, relationships
- Effect-specific structure table (when applicable): each effect type has different data structure

**4. Scaffold — Interaction Model**

- Epic/Sub-epic/Story breakdown
- A few stories per epic in full detail; then "X more stories based on pattern" (e.g. "24 more Configure Effect stories grouped by structural similarity")
- Pattern-change boundaries (when does the pattern change? new epic? new sub-epic?)

**5. Scaffold — Domain Model**

- Module per major concept (Character, Power, Effect, etc.)
- State model scaffolding per concept

**Scaffold completeness:** The scaffold does not need to enumerate every story. A few stories per epic, then "X more stories based on each [power, effect, etc.]" is often sufficient. The pattern, once identified, drives the rest.

### 4 - Scaffold

Enough of the interaction tree and domain model is synthesized to understand how remaining slices will be processed. Initial structure: epic/sub-epic/story breakdown, a few stories in full detail, then "X more stories based on pattern." Domain concepts with properties, lifecycle, and relationships. The scaffold does not need to enumerate every story — patterns drive the rest.

#### Scaffold (by Session Type)


| Session Type      | Scaffolded together                                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | Interaction scaffold (epics, stories) + Domain scaffold. A few stories per epic in full; rest by pattern.                                    |
| **Exploration**   | Steps (linear). Optionally domain for step context.                                                                                          |
| **Specification** | Steps + Scenarios + Examples together. May scaffold a couple of stories with full examples to establish pattern, then apply pattern to rest. |


### 6 - Slices

The order in which you work through slices is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

A **slice** is a collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope for the run. Slices are stored in the session file; tick each when a run is done for it.

**Ideas:** Architectural slice, domain slice, integration slice, workflow slice, value slice, risk slice. Favour vertical slicing. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

**New session:** Slices can be carried over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

### 7 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.
