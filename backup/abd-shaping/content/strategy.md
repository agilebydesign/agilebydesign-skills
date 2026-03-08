# Strategy Phase

<!-- section: shaping.strategy.phase -->
1. **Analyze the source** to determine where complexity lives.
2. **Present the strategy** to the user. Include: complexity areas identified, proposed Epic/Story breakdown, assumptions, break down strategy, **proposed traversal order (slices)**.
3. **Validate until reasonable** — User reviews; refine until approved. Do not produce an interaction tree until then.
4. **Save the strategy** to `<skill-space>/shaping/strategy.md`.

<!-- section: shaping.strategy.criteria -->
## Strategy Criteria

### 1 - Splitting Criteria

**Stories** represent the "stopping point". Each story represents something tangible that a user can recognize while fine-grained enough to implement / deliver as independent work.

**Determine splitting criteria** — How do we split epics into sub-epics, and sub-epics into stories? Analyze the source to identify criteria that drive the split. Examples of ways to figure out splitting criteria:
- **Business rules** — Distinct rules or conditions that change behavior warrant separate stories when the interaction differs.
- **System interactions** — Different systems or integration points warrant separate stories when the exchange pattern differs.
- **Workflows** — Different sequences or paths warrant separate stories when steps, actors, or outcomes differ.
- **Structure** — Different concept shapes or taxonomies warrant separate stories when the concept structure changes the interaction.
- **State** — Different state transitions or preconditions warrant separate stories when the required or resulting state differs materially.

State your splitting criteria and reasoning so the user can adjust.

### 2 - Depth

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

<!-- section: shaping.strategy.slices.running -->
## Running Slices

1. **Run the first slice** — Produce 4–7 stories for Slice 1. User reviews and corrects.
2. **Corrections → strategy** — When a mistake is found, add a **DO** or **DO NOT** to the strategy document. Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the slice until the user approves
3. **Next slice** — Proceed to the next slice. Repeat for each slice.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

<!-- section: shaping.strategy.corrections -->
## Corrections Format

When adding corrections to the strategy document, each **DO** or **DO NOT** must include:
- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the slice until the user approves.

When analyzing **existing content**, review and follow the strategy.

### Object Model Correction

**DO** — Inject the Engine (or context provider) into components that need it. Use properties over getters. Encapsulate over passing parameters — components pull context from injected dependencies instead of receiving it as method arguments.

- **Example (wrong):** `AbdSkill.get_instructions_for(operation, context)` — context passed as parameter.
- **Example (correct):** AbdSkill has `Engine engine` (injected); `instructions` property; assembles using `engine.workspace`, `engine.strategy_path` when needed.

### Skill Update Workflow

**DO** — Update the ace-shaping skill in `agile-context-engine/skills/ace-shaping/` first (core); then copy those updates to test installations (e.g. `mutants-and-masterminds/.agents/skills/ace-shaping/`).

- **Example (wrong):** Editing the skill only in a test project; creating standalone scripts in test without updating core; core and test copies drift.
- **Example (correct):** Edit `agile-context-engine/skills/ace-shaping/`; run build; copy updated `scripts/build.py`, `content/script-invocation.md`, and any other changed files to the test project's ace-shaping copy.
