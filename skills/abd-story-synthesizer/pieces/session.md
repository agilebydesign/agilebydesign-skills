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

### 2 - Context

Context preparation has three steps: chunk it, scan it, read it. Each step builds on the previous.

#### 2a - Context Chunking

Source documents (PDF, PPTX, DOCX) must be chunked into markdown before analysis. The `get_instructions` command validates this automatically — if documents are unchunked or stale, it warns with the command to run.

- **Raw context:** Categorize what you have — source paths, chunk count, chunk types, section mapping. Example: "406 sections; Abilities 107–111, Skills 113–129, Powers 143+, Combat 235–251."
- **Existing structure:** If output already exists: "these stories", "all these epics", "Epic 2 and its sub-epics".

#### 2b - Concept Tracking

Run `concept_tracker.py` to extract terms from chunks and build a cross-reference matrix. Required before foundational models — if not available, stop and report the error.

```bash
python scripts/concept_tracker.py seed --source <domain-model-or-wordlist>   # optional: seed glossary
python scripts/concept_tracker.py scan --context-path <context-path>
python scripts/concept_tracker.py report <terms_report.json> --min-units 5
```

**Output:** `terms_report.json` with per-unit terms, term index, cross-references by frequency, and co-occurrence clusters. Use the report to drive foundational model identification (§4).

#### 2c - Concept Deep Analysis

The concept tracker finds *what terms exist* and *where they co-occur*, but does NOT reveal mechanical variation. Before writing foundational models or variation analysis, deep-read the source chunks for each candidate model.

1. Use `term_index` from `terms_report.json` to find which chunks contain each candidate model's key terms
2. For each candidate model, read 3–5 representative chunks
3. Extract the mechanically distinct categories from the actual source text — not from memory
4. Record which sections were read and what categories were found

**Validation pass on "examples" annotations:** After drafting the scaffold, for every annotation that says "X are examples (same flow)," verify from source chunks that all items share the same interaction flow. The test: does the item change who rolls, what DC, what triggers the check, or what the outcome does? If yes — separate story, not example.

### 4 - Foundational Object Models

Using the concept tracker report and deep read pass (§3b), identify foundational models via OOAD (find objects, find collaborations, find repetition — see `pieces/domain.md` § Foundational Object Models for full process). Each model: State Model (typed concepts with properties, operations, collaborators) + Extensions (names only). Each model becomes a module in the domain model.

**Output:** Write to `<session>/domain-model.md` § Foundational Object Models (between `<!-- section: foundational_models -->` markers). Session §4 references the output file — do not duplicate models here. Auto-injected into `create_strategy` prompt.

### 5 - Variation Analysis

Per foundational model from §4, analyze what varies: what's consistent, what differs, what extends with new behavior (→ story) vs adds data to same behavior (→ example). Identify business rules, workflow differences, and state variations. See `pieces/interaction.md` § Variation Analysis for full process.

**Output:** Write to `<session>/interaction-tree.md` § Variation Analysis (between `<!-- section: variation_analysis -->` markers). Session §5 references the output file — do not duplicate analysis here. Auto-injected into `create_strategy` prompt.

### 6 - Interaction Scaffold

**Story vs Example rule:** Functionality that extends a foundational model with NEW BEHAVIOR requires a story (new operations, new state transitions, new validation rules). Adding DATA to the same behavior is just an example on an existing story. This is how you decide what becomes a story and what becomes an example.

Build the interaction tree on top of the foundational models:

- Epic/Sub-epic/Story breakdown
- Each sub-epic references which foundational model(s) it extends
- List ALL story names (lean format: name + parenthetical examples). The session scaffold identifies every story.
- Pattern-change boundaries (when does the pattern change? new epic? new sub-epic?)
- The scaffold lists names only — no Trigger, Response, Pre-Condition, or other fields. Those belong in the interaction-tree.md output file.

**Scaffold format:** Lean — epic name, story names with parenthetical examples, variation analysis rationale. List ALL story names so slices can be properly designed (you need the full picture to build vertical slices). 

### 7 - First-Cut Output Files

The scaffold phase produces the **first cut of the real output files** (`interaction-tree.md`, `domain-model.md`). These are not separate "scaffold files" — they ARE the deliverables at version 1. Runs expand them slice by slice.

The first cut uses pattern+extrapolation: 2-3 stories per epic in full detail (Trigger, Response, Pre-Condition, domain concepts), remaining stories listed by name only. Runs expand the named stories with full detail slice by slice.

**Validate first-cut outputs.** Session creation is run-0 — run `build.py validate` on `interaction-tree.md` and `domain-model.md` before session creation is done. Same rules, same scanners, same fix-before-marking-complete as any run. The session scaffold (§6) also gets the slice scanner (`session-slice-not-epic-by-epic`).

#### First Cut (by Session Type)


| Session Type      | First cut produces                                                                                                                           |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Discovery**     | `interaction-tree.md` (epics, 2-3 stories per epic in full; rest by pattern) + `domain-model.md` (concepts with properties and operations). |
| **Exploration**   | Steps added to existing stories in `interaction-tree.md`. Optionally domain updates.                                                         |
| **Specification** | Steps + Scenarios + Examples added to existing stories. May detail a couple of stories fully to establish pattern, then apply to rest.        |


### 8 - Slices

The order in which you work through slices is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

**DO NOT slice by epic.** If your slices map 1:1 to epics, you did it wrong. Each slice must build something AND use it — end-to-end. There is no value in building all of one epic's stories without proving they work by using them. Group build + use into categories and implement that way.

**Slicing checklist:**
- Does each slice build AND use something?
- Does any slice build things that aren't used until a later slice? If yes, restructure.
- Are slices ordered from simple to complex, layering on complexity?
- Does each slice prove the previous one works before adding the next layer?

A **slice** is a collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope for the run. Slices are stored in the session file; tick each when a run is done for it.

**Ideas:** Architectural slice, domain slice, integration slice, workflow slice, value slice, risk slice. Favour vertical slicing. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

**New session:** Slices can be carried over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

### 9 - Runs

One run per slice. See `pieces/runs.md` for run lifecycle, run log structure, corrections format, and patterns.
