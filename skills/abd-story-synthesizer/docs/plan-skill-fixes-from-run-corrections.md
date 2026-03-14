---
name: Skill Fixes from Run Corrections
overview: Analyze corrections in run-0.md and run-1.md, extract domain-neutral fixes, and propose concrete changes to the abd-story-synthesizer skill (rules, pieces, process, checklists) so the same mistakes do not recur when using the skill on any domain.
todos: []
isProject: false
---

# Skill Fixes from Run-0 and Run-1 Corrections

## Analysis Summary

The run logs document 13 distinct corrections (5 from run-0, 8 from run-1). Each is abstracted to a **domain-neutral principle** and mapped to a **skill component** to update. All proposed skill changes use generic terms (Entity, Trait, Resource, Validation, Outcome, Effect, acquisition, tier, modifier source) — no MM3E or workspace-specific concepts.

---

## Run-0 Corrections (Session / Strategy Creation)

### R0-1: Slices too large

**Mistake:** One slice per major subsystem is too big for review and iteration.

**Domain-neutral principle:** Do not propose slices that absorb too many workflows. Split into smaller slices, each one coherent workflow.

**Skill fix:** Create rule [rules/context-slice-size.md](rules/context-slice-size.md) with `tags: [session, slices]`:

- **DO NOT** propose slices that are too large — one slice per major subsystem is too big. Each slice must be small enough to review and iterate in one pass.
- Slice checklist item: "Is the slice small enough to review and iterate? (If it covers an entire build/creation flow, split it.)"

---

### R0-2: Slices organized like modules/epics

**Mistake:** Organizing slices like modules (Campaign Setup, Character Creation, Combat) hides cross-cutting flows.

**Domain-neutral principle:** Slices must cross the solution and show how the system ties together across functional areas. Do not organize slices like modules or epics.

**Skill fix:** Create rule [rules/context-slice-cross-cutting.md](rules/context-slice-cross-cutting.md) with `tags: [session, slices]`:

- **DO NOT** organize slices like modules or epics. Each slice must cross the solution and show how key business logic, structure, and state tie together across functional areas.
- Slice checklist item: "Does the slice cross the solution (not just one subsystem)? Does it answer: *What key business logic, structure, state can we model, and build on later?*"

---

### R0-3: Non-core stuff last

**Mistake:** Putting setup/config first delays discovery of core mechanics.

**Domain-neutral principle:** Core mechanics first; peripheral concerns (setup, config) last.

**Skill fix:** Create rule [rules/session-slice-ordering.md](rules/session-slice-ordering.md) with `tags: [session, slices]`:

- **DO** order slices by importance to core mechanics. Put core resolution/flow first; setup, config, and peripheral concerns last.
- Slice checklist item: "Is slice order correct? (Core mechanics first; setup/config last.)"

---

### R0-4: Behavior packet adequacy

**Mistake:** Minimal packet ("target rolls resistance, map degree to condition") omits structural details needed to build the model.

**Domain-neutral principle:** Ensure behavior packets are adequate before building the model. A minimal packet is insufficient. The packet must specify: structural details, flow direction, composition rules, state transitions, and cross-cutting patterns.

**Skill fix:** Add to [pieces/process.md](pieces/process.md) Model Discovery and Model Assessment (no new rule):

- In Model Discovery: "Packets must specify enough structure to build the model — concepts, flow (who creates what, who receives), and any mapping/composition rules the domain needs. Do not use a minimal one-liner."
- In Model Assessment: "Verify behavior packets are adequate before Phase 7. If packets are minimal, reject and redo discovery."

---

### R0-5: Epics not named after slices

**Mistake:** Naming epic "Bare Bones Mechanics" (the slice name) conflates slice with epic and hides functional structure.

**Domain-neutral principle:** Do not name interaction-tree epics after slices. Epics and sub-epics come from goal, domain, concept map, evidence — they are functional. Populate stories for the current slice; estimate/placeholder the remainder.

