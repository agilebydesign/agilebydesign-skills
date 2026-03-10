---
title: Correction recording required
impact: HIGH
tags: [discovery, exploration, specification, interaction_tree, epic, story, domain, step, scenario, example]
---

## Correction recording required

Every user-requested change must be recorded as a correction in the run log. A change is not complete until the correction is written. This rule applies at all stages (Discovery, Exploration, Specification) and all object types (epics, stories, steps, scenarios, examples, domain concepts).

**DO** record a correction in the run log for every user-requested fix, restructuring, or improvement — immediately after applying the change. The correction must be in domain-neutral language with wrong/correct examples.
- Example (right): User asks to restructure a sub-epic. AI applies the restructuring AND writes a DO/DO NOT to the run log with wrong/correct examples. AI confirms: "Correction recorded: [summary]."
- Example (right): User points out stories should be merged. AI merges them AND writes the correction. Both the fix and the correction happen together.

**DO NOT** apply a fix without recording the corresponding correction. Do not batch corrections for later. Do not skip corrections for "obvious" fixes.
- Example (wrong): User requests 5 changes during session creation. AI applies all 5 but only records the last one as a correction. The first 4 patterns are lost.
- Example (wrong): AI applies a fix and says "done" without mentioning or writing the correction.

**During validation**, check that the run log contains corrections for all changes made since the last checkpoint. If corrections are missing, flag them as violations.
