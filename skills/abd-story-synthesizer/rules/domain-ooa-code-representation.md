---
title: State Model — Code Representation
impact: MEDIUM
tags: discovery, domain
scanner: domain_code_representation
---

## Align to Implementation

**DO** use concise concept names that could exist as types (Order, Portfolio, LineItem).

**DO** use typed Properties and Operations — actual type names (Money, Symbol, Quantity), not prose descriptions.

**DO NOT** use long prose sentences as concept names (e.g. "Collection of customer investments that aggregates all holdings...").

**DO NOT** use prose descriptions for Property or Operation types — use actual type names (e.g. `RiskScore, RiskModel, Holding`, not "detailed object containing volatility calculations").
