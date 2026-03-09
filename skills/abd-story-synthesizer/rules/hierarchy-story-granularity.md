---
title: Story granularity
impact: MEDIUM-HIGH
tags: [shaping, discovery, interaction_tree, epic, story]
---

## Story granularity

**DO** break down by distinct requirements areas, distinct concept structure, or workflow steps; sufficient stories to capture rule detail.
- Example (right): Story "View Product Details", Story "Make Payment" (each has distinct logic). Story "Drive Bike", Story "Drive Car" (concept structure differs).

**DO NOT** collapse large rule sections into one story.
- Example (wrong): Story "All combat effects" or "All attack types" when the context has dozens of distinct rules. Right: Story "Apply damage effect", Story "Apply condition effect", Story "Resolve melee attack", etc.
