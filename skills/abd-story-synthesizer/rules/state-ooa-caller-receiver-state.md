---
title: State Model — Caller, Receiver, State Mapping
impact: HIGH
tags: discovery, exploration, specification
---

## Caller, Receiver, Message → Initiation and Response

**DO** map OOA caller/receiver/message to the interaction model:
- **Caller** → Initiating-Actor (who starts the interaction)
- **Receiver** → Responding-Actor (who receives and responds)
- **Message** → Behavior in Initiation (what is requested) and Behavior in Response (what is done)

**DO** ensure every concept that participates as caller or receiver exists in the State Model with Properties and Operations that support that participation.

## State Before / State After → Pre-Condition, Initiating-State, Resulting-State

**DO** map OOA state before/after to interaction fields:
- **State Before** → Pre-Condition (what must be true) + Initiating-State (state that qualifies the initiation)
- **State After** → Resulting-State (state that results from the response)

**DO** reference domain concepts in these labels via `**Concept**` so state flows are traceable to the State Model.

## Event as Initiation

**DO** treat an **event** as the **Initiation** that causes the **Response**. The Initiation (Initiating-Actor, Behavior, Initiating-State) is the stimulus; the Response (Responding-Actor, Behavior, Resulting-State) is the reaction. Events often appear as user actions, system triggers, or state changes that qualify the interaction.
