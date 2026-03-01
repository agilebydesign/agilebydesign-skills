# Shaping Process

The shaping process follows this flow. **Use this checklist** — do not skip steps.

## Process Checklist

- [ ] **Strategy Phase complete** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `story/<domain>-shaping-strategy.md`
- [ ] **Strategy approved by user** — Do not produce an interaction tree until then
- [ ] **Slice 1 produced** — 4–7 stories for the first slice
- [ ] **Slice 1 approved** — User reviews; corrections → add DO/DO NOT to strategy; re-run until approved
- [ ] **Next slice** — Proceed to next slice; repeat until all slices done
- [ ] **Post-shaping review** — Review all corrections; determine what needs to change in rules/instructions

## Flow

1. **Strategy** — Come up with a strategy (Epic/Story breakdown, slice order, assumptions).
2. **Validate strategy up front** — Review and refine the strategy until it looks reasonable. Do not produce an interaction tree until the strategy is approved.
3. **Run first slice** — Produce the first slice of stories (e.g. 4–7 stories). User reviews and corrects.
4. **Corrections feed back into strategy** — When mistakes are found, add **DO** / **DO NOT** rules to the strategy document. Re-run the slice until approved.
5. **Next slice** — Once the slice is approved, proceed to the next slice. Repeat steps 3–4 for each slice.
6. **Slice ordering** — At any point, you may change the ordering of slices and adjust the strategy accordingly.
7. **Post-shaping review** — Once all slices are done, have the AI review all corrections and determine what needs to change in the rules and/or instructions.

When analyzing **existing content**, review and follow the strategy.

## Strategy Criteria

### 1 - Shaping GranularityOkay, let's run this scale again.

**Stories** represent the "stopping point". Each story represents something tangible that a user can recognize while fine-grained enough to implement / deliver as independent work.

**Analyze the source** to determine where complexity lives:
- **Business rules** — Distinct rules or conditions that change behavior warrant separate stories when the interaction differs.
- **System interactions** — Different systems or integration points warrant separate stories when the exchange pattern differs.
- **Workflows** — Different sequences or paths warrant separate stories when steps, actors, or outcomes differ.
- **Structure** — Different concept shapes or taxonomies warrant separate stories when the concept structure changes the interaction.
- **State** — Different state transitions or preconditions warrant separate stories when the required or resulting state differs materially.

State your reasoning so the user can adjust.

### 2 - Shaping Depth

When shaping, choose the **depth** of what you produce:
- **Interactions only** — Capture only the interactions themselves, without actors.
- **Interactions + actors** — Interactions with initiating and supporting actors, but nothing more.
- **State concepts without state changes** — Identify and model State Concepts but not Required State and Resulting State for each interaction.
- **Failure modes and responses** — Include or omit Failure Modes and Response behavior.
- **Deeper in some places** — Go deeper in selected areas (steps, examples, acceptance criteria).

Decide and document in the strategy what is in scope.

### 3 - Traversal Order (Slices)

The order in which you work through stories is **not** necessarily epic-by-epic. Slices are units of work that may cut across epics.

**Ideas for prioritizing slices:**
- Architectural slice — Stories that establish the architecture
- Domain slice — Stories aligned by common business logic
- Integration slice — Stories across integration points
- Workflow slice — End-to-end workflow for a particular use case
- Value slice — Stories that provide the most value if done first
- Risk slice — Stories that de-risk some aspect of the solution

Favour slicing vertically, often by a common theme or category of complexity. Consider required-state dependencies (creators before consumers), where complexity is concentrated, and what makes a coherent slice for review.

## Strategy Phase

1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed Epic/Story breakdown, assumptions, break down strategy, **proposed traversal order (slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `story/<domain>-shaping-strategy.md`.

## Running Slices

1. **Run the first slice** — Produce 4–7 stories for Slice 1. User reviews and corrects.
2. **Corrections → strategy** — When a mistake is found, add a **DO** or **DO NOT** to the strategy document. Re-run the slice until the user approves.
3. **Next slice** — Proceed to the next slice. Repeat for each slice.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

## Post-Shaping Review

Once all slices are done, have the AI review all corrections in the strategy and determine what needs to change in the rules and/or instructions. Promote those that apply across domains.
