<!-- section: story_synthesizer.concept_scan -->
# Domain Concept Scan

The concept scan is the first AI step in the pipeline (Step 2). It runs after context has been normalized but before evidence extraction scripts run. Its purpose is to discover the conceptual structure of the system without designing classes.

## Goal

Produce a **conceptual map** that orients the evidence extraction scripts and feeds into later AI passes. This is not a domain model — it is a hypothesis about what the system is really about, where decisions live, and where behavior varies.

## Instructions

You are performing a domain concept scan.

Your goal is **NOT** to design classes yet.

Your goal is to discover the conceptual structure of the system.

Analyze the context and identify the following:

### 1. Core Domain Primitives

The fundamental things the system operates on. Not surface nouns — things that hold state, get transformed, or participate in decisions.

### 2. Interaction Phases

The major stages of domain interactions or resolution processes. What are the phases that context flows through?

### 3. Stateful Entities

Anything that accumulates state, conditions, or lifecycle changes. Things that are created, modified, tracked, or expired.

### 4. Authority Boundaries

Concepts that appear to own decisions or enforce rules. What decides? What validates? What controls transitions?

### 5. Resource Flows

Resources that are created, transferred, consumed, or modified. What moves through the system and who acts on it?

### 6. Variation Axes

Places where behavior changes depending on a mode, type, category, or condition. These often indicate polymorphic structures.

### 7. Rule Mechanisms

Clusters of rules that appear to revolve around the same mechanism. Rules that collaborate to produce an outcome.

### 8. Implicit Concepts

Missing or implicit concepts that appear necessary to explain the rules but are not named directly in the context.

## Constraints

- Do NOT assume these correspond to classes
- Be skeptical of surface nouns — focus on mechanisms, phases, and rule ownership
- Produce a conceptual map, not an object model
- After the map: identify potential conceptual abstractions that may later become domain objects
- Identify search anchors for targeted evidence extraction

## Output Structure

```
## Core Primitives
- [list]

## Interaction Phases
1. [ordered list]

## Stateful Entities
- [list]

## Authority Boundaries
- [list with what each controls]

## Resource Flows
- [list with flow direction]

## Variation Axes
- [list with what varies]

## Rule Mechanisms
- [list with mechanism description]

## Implicit Concepts
- [list with why each is needed]

## Search Anchors
- [terms/patterns for evidence extraction scripts to target]
```

## Output Location

Write to `<session>/concept_scan.md`.
