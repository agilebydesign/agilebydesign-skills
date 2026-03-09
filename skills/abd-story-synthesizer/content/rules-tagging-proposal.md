# Rules Tagging Proposal for abd-story-synthesizer

**Tags do everything.** The strategy declares which tags are in scope. Include a rule if any of its tags matches any in-scope tag. No distinction between mode and component — declare tags by mode, by component, or explicitly.

**Tag set:**

| Tag | Description |
|-----|-------------|
| `shaping` | Coarse structure; epics and stories; names and actors only |
| `discovery` | Story-level detail: Initiation, Response, Pre-Condition, Initiating-State, Resulting-State |
| `exploration` | Steps below story; linear, no edge cases |
| `walkthrough` | Domain walkthrough on stories |
| `specification` | Steps, scenarios, examples, failure modes |
| `interaction_tree` | Epic/Story hierarchy; names, actors, constraints |
| `story` | Story-level fields: Initiation, Response, Pre-Condition, etc. |
| `domain` | Domain Model — concepts, Properties, Operations |
| `step` | Atomic Initiation/Response; When/Then or verb-noun |
| `step_edge_case` | Steps + Failure-Modes; error paths |
| `example` | Example tables per concept |
| `scenario` | Step grouping by path |

**Filtering:** Strategy declares `tags: [tag1, tag2, ...]`. Include rule if `rule.tags ∩ strategy.tags ≠ ∅`.

**When no strategy or new pattern:** Default to `tags: [shaping, discovery, interaction_tree, story, domain]`

---

## 1. abd-story-synthesizer rules (current — self-contained)

These are the `.md` rules in `rules/`. They are currently shaping-focused.

| Rule | Current | Proposed for synthesizer | Tags |
|------|---------|--------------------------|------|
| **context-derive-from-source** | Derive from source; don't invent | Same — applies to all synthesis | interaction_tree, story, step, scenario, example, domain |
| **context-speculation-assumptions** | State assumptions when unclear; don't speculate | Same — applies to all synthesis | interaction_tree, story, step, scenario, example, domain |
| **hierarchy-parent-granularity** | Parent at appropriate granularity; don't leak child detail | Same — applies to hierarchy | interaction_tree |
| **hierarchy-sequential-order** | Sequential order; creators before consumers | Same — applies to tree ordering | interaction_tree |
| **hierarchy-story-granularity** | Break down by distinct requirements; sufficient stories | Same — applies when stories are in scope | story |
| **interactions-inheritance-pre-condition** | Pre-Condition on parent only; inheritance; promote shared to parent; child lists only new or unique | Same — applies whenever Pre-Condition is in scope | interaction_tree, story |
| **interactions-inheritance-domain-concepts** | Scope concepts to Epic/Story; declare at lowest common ancestor; stories inherit from epic; place at most specific level where relevant | Same — applies whenever domain concepts are in scope. Merges scope_concepts_correctly. Use Domain Model format for concept examples (Properties, Operations), not CRC format. | interaction_tree, story, domain |
| **interactions-inheritance-resulting-state** | Resulting-State inheritance; outcome language at Epic level; shared on parent, child-specific on child | Same — applies when Resulting-State is in scope | interaction_tree, story |
| **interactions-inheritance-actors** | Initiating-Actor, Responding-Actor inherited; use [User], [System] at every initiation/response | Same — applies when Initiation/Response in scope | interaction_tree, story, step |
| **interactions-inheritance-examples** | Examples live on interaction; use [inherited] when tables come from parent | Same — applies when Examples in scope | interaction_tree, story, step, scenario |
| **interactions-inheritance-initiating-state** | Initiating-State qualifies interaction; Epic holds rules that apply to all children | Same — applies when Initiating-State in scope | interaction_tree, stories |
| **interaction-failure-modes** | Max 3; domain/state/authorization only | Same — applies when Failure-Modes are in scope | story, step_edge_case |
| **interaction-supporting-actor-response** | Supporting = system; coarse Epic Response | Same — applies when Initiation/Response in scope | interaction_tree, story, step |
| **state-logical-domain-level** | Logical/domain level; no implementation | Same — applies to all synthesis | interaction_tree, story, step, scenario, example, domain |
| **state-synchronize-concepts** | Full workflow: interactions → concepts → Domain Model → inline Concepts | Same — applies when Domain Model is in scope | interaction_tree, story, domain |
| **verb-noun-format** | Verb-noun for names and steps; active voice; base verb forms; business/behavioral language; no technical terms | From shape + exploration; merged with active_business_and_behavioral_language, use_verb_noun_format_for_story_elements, behavioral_ac_at_story_level. Applies to all nodes. | interaction_tree, story, step, scenario |
| **small-and-testable** | Stories testable, deliverable; story vs step distinction | From shape; story = testable outcome, step = implementation detail | story, step |
| **outcome-oriented-language** | Outcomes over mechanisms; artifacts over "visualizing" | From shape; applies to naming and Initiation/Response | interaction_tree, story, step |
| **ensure-vertical-slices** | Vertical slices; end-to-end flows | From shape; applies when slice design is in scope | interaction_tree |

