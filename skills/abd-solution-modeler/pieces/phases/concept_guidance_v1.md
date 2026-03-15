# Phase 2 — Concept Guidance v1

**Actor:** AI | **Full spec:** [requirements.md](../../docs/requirements.md) § Phase 2

## Purpose

Create the **initial domain hypothesis** that will guide extraction.

This phase should identify the domain's likely:
- **Concepts**
- **Modules**
- **Mechanisms**
- **Actors**
- **Epics**

**Interaction detail:** Epic skeleton only. Epic names; no sub-epics, stories, state, scenarios, or steps.

## Trigger

concept scan, first-cut domain, epic skeleton, domain hypothesis

## Domain detail
Only include:
- concept names
- short interaction-oriented concept statements

Do **not** include:
- properties
- operations
- collaborators
- invariants
- final inheritance
- service/manager/resolver concepts unless explicitly present in the source domain

## Interaction detail
Only produce:
- **Epic skeleton**
- Epic names
- short epic statements

Do **not** produce:
- sub-epics
- stories
- scenarios
- steps
- examples
- state labels

## Inputs
- `rule_chunks.json`

## Instructions

Identify:

1. **Candidate Concepts**
   - include only concepts that appear central to the domain
   - prefer concepts that participate in interactions or state changes
   - avoid example-only roles unless they are real domain concepts

2. **Candidate Modules**
   - group concepts around likely mechanisms
   - modules should be broad and provisional

3. **Likely Mechanisms**
   - name mechanisms that appear to organize multiple rules
   - do not convert mechanisms into classes yet

4. **Likely Actors**
   - identify human/system/domain actors only where relevant to interactions

5. **Likely Epics**
   - broad domain interaction areas only
   - epic names should be verb-noun and domain-grounded

## Output quality rules
- stay shallow
- prefer fewer, stronger concepts over long noun lists
- do not include formulas or exact rule math
- if uncertain, mark as **candidate**, not final
- every concept should have a short interaction-oriented statement
- every epic should be grounded in **Concept** language
- every concept named in the interaction skeleton must exist in the guidance output

## Outputs

1. `domain_concept_guidance_v1.md`
2. `concept_guidance_v1.json`
3. `interaction_tree.md` (epic skeleton only)

## Markdown output shape

```text
# Domain Concept Guidance v1

## Modules

### Module: <name>
- concepts — **ConceptA**, **ConceptB**, **ConceptC**

## Concepts (candidate)

**ConceptA** [foundational] — interacts with **ConceptB**
**ConceptB** — modifies **ConceptC**
**ConceptC** — results from **ConceptA**

## Mechanisms (likely)

- **MechanismA** — short description
- **MechanismB** — short description

## Actors (likely)

- **ActorA** — short description

## Extraction Guidance

### Priority Concepts
- **ConceptA**
- **ConceptB**

### Priority Mechanisms
- **MechanismA**
- **MechanismB**

### Variation Axes
- axis a
- axis b

### Synonym Hints
- **ConceptA**: alias 1, alias 2
- **ConceptB**: alias 3, alias 4
```

## Required JSON shape (concept_guidance_v1.json)

```json
{
  "priority_concepts": ["ConceptA", "ConceptB"],
  "concept_aliases": {
    "ConceptA": ["alias 1", "alias 2"],
    "ConceptB": ["alias 3", "alias 4"]
  },
  "priority_mechanisms": ["MechanismA", "MechanismB"],
  "priority_actors": ["ActorA", "ActorB"],
  "variation_axes": ["axis a", "axis b"],
  "noise_filters": ["license", "table of contents", "ads"],
  "focus_sections": ["section a", "section b"]
}
```

## Checkpoint 1

Human verifies domain framing before proceeding.
