# Process Overview

<!-- section: shaping.process.intro -->
Your task is to **shape** source material into an **Interaction Tree** and **State Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them. In Agile terminology, this translates to a **story map** and **domain model**. The hierarchy goes from larger, coarser-grain business outcomes (*Epics*) down to **Stories** — tangible user and system interactions. Shaping means we do not go deeper than the story level; details are flushed out later.

Each rule has a DO with example and a DO NOT with example.

**You MUST follow this process before producing any output.**

1. **Strategy Phase first** — Analyze the source, propose Epic/Story breakdown and slice order, save the strategy. Do not produce an interaction tree until the strategy is approved.
2. **Work in slices** — Produce 4–7 stories per slice. Get user approval before moving to the next slice.
3. **No full output in one go** — Do not produce a complete interaction tree in a single pass. Iterate slice by slice.

### When the user says

When the user says "create the story map," "proceed," "build it," "generate the output," or similar, you **MUST still begin with the Strategy Phase**. Do not skip to producing the full output.

### Output Paths (default)

- **Strategy:** `<skill-space>/shaping/strategy.md`
- **Output:** `<skill-space>/shaping/slice-N/` (per slice)

These paths can be configured under the skill-space config (`ace-config.json` or equivalent) so the user can choose where files go and what they are named.

### Before You Produce Output

**STOP.** Before producing any Interaction Tree or State Model, you MUST:

1. [ ] Complete the Strategy Phase (analyze source, propose breakdown, save strategy to `<skill-space>/shaping/strategy.md`)
2. [ ] Get user approval of the strategy
3. [ ] Run Slice 1 only (4–7 stories) and get approval before continuing

## Process Checklist

- [ ] **Strategy Phase complete** — Source analyzed; Epic/Story breakdown proposed; strategy saved to `<skill-space>/shaping/strategy.md`
- [ ] **Strategy approved by user** — Do not produce an interaction tree until then
- [ ] **Slice 1 produced** — 4–7 stories for the first slice
- [ ] **Slice 1 approved** — User reviews; corrections → add DO/DO NOT to strategy (with wrong/correct examples); re-run until approved
- [ ] **Next slice** — Proceed to next slice; repeat until all slices done
- [ ] **Post-shaping review** — Review all corrections; determine what needs to change in rules/instructions

<!-- section: shaping.process.post_shaping.review -->
## Post-Shaping Review

Once all slices are done, have the AI review all corrections in the strategy and determine what needs to change in the rules and/or instructions. Promote those that apply across domains.
