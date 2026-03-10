---
title: Data vs logic story split
impact: HIGH
tags: [discovery, interaction_tree, story]
---

## Data vs logic story split

When multiple items in the context follow the same workflow but with different data values, they are one story with examples — not separate stories. When items change the business rules, validation logic, workflow, or constraints, they are separate stories. The split criterion is: does this item change the rules, or just the data?

**DO** merge items into one story when the only difference is pre-selected data values — the workflow, business rules, and validation are identical. Name the variants as examples on the story so the scope is visible, but don't detail what each variant pre-fills until Specification.
- Example (right): "Select pre-configured **Transaction** type" as one story with examples: Wire, ACH, SEPA.
- Example (right): "Select **InsurancePolicy** template" as one story with examples: Auto, Home, Life.

**DO** break out a separate story when options change the business rules, workflow, or business logic — new validation, new cost calculation, new constraints, new state transitions.
- Example (right): "Configure **Transaction** modifiers" as its own story — adding rush processing changes the fee calculation, adding compliance hold changes the state machine, adding split payment changes the validation rules. These are not data variants; they change how the system behaves.
- Example (right): Base story "Configure **Policy**" handles standard fields. Separate story "Configure **Policy** riders" handles add-ons that change premium calculation, coverage rules, and exclusion logic.

**DO NOT** create separate stories for pre-configured variants of the same workflow when the only difference is which data values are pre-filled.
- Example (wrong): "Configure Wire Transfer", "Configure ACH Transfer", "Configure SEPA Transfer" as three separate stories — when all three are "Configure **Transaction**" with different pre-filled fields. The workflow is identical; only the data differs.
- Example (wrong): "Configure Auto Policy", "Configure Home Policy" as separate stories — when both follow the same configure-validate-submit workflow with different field sets. Make them examples on one story.

**How to decide:**
1. Does this variant change which validation rules apply? → Separate story
2. Does this variant change the cost/pricing calculation? → Separate story
3. Does this variant add or remove workflow steps? → Separate story
4. Does this variant add new constraints or state transitions? → Separate story
5. Does this variant only change which fields are pre-filled? → Same story, add as example
6. Does this variant only change the data values but the same rules apply? → Same story, add as example
