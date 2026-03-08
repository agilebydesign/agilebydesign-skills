# Run Output

Each run writes a run log to its own file. A run may require **multiple iterations** (user reviews → corrections added → re-run). The run log is updated on each iteration; corrections accumulate in the Corrections section.

**Path (default):** `<skill-space>/story-synthesizer/runs/run-N.md` (N = run number). Configurable via skill-space config.

## Structure

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
The DOs and DON'Ts added during this run. Each time the user finds a mistake, add a new correction here (do not add to strategy). Each correction includes:
- The rule
- Example (wrong)
- Example (correct)
```

Run logs are used to track progress, feed into agents, analyze patterns, or refine the strategy. The post-synthesis review promotes reusable corrections from run logs to the strategy or skill rules.
