
# Complete Domain Modeling Pipeline
Guidance → Sketch → Refine  
With **OOAD Domain Model** + **Interaction Tree** (Story Mapping)

This document defines a **full execution plan** for transforming raw context (rules, requirements, documentation, or code) into a **validated OO domain model** and **interaction tree**.

Two primary artifacts evolve together:

1. **Domain Model (OOAD)**
2. **Interaction Tree**

Both are incrementally refined through the pipeline.

---

# Core Modeling Formats

## Module

A grouping of tightly related concepts collaborating around a mechanism.

```
### Module

- name — module name
- concepts — list of tightly related domain concepts
```

---

## Domain Concept

```
**ConceptName** [foundational] : <Base Concept if any>

- <type> property

      <collaborating concepts if any>

- <type> operation(<param>, ...)

      <collaborating concepts if any>

- Interactions: interaction nodes this concept is used by

- examples: list of domain concept tables in interaction tree using this concept
```

Guidelines:

- Prefer **composition** over inheritance
- Use `Dictionary<K,V>` when items are keyed
- Use `List<T>` only when ordering matters
- Avoid central "service/manager" concepts

---

# Interaction Tree Model

An **Interaction** is a meaningful exchange between actors resulting in state retrieval or change.

**Hierarchy:** Epic → Story → Scenario → Step

| Node | Meaning |
|-----|--------|
Epic | Large domain capability; groups stories |
Story | Smallest independently valuable behavior; backbone unit |
Scenario | step grouping for a condition |
Step | Atomic interaction |

**Per interaction:** Trigger (Triggering-Actor, Behavior) + Response (Responding-Actor, Behavior). Pre-Condition (label). Examples.

**Domain grounding:** Use `**Concept**` in labels; every concept must exist in Domain Model.

**Inheritance:** Parent → child; use `[brackets]` for inherited values.

**Interaction tree progression (what each phase adds):**

| Phase | Adds to interaction tree |
| ----- | ------------------------- |
| 2 | Epic skeleton (names only) |
| 5 | Epics, sub-epics, first-cut stories (names only) |
| 6 | Story placement refined; structure only |
| 7 | Concepts linked to stories |
| 8 | Triggering-Actor, Responding-Actor per story |
| 9 | Trigger, Response, Pre-Condition, Steps |
| 10 | Variation paths (prep for scenarios) |
| 11 | Scenarios (group steps), Failure-Modes, Constraints |
| 12 | Walkthrough validates (no new content) |
| 13 | Examples (tables per concept) |

---

# Phase 1 — Normalize Context

Actor: **Code**

Purpose:
Prepare raw materials for reasoning.

Inputs:

- rulebooks
- specs
- documentation
- code (optional)

Instructions:

- split into logical chunks
- assign stable IDs
- preserve source location
- do not interpret text

Outputs:

```
rule_chunks.json
```

Example:

```json
{
  "chunk_id": "R12",
  "source": "combat_rules.md",
  "text": "Target rolls Toughness against DC 15 + damage rank."
}
```

Checkpoint: None

---

# Phase 2 — Concept Guidance v1

Actor: **AI**

Purpose:
Create the **initial domain hypothesis**.

**Domain detail:** Concept names + interactions only (no properties, operations, collaborators).

**Interaction detail:** Epic skeleton only. Epic names; no sub-epics, stories, state, scenarios, or steps.

Inputs:

```
rule_chunks.json
```

Instructions:

Identify:

- candidate **Concepts**
- candidate **Modules**
- likely **Mechanisms**
- likely **Actors**
- likely **Epics**

Avoid:

- finalizing inheritance
- creating service classes

Outputs:

```
domain_concept_guidance_v1.md
interaction_tree.md (epic skeleton)
```

Example Domain Model:

```
### Module

- name — Combat Core
- concepts — Character, Attack, Effect, ConditionTrack
```