---

## 2. story_bot shape rules (JSON)

These are in `agile_bots/bots/story_bot/behaviors/shape/rules/`. Many are shaping-specific.

| Rule | Current | Proposed for synthesizer | Tags |
|------|---------|--------------------------|------|
| **verb_noun_format** | Actor → verb noun; actor in metadata; active voice; base verb forms; business language | Adapt: Use verb-noun for epic/story/step names. Actor documented separately. Active voice, base verb forms, business language for all interaction text. (Merges active_business_and_behavioral_language.) | interaction_tree, story, step |
| **small_and_testable** | Stories testable, deliverable; story vs step distinction | Adapt: Story = testable outcome; step = implementation detail. Apply when stories or steps in scope. | story, step |
| **outcome_oriented_language** | Outcomes over mechanisms; artifacts over "visualizing" | Same — applies to naming and Initiation/Response | interaction_tree, story, step |
| **enumerate_all_stories_explicitly** | List all stories for focus increment; no ~X notation | **Skip or scope:** Synthesizer doesn't do increments. If we add increment support, tag `stories`. | — |
| **ensure_vertical_slices** | Vertical slices; end-to-end flows | **Skip or scope:** Synthesizer slices are strategy-defined. Could tag `interaction_tree` if slice design is in scope. | interaction_tree |
| ~~**active_business_and_behavioral_language**~~ | Active voice; base verb forms; business language | **Merge:** Merged into verb_noun_format. | — |
| ~~**scale_story_map_by_domain**~~ | Domain first, operation second; break out by domain | **Remove:** Not recommended for synthesizer. | — |
| ~~**valuable**~~ | Stories capture discrete behavior describable in system/business terms | **Remove:** Not recommended for synthesizer. | — |
| ~~**consolidate_superficial_stories**~~ | Consolidate stories that differ only in data values | **Remove:** Handled in identification criteria. | — |
| ~~**review_and_expand_stories**~~ | Break down stories into component interactions when System/Technology approach | **Remove:** Part of identification criteria. | — |
| **instructions_quality** | Instruction quality across bot chain | **Skip:** Bot-specific; not synthesis content. | — |
| **rule_change_impact** | Baseline for rule changes | **Skip:** Validation tooling; not a synthesis rule. | — |

---

## 3. story_bot exploration rules (JSON)

These apply to steps. In the old rules, "AC" (acceptance criteria) was just steps — no different.

| Rule | Current | Proposed for synthesizer | Tags |
|------|---------|--------------------------|------|
| ~~**use_verb_noun_format_for_story_elements**~~ | Verb-noun for scenarios and steps | **Merge:** Merged into verb-noun-format (expanded scope to scenario). | — |
| **use_atomic_acceptance_criteria** | Atomic steps; state general once, variations only what differs | Same — applies when steps or Failure-Modes in scope | stories, steps, steps_edge_cases |
| **use-and-and-but-for-conditions** | And for multiple reactions; But for negative conditions | **Merge:** Merges use_and_for_multiple_reactions and use_but_for_negative_conditions. Same — applies to Initiation/Response and steps | steps, scenarios |
| **use_channel_specific_language** | Channel-specific: Domain/API, CLI, Panel | **Consider:** Synthesizer is domain-agnostic. Could tag `steps`, `scenarios` if channel is in strategy. | steps, scenarios |
| **hierarchy-approximately-4-to-9-children** | Any node has ~4–9 children; for stories count steps (not scenarios) | **Adapt:** Replaces stories_have_4_to_9_acceptance_criteria. Applies to epic, story, scenario — not steps. | interaction_tree, stories, scenarios |
| ~~**enumerate_all_ac_permutations**~~ | Enumerate step permutations explicitly | **Remove:** Content moved to Identification Criteria (Steps — Enumerate all permutations). | — |
| ~~**behavioral_ac_at_story_level**~~ | Steps at story level, behavioral | **Merge:** Merged into verb-noun-format (behavioral language, no technical terms). Applies to all nodes. | — |
| **alternate_actors_in_steps** | Alternate actors in steps for clarity | Same — applies to steps | steps |
| **keep_acceptance_criteria_consistent_across_connected_domains** | Steps consistent across connected domains; parallel structure and depth | Same — applies when multiple domains. Merges keep_scenarios_consistent_across_connected_domains: parallel scenario structures, consistent depth, parameterize near-duplicates with {Concept} instead of duplicating. | steps, scenarios |

---

## 4. story_bot scenarios rules (JSON)

