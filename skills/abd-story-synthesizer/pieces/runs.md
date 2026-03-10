<!-- section: story_synthesizer.runs -->
# Runs

During a session you synthesize the scope of a slice through a run. **One run per slice.** Run 1 = slice 1, run 2 = slice 2, etc. A run captures what happened, what changed, when it changed. The session defines level of detail; the slice defines scope for the run.

**Going deeper on the same slice** (e.g. adding steps to discovered stories) is a **new session** with a different focus, not another run.

Each run writes a **run log** to its own file under the session's runs folder. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md` (N = run number). Configurable via skill-space config.

## Running Slices

1. **Run the first slice** — Produce output for Slice 1 according to the session's level of detail (e.g. 4–7 stories if stopping at stories; epics only if stopping at sub-epics). Write the run log. User reviews.
2. **Corrections → run log** — When a mistake is found, add a DO or DO NOT to the run log's Corrections section (see Corrections Format below). Re-run the slice; update the run log; repeat until approved.
3. **Next slice** — Proceed to the next slice. Apply corrections from previous runs. Same pattern: produce → review → corrections → re-run until approved.
4. **Slice ordering** — At any point, you may change the slice order; update the session and continue.
5. **Progressive expansion** — Slice size may increase as the user prefers.

## Run Log Structure

```
# Run N

## Scope
The slice for this run. At least node names (epics, stories) in scope. E.g.:
- Epic: User checks out
- Story: Apply discount code
- Story: Select payment method

## Before
What we had at the start (e.g., raw context, stories, steps). Summary or snippet.

## After
What we had afterwards (e.g., context → stories, stories → steps). Summary or snippet.

## Corrections
The DOs and DON'Ts added during this run. Each time the user finds a mistake, add a new correction here (do not add to session file directly). Each correction includes:
- The rule
- Example (wrong)
- Example (correct)
```

Run logs are used to track progress, feed into agents, analyze patterns, or refine the session strategy. The post-synthesis review promotes reusable corrections from run logs to the session or skill rules.

<!-- section: story_synthesizer.runs.corrections -->
## Corrections Format

When adding corrections to the run log (Corrections section), each **DO** or **DO NOT** must include:

- The **DO** or **DO NOT** rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be after the fix
- If it is the second (or later) time failing on the same guidance, add an extra example to the existing DO/DO NOT block

Re-run the slice until the user approves. Corrections stay in the run log; the post-synthesis review promotes reusable ones to the session or skill rules.

## When User Gives a Correction

**Trigger phrases:** "wrong", "correction", "this is wrong", "strategy is wrong", "too superficial", "fix this", "redo", "try again"

**You MUST:**

1. **Add to run log** — Create or append to `runs/run-N.md` (use `run-0.md` for corrections during session start / strategy creation). Format:
  - **DO** or **DO NOT:** [the rule]
  - **Example (wrong):** [what was done incorrectly]
  - **Example (correct):** [what it should be]
2. **Apply the correction** — Refine session strategy or re-run with corrections as input.
3. **Proactively confirm** — Say: "I've added this to the run log. Correction: [brief summary]. I've applied it."

**First-run corrections:** Use `runs/run-0.md` to capture corrections during session start and initial tree/model building. Same format. The run log feeds future runs.

<!-- section: story_synthesizer.runs.patterns -->
## Patterns (from Runs)

**Strategy is upfront; runs can extend it.** After each run, examine all runs for new patterns. If found, add to the session's Patterns section.


| Run   | What was built                                               | Pattern found             | Applicable to               |
| ----- | ------------------------------------------------------------ | ------------------------- | --------------------------- |
| run-1 | e.g. "wrote steps and examples for all stories under epic X" | Brief pattern description | Scope where pattern applies |


**Example:** Run 2 built steps and examples for "Configure Power Effect" stories. Pattern: "Effect-type stories share same step structure — Configure, Validate, Apply." Applicable to: other effect types under the same epic.