```
**Character** [foundational] — Resolve **Attack**
**Attack** — Resolve **Attack**
**Effect** — Resolve **Attack**, damage resolution
```

Example Interaction Tree:

```
# Epic: Resolve **Attack**
(**Character** performs **Attack**; **System** resolves **Effect** and resulting **Condition** changes)
```

Checkpoint 1: Human verifies domain framing.

---

# Phase 3 — Evidence Extraction

Actor: **Code**

Purpose:
Extract structured rule evidence.

Inputs:

```
rule_chunks.json
```

Instructions:

Extract:

- terms
- actions
- decisions
- states
- relationships
- modifiers

Outputs:

```
terms.json
actions.json
decisions.json
states.json
relationships.json
modifiers.json
```

Example:

```
Attack invokes Effect
```

---

# Phase 4 — Evidence Graph

Actor: **Code**

Purpose:
Build rule dependency structure.

Inputs:

Extraction outputs.

Instructions:

Create graph relations:

```
Concept → performs → Action
Action → produces → State
Concept → modifies → Concept
```

Outputs:

```
evidence_graph.json
```

Example:

```
Attack → invokes → Effect
Effect → invokes → ResistanceCheck
Outcome → modifies → ConditionTrack
```

Checkpoint 2: Human validates rule coverage.

---

# Phase 5 — Concept Guidance v2

Actor: **AI**

Purpose:
Refine domain structure using evidence graph.

**Domain detail:** Refined concepts, modules.

**Interaction detail:** Second-cut epics and sub-epics; first-cut stories (names only). Incomplete, incorrect likely. No state, scenarios, steps, or other story details.

Inputs:

```
domain_concept_guidance_v1.md
evidence_graph.json
```

Instructions:

- merge duplicate concepts
- split overloaded concepts
- detect hidden concepts
- refine modules
- refine operations cautiously

Outputs:

```
domain_concept_guidance_v2.md
interaction_tree.md (epics, sub-epics, story names only)
```

Example:

```
### Module

- name — Combat Resolution
- concepts — Attack, TargetingMode, Effect, ResistanceCheck, ConditionTrack
```

Example Interaction Tree:

```
# Epic: Resolve **Attack**
  ## Sub-epic: Execute Attack
    Story: Execute **Attack**
    Story: Apply **Effect** to target
  ## Sub-epic: Resolve Damage
    Story: Roll **ResistanceCheck**
```

---

# Phase 6 — Interaction Tree Structure

Actor: **AI**

Purpose:
Refine story placement under epics/sub-epics. Still structure only.

**Interaction detail:** Epics, sub-epics, stories correctly placed. Names only. No Trigger, Response, Pre-Condition, state, scenarios, steps, Failure-Modes, or Constraints.

Inputs:

```
domain_concept_guidance_v2.md
evidence_graph.json
interaction_tree.md
```

Outputs:

```
interaction_tree.md
```

Checkpoint 3: Human validates structure.

---

# Phase 7 — Concept Model

Actor: **AI**

Purpose:
Identify core concepts and modules. Convert refined concepts into class-like model.

**Interaction detail:** Link domain concepts to each story (which **Concepts** each story uses). Still no Trigger, Response, Steps.

Inputs:

```
domain_concept_guidance_v2.md
interaction_tree.md
```

Outputs:

```
concept_model.md
interaction_tree.md
```

Example:

```
**ConditionTrack**

- Dictionary<String, Condition> conditions

- applyCondition(condition)
```

---

# Phase 8 — Structural Model

Actor: **AI**

Purpose:
Add relationships and composition between concepts.

**Interaction detail:** Triggering-Actor and Responding-Actor per story (who starts, who responds). Structure only; no Trigger/Response behavior yet.

Instructions:

- define composition relationships
- attach collaborators

Outputs:

```
structural_model.md
interaction_tree.md
```

Example:

```
Character
 ├ Attacks
 └ ConditionTrack
```

