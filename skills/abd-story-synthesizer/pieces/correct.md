<!-- section: story_synthesizer.correct.run -->
# Correct Run

Review this chat for changes made to session files that are not recorded as corrections in the current run log.

**For each change you made during this session:**

1. Was it a user-requested fix, restructuring, or improvement? (Skip trivial changes: typo fixes, formatting, count updates that follow from other changes)
2. Does a corresponding DO or DO NOT correction exist in the run log?
3. If not — propose the correction to the user before writing it.

**For each candidate correction, present to the user:**

- **Change:** Brief description of what was changed
- **Proposed correction:** The DO or DO NOT rule
- **Record this?** (yes / skip)

Only skip trivial changes (formatting, typos, mechanical count updates). Everything else is a candidate — changes that reflect a pattern about how to structure stories, domain models, scaffolds, variation analysis, or the process itself.

**Write corrections in domain-neutral language.** Corrections must apply across any domain — payments, retail, games, healthcare, whatever. Use terms like "business rules", "workflow", "validation", "data variants", "cross-cutting concepts" — not the current skill space's domain terms. The examples can reference the current domain to illustrate, but the rule itself must be generic.

**After review, write approved corrections to the run log** using the standard format:
- **DO** or **DO NOT:** [the rule]
- **Example (wrong):** [what was done incorrectly]
- **Example (correct):** [what it should be]

<!-- section: story_synthesizer.correct.session -->
# Correct Session

Review the corrections in the current run log and determine which should be incorporated into the session strategy.

**For each correction in the run log:**

1. Does this correction affect how the session's variation analysis, slices, or scaffold should be structured?
2. Is it specific to this session's context (not a universal rule)?
3. If yes to both — propose incorporating it into the session strategy.

**For each candidate, present to the user:**

- **Correction:** The DO or DO NOT from the run log
- **Strategy impact:** What would change in the session file (variation analysis section, slice scope, scaffold structure)
- **Proposed change:** The specific edit to the session file
- **Apply this?** (yes / skip)

Be aggressive in suggestions. If a correction reveals a pattern that should change the variation analysis, slice ordering, or scaffold structure — propose it. Don't wait for the user to ask.

**After review, apply approved changes to the session file** and note in the run log which corrections were incorporated into strategy.

<!-- section: story_synthesizer.correct.skill -->
# Correct Skill

Review the corrections in the current run log and determine which should be promoted to the skill's rules or process pieces.

**For each correction in the run log:**

1. Is this correction reusable across projects — not specific to this session's domain?
2. Does an existing skill rule already cover it? (If so, does the rule need strengthening?)
3. If reusable and not covered — propose promoting it to a new or existing rule.

**For each candidate, present to the user:**

- **Correction:** The DO or DO NOT from the run log
- **Target:** New rule, strengthen existing rule, or update process piece
- **Target file:** The specific file path (e.g. `rules/interaction-data-vs-logic-story-split.md`)
- **Proposed change:** What to add or modify
- **Promote this?** (yes / skip)

Be aggressive in suggestions. If a correction applies beyond this project's domain, it belongs in the skill. Don't hold back — propose the change, let the user decide.

**After review, apply approved changes to the skill** and record in the run log's "Promoted to Skill" table:

| Correction | Target file | Change |
|-----------|-------------|--------|

Then rebuild AGENTS.md: `python scripts/build.py`
