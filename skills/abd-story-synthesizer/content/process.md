# Process Overview

<!-- section: story_synthesizer.process.intro -->
Your task is to **synthesize** context into an **Interaction Tree** and **Domain Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them. In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Synthesis can stop at the story level; details are flushed out later.

Each rule has a DO with example and a DO NOT with example.

**You MUST follow this process.**
When the user says "create the story map," "proceed," "build it," "build a strategy," "generate the output," or similar, you **MUST** call `python scripts/build.py get_instructions <operation>` (e.g. `create_strategy` for strategy, `run_slice` for runs) and inject its output before producing any shaping output. Do not rely on AGENTS.md alone.

1. **Iterative Strategy** — Strategy runs through every run. First run: analyze the source, create the strategy document, build enough of the tree and Domain Model to spot patterns, extrapolate. Create the tree and Domain Model as you go — do not wait for strategy approval before producing output.
2. **Work in runs** — Each run produces output for a slice (4–7 stories typical). A run may require **multiple iterations**: user reviews, finds mistakes, you add corrections to the **run log**, re-run. Repeat until the user approves. Only then proceed to the next run.
3. **No full output in one go** — Do not produce a complete interaction tree in a single pass. Iterate run by run.
4. **Review and Adjust** - Once all runs are done, have the AI review all corrections collected in the **run log** and determine what needs to change in the rules and/or instructions. Promote those that apply across projects  to the skill's rules.

## Output Paths (default)

- **Strategy:** `<skill-space>/story-synthesizer/strategy.md`
- **Output:** `<skill-space>/story-synthesizer/` — Interaction Tree and Domain Model (format in `output/interaction-tree-output.md` and `output/domain-model-output.md`)
- **Runs:** `<skill-space>/story-synthesizer/runs/` — run logs (one file per run, e.g. `run-1.md`)

**Runs** — Each run is a purposeful loop: it defines how much detail to synthesize, where to stop (epics vs stories vs steps), and produces output. We track runs, not slices. Each run writes a run log. **Corrections go to the run log** (the run's Corrections section), not to the strategy. See `run-output.md` for format;

## Slices and Runs

- **Slice** — A collection of context we want to further refine, ranging from no structure to a set of example stories. Each slice defines *what* we are synthesizing. A slice can be scoped to epics only (not down to stories), or it can go all the way to stories, steps, or examples — the slice defines the scope.
- **Run** — A purposeful loop to perform the next increment of our strategy. Each run defines in how much detail we will be synthesizing, where we stop (e.g., at epics or at stories), tracks the output of the step in the process, is used to track progress, and produces a slice of output. A run can stop at epics and not stories — we have explicit control over the stopping point.

### Run Log

Each run writes a **run log** to its own file. The log records Before, After, and Corrections. See `run-output.md` for structure and format.

This gives better granularity for improving things over time — run logs can be fed into an agent, analyzed for patterns, or used to refine the strategy.

### Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the run's stopping point (e.g., 4–7 stories if stopping at stories; epics and sub-epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a **DO** or **DO NOT** to the **run log** (the run's Corrections section). Each correction must include:
   - The **DO** or **DO NOT** rule
   - **Example (wrong):** What was done incorrectly
   - **Example (correct):** What it should be after the fix
   - If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block
   - Re-run the slice; update the run log with the new Before/After and any additional corrections; repeat until the user approves
3. **Next slice** — Proceed to the next slice. Same pattern: produce → review → corrections to run log → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the strategy and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

These paths can be configured under the skill-space config (`abd-config.json` or equivalent) so the user can choose where files go and what they are named.

## Process Checklist

- [ ] **Strategy document created/updated** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `<skill-space>/story-synthesizer/strategy.md`; tree and Domain Model built as you go
- [ ] **Run 1 produced** — Output for first slice; run log written to `runs/run-1.md`
- [ ] **Run 1 iterated to approval** — User reviews; when mistakes are found, add DO/DO NOT to the **run log** Corrections section (with wrong/correct examples); re-run taking corrections into account; repeat until user approves
- [ ] **Post-synthesis review** — Review all corrections collected in run log; determine what needs to change in rules/instructions; promote reusable corrections to strategy and/or skill
- [ ] **Next run** — Proceed to next slice;or conduct another run to go deeper on same slice; same iteration pattern (produce → review → corrections to run log → re-run until approved)
