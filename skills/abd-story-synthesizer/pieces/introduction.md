<!-- section: story_synthesizer.introduction -->
# Introduction

The story synthesizer skill turns context into an **Interaction Tree** and **Domain Model** — meaningful exchanges between actors, plus the domain concepts and state that support them. Outputs: story map, domain model, acceptance criteria, specifications.

**Interaction Tree:** Epic → Story → Scenario → Step. Epics can nest (an epic whose parent is an epic is sometimes called a sub-epic). Epics group stories; the story is the backbone — the smallest unit that is both valuable and independently deliverable. Each epic and story can have Pre-Condition, Trigger, and Response. Scenarios optionally group steps; steps are atomic interactions.

**Domain Model:** Domain Models describe the state found in Pre-Condition, Trigger, and Response. **Domain Concepts** (the things that hold state and get operated on) are referenced via `**Concept**` in the name/labels of Interaction tree elements.

The core principle: **Do not go from text to classes. Go from context → mechanisms → behavior owners → object model.**

 Domain concepts emerge from the use of a **17-step pipeline** that separates mechanical evidence extraction (CODE) from analytical reasoning (AI). Scripts extract structured evidence from contex into an **evidence graph** — actions, decisions, variations, states, and relationships.
 
 AI then operates on the evidence graph through focused passes — never on raw text directly. The evidence pipeline creates object models through behavior packet detection, mechanism synthesis, and decision ownership — not from surface noun extraction. Interaction Tree and Domain Model evolve together — no drift.