These apply to scenarios and example tables.

| Rule | Current | Proposed for synthesizer | Tags |
|------|---------|--------------------------|------|
| **write_concrete_scenarios** | **Concept** notation; example tables per interaction (Pre-Condition, Initiation, Response, Steps); format per core.md and output/interaction-tree-output.md — Qualifier Concept (qualifier), scenario column required (kebab-case), `===` between tables | Same — applies when scenarios and examples in scope | scenarios, examples |
| **example_tables_use_domain_language** | One-to-one mapping: example tables and columns must match domain concepts and their fields exactly — no drift. Table columns map to scenario parameters. Domain terminology; omit IDs. Use concrete examples in format per core/output — no placeholder or symbolic notation. (Merges map_table_columns_to_scenario_parameters.) | Same — applies when examples in scope | examples, domain, scenarios |
| ~~**scenario_language_matches_domain**~~ | Given/When/Then use domain concepts, not UI | **Merge:** Merged into verb-noun-format (domain concepts in steps, not UI labels). Applies to steps in or out of scenarios. | — |
| **given_describes_state_not_actions** | All state fields (Pre-Condition, Initiating-State, Resulting-State) describe concepts with qualifier — not events or actions. Given = state; When = first action. | Same — applies whenever state fields are in scope | interaction_tree, story, step, scenario |
| **scenarios_on_story_docs** | Scenarios in story-graph.json, not separate files | **Skip:** Synthesizer output format is Interaction Tree + Domain Model (markdown), not story-graph.json. | — |
| **scenarios_cover_all_cases** | Happy path, edge cases, error cases | Same — applies when scenarios in scope | scenarios |
| ~~**map_table_columns_to_scenario_parameters**~~ | Table columns map to scenario parameters | **Merge:** Merged into example_tables_use_domain_language (columns match domain fields; map to scenario parameters). | — |
| **background_vs_scenario_setup** | Shared setup = Pre-Condition with Examples at story level; scenarios below inherit. Use Given/And only (state, not actions); **Concept** notation. Example: Story has `Pre-Condition: Given **User** is logged in; And **User** has active **Session**` with Examples (Logged In User, Active Session tables); each Scenario shows `Pre-Condition: [Given **User** is logged in; And ...]` and `Examples: [Logged In User, Active Session]`. | Same — applies when scenarios share setup | stories, scenarios, examples |
| ~~**use_scenario_outline_when_needed**~~ | Scenario Outline for formulas, domain entities, data variations | **Remove:** Strategy explicitly declares whether examples are in scope for a run. No separate rule needed. | — |
| ~~**keep_scenarios_consistent_across_connected_domains**~~ | Parallel scenario structures across domains; consistent depth | **Merge:** Merged into keep_acceptance_criteria_consistent_across_connected_domains (same rule — applies when multiple domains in scope). | — |

---

## 5. CRC bot domain rules (JSON)

These apply to domain concepts (Domain Model).

| Rule | Current | Proposed for synthesizer | Tags |
|------|---------|--------------------------|------|
| **use_domain_language** | Domain-specific language; no Hold/Get/Has; mine from stories | Same — applies to Domain Model and `**Concept**` in interactions | domain |
| **use_resource_oriented_design** | Concepts as resources; properties and behaviors | Same — applies to Domain Model | domain |
| **favor_atomic_responsibilities** | One responsibility = one behavior; verb phrases | Same — applies to Domain Model | domain |
| **map_bidirectional_collaborators** | Bidirectional collaborator mapping | Same — applies to Domain Model | domain |
| **integrate_and_organize_concepts** | Integrate and organize concepts | Same — applies to Domain Model | domain |
| ~~**scope_concepts_correctly**~~ | Scope concepts to appropriate level | **Merge:** Merged into interactions-inheritance-domain-concepts. Use Domain Model format (Properties, Operations) for examples — not CRC class-responsibility-card format. | — |
| **use_natural_english** | Natural English for responsibilities | Same — applies to Domain Model | domain |
| **use_module_for_folder_structure** | Module for folder structure | **Skip:** Code-structure specific; not synthesis content. | — |
| **favor_code_representation** | Favor code representation | **Skip:** Design/implementation specific. | — |
| **shape_relationships_from_story_map** | Shape relationships from story map | **Consider:** Could apply when deriving Domain Model from interactions | domain |

**Naming:** CRC's `use_domain_language` and synthesizer's `verb-noun-format` both touch naming. For synthesizer:
- **Epic/Story/Step names:** verb-noun (from shape)
- **Domain concept names:** domain language, no Manager/Service (from CRC)
- **Example table headers:** domain terminology (from scenarios)

**Domain Model examples:** Use Domain Concept format (Properties, Operations, Module) — not CRC class-responsibility-card format (responsibilities + collaborators). See `core.md` Domain Concept and `output/domain-model-output.md`.