---

# Phase 9 — Behavior Model

Actor: **AI**

Purpose:
Assign operations to concepts based on interaction steps.

**Interaction detail:** Trigger, Response, Pre-Condition, Steps. Behavioral flow from operations. No scenarios yet (steps not grouped).

Inputs:

```
interaction_tree.md
structural_model.md
```

Outputs:

```
behavior_model.md
interaction_tree.md
```

Example:

```
**Effect**

- resolve(target)

      ResistanceCheck
      ConditionTrack
```

Example Interaction Tree:

```
### Story: Execute **Attack**
- Pre-Condition: [**Character** has valid **Attack**]
- Trigger: Triggering-Actor: [User], Behavior: performs attack
- Response: Responding-Actor: [System], Behavior: resolves **Effect**, rolls **ResistanceCheck**
- Steps:
  1. Perform attack check
  2. Invoke **Effect**
  3. Roll **ResistanceCheck**
  4. Apply **Condition**
```

Checkpoint 4: Human verifies ownership correctness.

---

# Phase 10 — Variation Model

Actor: **AI**

Purpose:
Model inheritance/strategy/modifier variation.

**Interaction detail:** Identify variation paths (success vs failure, branches). Prep for scenario grouping. No scenarios yet.

Inputs:

```
modifiers.json
interaction_tree.md
```

Outputs:

```
variation_model.md
interaction_tree.md
```

Example:

```
**Effect** [foundational]

**DamageEffect** : Effect

**AfflictionEffect** : Effect
```

---

# Phase 11 — Refined Domain Model

Actor: **AI**

Purpose:
Clean structure and finalize modules.

**Interaction detail:** Scenarios (group steps by condition). Failure-Modes, Constraints. Required before Scenario Walkthrough — you cannot walk through scenarios without scenarios.

Instructions:

- split large classes
- remove fake concepts
- refine module boundaries

Outputs:

```
refined_domain_model.md
interaction_tree.md
```

Example Interaction Tree:

```
### Story: Execute **Attack**
- Scenarios:
  - Success — target hit
  - Resistance succeeds — no effect
- Failure-Modes: invalid target, resistance succeeds
- Steps: (grouped under scenarios)
```

Checkpoint 5: Human structural validation.

---

# Phase 12 — Scenario Walkthrough

Actor: **AI + Human**

Purpose:
Validate design by walking through scenarios. Requires scenarios from Phase 11. No Examples yet — those come after walkthrough when you know exact behavior on exact objects.

Inputs:

```
interaction_tree.md (with scenarios, steps)
refined_domain_model.md
```

Outputs:

```
scenario_walkthroughs.md
```

Example:

```
Attack.perform()
→ TargetingMode.resolve()
→ Effect.resolve()
→ ResistanceCheck.roll()
→ ConditionTrack.applyCondition()
```

Checkpoint 6: Behavioral validation.

---

# Phase 13 — Validated Domain Model

Actor: **AI**

Purpose:
Produce final OOAD model synchronized with interaction tree.

**Interaction detail:** Add Examples (tables per concept). Ideal time — after scenario walkthrough you know exact behavior on exact objects.

Outputs:

```
validated_domain_model.md
interaction_tree.md (with Examples)
```

---

# Final Artifacts

Code:

```
rule_chunks.json
terms.json
actions.json
decisions.json
states.json
relationships.json
modifiers.json
evidence_graph.json
```

AI:

```
domain_concept_guidance_v1.md
domain_concept_guidance_v2.md
concept_model.md
structural_model.md
behavior_model.md
variation_model.md
refined_domain_model.md
scenario_walkthroughs.md
validated_domain_model.md
```

Behavior Model:

```
interaction_tree.md
```

---

# Key Principle

The system maintains **two synchronized models**:

### Structural

Domain Model (OOAD)

### Behavioral

Interaction Tree

Each continuously refines the other until a stable domain model emerges.
