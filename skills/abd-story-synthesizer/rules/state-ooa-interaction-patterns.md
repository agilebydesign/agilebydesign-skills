---
title: State Model — Interaction Patterns
impact: HIGH
tags: [discovery, exploration, specification, interaction_tree, story, step]
---

## Interaction Patterns

**DO** recognize and use interaction patterns when describing Initiation → Response:

| Pattern | Description | Interaction Tree mapping |
|---------|-------------|--------------------------|
| **Producer-Consumer** | One-way; producer sends; consumer reacts | Initiation from one actor; Response from another; no return flow |
| **Client-Server** | Two-way; client requests; server responds | Initiation (request) → Response (reply); may chain to further interactions |
| **Coordinator** | One object orchestrates several others | Epic or Story where one concept delegates to multiple collaborators |
