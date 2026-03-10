---
title: Scaffold pattern not enumeration
impact: HIGH
tags: [discovery, interaction_tree, epic, story]
---

## Scaffold pattern not enumeration

The first cut of `interaction-tree.md` and `domain-model.md` establishes the pattern for each epic. Runs expand the files slice by slice. If the first cut enumerates everything, runs have nothing to do. The session scaffold summarizes the first cut; the output files contain the real content.

**DO** detail 2-3 representative stories per epic/sub-epic with full fields (Trigger, Response, Pre-Condition, domain concepts). List remaining stories by name only with "N more stories following this pattern based on [specific items]."
- Example (right): Two stories under a sub-epic shown in full with Trigger/Response and domain concepts; then "4 more stories following this pattern: [Story A], [Story B], [Story C], [Story D]."

**DO** have the session scaffold reference the output files and list every story by name with exact counts. Mark which stories have full trigger/response detail *(detailed)* and which are listed by name only. Use "N detailed + N more = total" counts per sub-epic that sum to the epic total.
- Example (right): Session scaffold says "See `interaction-tree.md` for full trigger/response detail on stories marked *(detailed)*." then lists: "Configure **Abilities** (2 stories): Set **AbilityRank** *(detailed)*, Validate **AbilityRank** *(detailed)*". Epic total: "16 sub-epics, 66 stories".
- Example (right): "Configure **Damage** Powers [MG1] (1 detailed + 4 more = 5 stories): Configure **Damage** *(detailed)*, 4 more following this pattern: Configure **Blast**, Configure **MentalBlast**, Configure **EnergyAura**, Configure **Strike**"
- Example (wrong): "Configure **Damage** Powers | 5 | DamageEffect, ResistanceCheck" — a table row with a count and concept names but no story names, no *(detailed)* markers, no reference to where the full content lives.
- Example (wrong): "~55 stories" when the actual count is 66 — approximate counts lose trust and make it impossible to verify completeness.

**DO NOT** enumerate every story with full detail in the first cut. The first cut is not the finished map — it is the pattern that runs expand.
- Example (wrong): All 6 stories in a sub-epic shown with full Trigger, Response, Pre-Condition, and domain concepts in the first-cut interaction-tree.md. Runs then have nothing to add for that sub-epic.