**Skill fix:** Do both:

1. Add to [pieces/interaction.md](pieces/interaction.md): **DO NOT** name epics after slices. Epics and sub-epics come from the larger context (goal, domain, concept map, evidence) — they are functional. Place slice stories under appropriate sub-epics. Mark remainder as estimated.
2. Create rule [rules/interaction-epics-from-context.md](rules/interaction-epics-from-context.md) with the same content.
3. Reference this in [pieces/session.md](pieces/session.md) and [pieces/runs.md](pieces/runs.md).

---

## Rules and Session Wiring

Slice rules (R0-1, R0-2, R0-3, R1-3) live in separate rule files and **guide** session creation and **validate** output. session.md references them; rules are loaded via `get_instructions create_strategy`. Same approach as run_slice — no special logic.

**Wire rules into create_strategy (same as run_slice):**

- Add `story_synthesizer.validation.rules` to `create_strategy` in [skill-config.json](skill-config.json). Run_slice and validate_slice already use this section; create_strategy gets rules the same way. No changes to [scripts/instructions.py](scripts/instructions.py) — the existing `.rules` path loads all rules.

**Validate output after session creation:**

- Add `validate_session` operation to skill-config.json (sections: session, validation.rules, validation.checklist — same pattern as validate_slice).
- In instructions.py, add `validate_session` to the operations that receive the strategy document (alongside generate_slice, run_slice, improve_strategy) so the AI can compare slices to rules.
- Add to [pieces/process.md](pieces/process.md) Phase 5: "After creating strategy, run `get_instructions validate_session` and validate slices against slice rules before running any slice."
- Add to [pieces/session_checklist_template.md](pieces/session_checklist_template.md): "Validate slices against slice rules (`get_instructions validate_session`)."

**session.md:** Add reference to slice rules: "Apply slice rules when designing slices. Run `get_instructions create_strategy` to load rules. After creating strategy, run `get_instructions validate_session` to validate slices."

---

## Run-1 Corrections (Slice Execution)

### R1-1: Don't skip Phase 6

**Mistake:** Jumping to Phase 7 (interaction tree + domain model) without Phase 6 (model_discovery, model_validation).

**Domain-neutral principle:** Phase 6 (Model Discovery and Assessment) is mandatory before Phase 7. Do not produce interaction tree or domain model without OOAD analysis and validation.

**Skill fix:** Strengthen [pieces/process.md](pieces/process.md) Phase 6 and 7:

- Add **CRITICAL** callout before Phase 7: "Do NOT run Phase 7 until Phase 6 is complete. Phase 6 produces OOAD analysis and validated model. Skipping produces a model that misses mechanisms, ownership, and validation."
- Add to [pieces/run_checklist_template.md](pieces/run_checklist_template.md): Note that steps 1–11 must complete before step 12; do not skip.

---

### R1-2: Don't truncate Model Assessment

**Mistake:** OOAD with only happy-path walkthrough and one-line anemia note.

**Domain-neutral principle:** Model Assessment must include: (1) scenario/message walkthrough for happy path, error path, edge case, stateful repetition, alternate variation, recovery where relevant; (2) anemia/centralization critique against all issue types; (3) base and inheritance check. Persist full assessment in run-N-ooad.md.

**Skill fix:** Strengthen [rules/domain-model-validation-scenario-walkthrough.md](rules/domain-model-validation-scenario-walkthrough.md) and [rules/domain-model-validation-anemia-critique.md](rules/domain-model-validation-anemia-critique.md):

- Add explicit **DO NOT** truncate. Full Model Assessment: multiple scenario walkthroughs with message flow, explicit anemia critique table, base/inheritance verdict. All in run-N-ooad.md.
- Add to [pieces/process.md](pieces/process.md) Model Assessment: "Persist the full assessment. A one-line note is insufficient."

---

### R1-3: Include foundation in early slices

