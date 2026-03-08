# Validation Pass

<!-- section: story_synthesizer.validation.scope_run -->
## Scope: Validate Run

Validate **only the output of the current run**. Ignore previous work. Use when the user says "validate our run" or "check what we just did."

**Required:** Run `python scripts/build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. **Fix them before marking the run complete** — this is part of the build phase.

<!-- section: story_synthesizer.validation.scope_slice -->
## Scope: Validate Slice

Validate **everything in the slice** — all accumulated output for that slice. Use when the user says "validate the slice" or "validate slice 1."

**Required:** Run `python scripts/build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. **Fix them before marking the run complete** — this is part of the build phase.

<!-- section: story_synthesizer.validation.explicit_validate -->
## Explicit Validate (User Request Only)

When the user **explicitly asks to validate** (e.g. "validate", "run validation", "check the output") **outside a build phase** — do **not** fix violations. Run validate, report violations, and leave with the reviewer. Do not edit files in front of the user unless you are in a build phase (run_slice, validate_run, validate_slice).

<!-- section: story_synthesizer.validation.checklist -->
## Validation Checklist

After generating interactions and concepts, verify against the output format in `output/interaction-tree-output.md` and `output/state-model-output.md`.

**Run scanners:** Execute `python scripts/build.py validate` (or `validate <path>`) to run rule-based scanners on the interaction tree and state model. Scanners use regex and native Python only (or grammar/AST when available). When in a build phase (run_slice, validate_run, validate_slice), fix any reported violations before considering the run complete. When the user explicitly asks to validate outside a build phase, report violations only — do not fix.

**Strategy alignment:** Check that nodes include the fields specified by the strategy's **Comprehensiveness Criteria** for the current mode (Shaping, Discovery, Exploration, Walkthrough, Specification). The strategy states which mode(s) apply and what is in scope — e.g. Discovery expects Pre-Condition, Initiating-State, Resulting-State, Initiation, Response; Specification expects Examples, scenarios, failure conditions. Do not require fields that are out of scope for the run.

---

## Interaction Tree

**Epic**
- [ ] Heading: `# Epic: <name using **Domain Concepts**> (<statement>)`
- [ ] Initiating-Actor, Responding-Actor, Pre-Condition, Examples present (or inherited)
- [ ] Pre-Condition on parent only when shared; children list only new or specialized state
- [ ] Examples: state table block or `Examples: [Table Name 1, ...]` when inherited

**Story**
- [ ] Heading: `### Story: <name using **Domain Concepts**> (<statement>)`
- [ ] Pre-Condition, Failure-Modes (max 3), Initiation, Response present
- [ ] Initiation: sub-bullets Initiating-Actor, Behavior (no state language in Behavior)
- [ ] Response: sub-bullets Responding-Actor, Behavior (no action language in outcome)
- [ ] Scenario and Steps when in scope

**Step**
- [ ] `- Step N: <name using **Domain Concepts**> (When/Then <statement>)`
- [ ] Initiation and Response with [inherited] when from parent
- [ ] System-initiated steps override Initiating-Actor to [System]

**Example tables**
- [ ] Qualifier in parentheses: `ConceptName (qualifier):`
- [ ] Scenario column required on entity tables; kebab-case (e.g. success, invalid-details)
- [ ] Each table: label, blank line, header row, separator row, data rows

**Hierarchy and order**
- [ ] Epic → Epic/Story → Scenario → Step (epics can nest)
- [ ] Required state creators appear before consumers; tree follows actual flow
- [ ] Each node touches at least one domain concept via `**Concept**` in labels

---

## State Model

**Concept**
- [ ] Format: `Concept : <Base Concept if any>`
- [ ] Properties, operations, collaborating concepts listed
- [ ] `examples:` list of state concept tables from interaction tree
- [ ] Each concept referenced via `**Concept**` in interaction tree must exist here
- [ ] Concepts scoped to Epic/Story that owns it (lowest common ancestor of all interactions that use it)
- [ ] Stories rarely define domain concepts — they inherit from epic
- [ ] Invariants under specific property/operation when they apply to that property/operation only

---

## Failure Modes

- [ ] Max 3 per interaction
- [ ] From domain rules, state conditions, or authorization only (no infrastructure or technical failures)

---

## Content

- [ ] No implementation details (APIs, services, databases, UI components, code)
- [ ] No speculation beyond the provided material
- [ ] Everything at logical/domain level
- [ ] Assumptions stated when unclear (no invented mechanics)
- [ ] **Granularity:** Sufficient stories to capture rule detail; no collapsing of large sections into single stories

---

## Corrections Format

When adding corrections to the run log, use the format from `strategy.md`:

- **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix

If failing on the same guidance again, add an extra example to the existing DO/DO NOT block.
