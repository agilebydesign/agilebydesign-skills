# Required Output Structure

**Output path (default):** `<skill-space>/shaping/` — write the Interaction Tree and State Model in `shaping/slice-N/` per slice. Configurable via skill-space config.

**Workflow:** Start with interactions. Derive concepts from the interactions. Model the concepts in OOAD style (State Model). Add inline Concepts blocks under Epics with compact definitions (properties, operations). Complete this full workflow for each slice.

<!-- section: shaping.output.interaction_tree -->
## A) Interaction Tree

A hierarchical structure of meaningful exchanges between actors. All levels use the same interaction format — they differ only in granularity.

**Hierarchy:**
```
Epic (coarse interaction)
  └─ Epic (finer-grained)
       └─ Story (fine interaction)
            └─ Scenario (optional grouping of steps)
                 └─ Step (atomic interaction to be done at a later state)
```

**Node names:** Use bold for Epic and Story node names (e.g. `- Epic: **Create Ace-Skill**`, `- Story: **Create scaffolding via script**`).

**Interaction format (used at every level):**

| Field | Description |
|-------|-------------|
| Actor | Initiating actor |
| Supporting | Responding actor(s) |
| Required State | Preconditions (inherit from parent; add only new/specialized) |
| State Concepts | Domain concepts involved |
| Initiation | What the initiating actor does (verb-noun) |
| Response | What the supporting actor does (behavior only) |
| Resulting State | Outcome only; use commas for multiple changes |
| Failure Modes | Max 3, rule/state based only |

**Granularity:** Each story must represent something tangible, valuable, and fine-grained enough to implement. Do not collapse large requirements / business rules / complexity into a single story.

<!-- section: shaping.output.state_model -->
## B) State Model

Identify the domain state concepts referenced in the Interaction Tree. Model each concept in OOAD style:

```
Concept : <Base Concept if any>
- <stateful concept returned> property
      <collaborating concepts if any>
- <stateful concept returned> operation(<param>, <param>, ...)
     <collaborating concepts if any>
```

**Format:**
- **Concept** — name; optionally `: BaseConcept` if it extends another
- **Properties** — `<concept type> property` with optional collaborating concepts below
- **Operations** — `<concept type> operation(<params>)` with optional collaborating concepts below
- **Collaborating concepts** — other concepts this property/operation works with or depends on
- **Invariants** — when an invariant applies to a single property or operation, state it under that property or operation

**Scoping:** Declare each concept at the Epic (or Story) that is the root of the smallest subtree where it is used. Concepts used across multiple Epics belong at their common ancestor.