**Mistake:** Deferring purchase/acquisition to a later slice when the first slice's core flow depends on it.

**Domain-neutral principle:** Early slices must include the foundational setup or prerequisites needed to engage with the solution. If the core flow depends on concepts that are created, configured, or allocated first, include that flow in the early slice. Do not defer to a later slice.

**Skill fix:** Create rule [rules/context-slice-foundation-inclusion.md](rules/context-slice-foundation-inclusion.md) with `tags: [session, slices]`:

- **DO** include foundational setup in early slices when the core flow depends on it. Examples: product setup, account creation, user onboarding, configuration before core use. If the solution requires something to exist or be configured before the main flow runs, the first slice must model that.
- **DO NOT** defer foundational setup to a later slice when the first slice's flow is under-specified without it.

---

### R1-5: Introduce shared base when concepts share protocol

**Mistake:** Deferring "consider base in future refinement" when concepts share protocol now.

**Domain-neutral principle:** When concepts share protocol (modifier, cost, acquisition, validation role), introduce a shared base in the current slice. Do not defer to future refinement.

**Skill fix:** Strengthen [rules/domain-model-validation-base-inheritance.md](rules/domain-model-validation-base-inheritance.md):

- Add **DO NOT** defer when shared protocol exists now. "Consider base in future refinement" is wrong when concepts share modifier, cost, acquisition, and validation role in the current slice.
- Add: Introduce base when the role is the same and variation is in implementation. Do not defer.

---

### R1-6: Create and update checklists via CLI

**Mistake:** Running phases without creating or updating checklists.

**Domain-neutral principle:** Each stage has a checklist. Create from template at stage start; update Done column when steps complete. Use the checklist CLI — do not rely on manual copy.

**Skill fix:**

1. **Create [scripts/create-checklist.py](scripts/create-checklist.py):**
   - `create-checklist overall` — creates `overall-context-checklist.md` from template
   - `create-checklist session <name>` — creates `<session>/session-checklist.md`
   - `create-checklist run <session> <n>` — creates `<session>/runs/run-N-checklist.md`
   - `create-checklist update <path> --step <n>` — marks step N done (☐ → ☑) in the checklist file

2. **Update [pieces/process.md](pieces/process.md):**
   - Replace "Copy X to Y" with "Run `create-checklist overall`" (and session/run equivalents)
   - Add **CRITICAL**: "Create checklist when starting: `create-checklist [overall|session|run]`. Update when step completes: `create-checklist update <path> --step N` or edit the file. A change is not tracked until the checklist is updated."

---

### R1-7: Pass objects not raw values

**Mistake:** Passing raw derived values (e.g. modifier) instead of the source object. Breaks encapsulation.

**Domain-neutral principle:** Do not pass raw derived values when the source object is available. The source owns creation; the created object receives the source and derives the value internally.

**Skill fix:** Add to [rules/domain-ooa-self-managing-parts.md](rules/domain-ooa-self-managing-parts.md) or new rule [rules/domain-ooa-traverse-from-root.md](rules/domain-ooa-traverse-from-root.md):

- **DO** traverse from root. The source owns creation; the created object receives the source and derives the value internally. Do not pass raw derived values.
- **DO NOT** pass raw values when the source object is available. Example (wrong): `validation.resolve(source.value)`. Example (correct): `source.create_validation(dc)` then `validation.resolve()` — validation gets value from source internally.

---

### R1-9: Model instances, not smashed properties

**Mistake:** Taking a complex object with multiple concepts and smashing them together into a single property or method.

**Domain-neutral principle:** When a concept has multiple related parts or relationships, consider whether it is best represented as instances/examples (objects in a diagram) or as a table of concepts with relationships — not as a single property or method that collapses the structure.

**Skill fix:** Create rule [rules/domain-ooa-model-instances-not-smashed.md](rules/domain-ooa-model-instances-not-smashed.md):