---

## 6. Summary: Tag distribution

| Tag | Rules |
|-----|-------|
| **interaction_tree** | context-derive-from-source, context-speculation-assumptions, hierarchy-parent-granularity, hierarchy-sequential-order, hierarchy-approximately-4-to-9-children, interactions-inheritance-pre-condition, interactions-inheritance-domain-concepts, interactions-inheritance-resulting-state, interactions-inheritance-actors, interactions-inheritance-examples, interactions-inheritance-initiating-state, interaction-supporting-actor-response, state-logical-domain-level, state-synchronize-concepts, verb-noun-format, outcome-oriented-language, ensure-vertical-slices, given_describes_state_not_actions |
| **stories** | (same as interaction_tree) + hierarchy-story-granularity, interaction-failure-modes, small-and-testable, use_atomic_acceptance_criteria, background_vs_scenario_setup |
| **steps** | context-derive-from-source, context-speculation-assumptions, interaction-supporting-actor-response, state-logical-domain-level, verb-noun-format, small-and-testable, outcome-oriented-language, use_atomic_acceptance_criteria, use-and-and-but-for-conditions, alternate_actors_in_steps, keep_acceptance_criteria_consistent_across_connected_domains, given_describes_state_not_actions |
| **steps_edge_cases** | interaction-failure-modes, use_atomic_acceptance_criteria |
| **scenarios** | context-derive-from-source, context-speculation-assumptions, state-logical-domain-level, interactions-inheritance-examples, hierarchy-approximately-4-to-9-children, verb-noun-format, use_atomic_acceptance_criteria, use-and-and-but-for-conditions, write_concrete_scenarios, given_describes_state_not_actions, scenarios_cover_all_cases, example_tables_use_domain_language, background_vs_scenario_setup, keep_acceptance_criteria_consistent_across_connected_domains |
| **examples** | context-derive-from-source, context-speculation-assumptions, state-logical-domain-level, write_concrete_scenarios, example_tables_use_domain_language, background_vs_scenario_setup |
| **domain** | context-derive-from-source, context-speculation-assumptions, interactions-inheritance-domain-concepts, state-synchronize-concepts, example_tables_use_domain_language, use_domain_language, use_resource_oriented_design, favor_atomic_responsibilities, map_bidirectional_collaborators, integrate_and_organize_concepts, use_natural_english, shape_relationships_from_story_map |

---

## 7. Implementation notes

1. **Rule format:** Synthesizer uses `.md` rules. Story bot and CRC bot use `.json` with scanners. For synthesizer: keep `.md` and add YAML frontmatter with `tags: [epic, story, ...]`.

2. **Filtering:** When assembling instructions for an operation, filter rules by the strategy's in-scope components. Include rules whose tags match any in-scope component. **Quick filtering** for minimal scope: if strategy says "just discovery" (or similar), include only rules tagged for that scope (e.g. `interaction_tree`, `stories`, `domain`) — no `steps`, `scenarios`, `examples`. E.g. Shaping → `interaction_tree`, `domain`; Discovery → `interaction_tree`, `stories`, `domain`; Specification → `steps`, `steps_edge_cases`, `scenarios`, `examples`.

3. **Strategy declares components:** The strategy's "What We Are Synthesizing" (section 0) and Comprehensiveness Criteria declare which components are in scope: `interaction_tree`, `stories`, `domain`, `steps`, `steps_edge_cases`, `examples`, `scenarios`. **Bespoke strategies** are supported: a custom strategy can mix components (e.g. initial discovery + mapping to stories + domain concepts + basic examples). Examples can be scoped at different levels — e.g. sub-epic level vs story or step level — the strategy defines where. The engine reads the strategy and includes rules whose tags match the declared components.

4. **Skipped rules:** `instructions_quality`, `rule_change_impact`, `scenarios_on_story_docs`, `enumerate_all_stories_explicitly`, `use_module_for_folder_structure`, `favor_code_representation`, `use_scenario_outline_when_needed` — bot-specific, output-format-specific, code-structure-specific, or redundant (strategy declares examples in scope). Not applicable to synthesizer. **Merged:** `keep_scenarios_consistent_across_connected_domains` → `keep_acceptance_criteria_consistent_across_connected_domains`; `scope_concepts_correctly` → `interactions-inheritance-domain-concepts` (use Domain Model format for concept examples, not CRC format). **Rule format:** Add YAML frontmatter with `tags: [interaction_tree, story, ...]` to each rule file.

5. **CRC design vs walkthrough:** There is no CRC design in the synthesizer — rules like `respect_existing_delegation`, `object_creation_and_selection`, `place_at_lowest_level`, `encapsulate_through_properties` apply to design refinement and are omitted. We will include CRC walkthrough rules. Walkthrough rules could be modeled as interactions; that is deferred for now.