- **DO** consider when a concept is best represented as instances/examples (objects in diagram) vs smashing it into a property or method.
- **DO** model context with tables as one or more concepts with relationships.
- **DO** model instances and examples explicitly when structure matters.
- **DO NOT** smash complex objects with multiple concepts into a single property or method.

---

## Files to Create or Modify


| Action | File |
| ------ | ---- |
| Modify | [pieces/session.md](pieces/session.md) — Add slice rules reference |
| Modify | [pieces/process.md](pieces/process.md) — R1-1, R1-2, R1-6; add validate_session step in Phase 5 |
| Modify | [pieces/run_checklist_template.md](pieces/run_checklist_template.md) — R1-1 |
| Modify | [pieces/session_checklist_template.md](pieces/session_checklist_template.md) — Add validate slices step |
| Modify | [pieces/interaction.md](pieces/interaction.md) — R0-5 |
| Modify | [scripts/instructions.py](scripts/instructions.py) — Add validate_session to operations that receive strategy document |
| Create | [scripts/create-checklist.py](scripts/create-checklist.py) — R1-6: create overall/session/run, update --step |
| Modify | [skill-config.json](skill-config.json) — Add validation.rules to create_strategy; add validate_session operation (session, validation.rules, validation.checklist) |
| Modify | [rules/domain-model-validation-scenario-walkthrough.md](rules/domain-model-validation-scenario-walkthrough.md) — R1-2 |
| Modify | [rules/domain-model-validation-anemia-critique.md](rules/domain-model-validation-anemia-critique.md) — R1-2 |
| Modify | [rules/domain-model-validation-base-inheritance.md](rules/domain-model-validation-base-inheritance.md) — R1-5 |
| Modify | [rules/domain-ooa-self-managing-parts.md](rules/domain-ooa-self-managing-parts.md) — R1-7 |
| Modify | [rules/README.md](rules/README.md) — Document session, slices tags |
| Create | [rules/context-slice-size.md](rules/context-slice-size.md) — R0-1, tags: [session, slices] |
| Create | [rules/context-slice-cross-cutting.md](rules/context-slice-cross-cutting.md) — R0-2, tags: [session, slices] |
| Create | [rules/session-slice-ordering.md](rules/session-slice-ordering.md) — R0-3, tags: [session, slices] |
| Create | [rules/interaction-epics-from-context.md](rules/interaction-epics-from-context.md) — R0-5 |
| Create | [rules/context-slice-foundation-inclusion.md](rules/context-slice-foundation-inclusion.md) — R1-3, tags: [session, slices] |
| Create | [rules/domain-ooa-traverse-from-root.md](rules/domain-ooa-traverse-from-root.md) — R1-7 |
| Create | [rules/domain-ooa-model-instances-not-smashed.md](rules/domain-ooa-model-instances-not-smashed.md) — R1-9 |


---

## Execution Order

1. Create slice rules (context-slice-size, context-slice-cross-cutting, session-slice-ordering, context-slice-foundation-inclusion) with tags [session, slices]
2. Add validation.rules to create_strategy and add validate_session operation in skill-config.json; add validate_session to strategy-injection list in instructions.py
3. Create remaining new rules (interaction-epics-from-context, domain-ooa-*)
4. Modify existing rules (domain-model-validation-*, domain-ooa-self-managing-parts)
5. Modify pieces (session.md, process.md, run_checklist_template.md, session_checklist_template.md, interaction.md); create create-checklist.py
6. Update rules README (session, slices tags)
7. Rebuild AGENTS.md: `python scripts/build.py`

---

## Domain-Neutral Guarantee

All new and modified content uses only generic terms: Entity, Trait, Resource, Validation, Outcome, Effect, Source, acquisition, tier, modifier, instance, concept, relationship. No MM3E concepts (Character, Ability, Defense, Condition, PowerPoint, etc.) appear in the skill. Run logs (run-0.md, run-1.md) remain unchanged — they document what happened in that workspace.
