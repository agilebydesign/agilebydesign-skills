---
title: State Model — Integrate Concepts
impact: HIGH
tags: discovery, domain
scanner: domain_integrate
---

## Nest Related Capabilities Under Parent

**DO** integrate related capabilities under a parent concept (e.g. Character Animation with multiple Operations, not separate Walk Animation, Run Animation concepts).

**DO** group concepts by business domain, not technical layers (Data Layer, Business Logic Layer).

**DO NOT** create separate concepts with the same noun when they should be one (PortfolioValue, PortfolioRisk, PortfolioAllocation → Portfolio).

**DO NOT** split related capabilities into separate sibling concepts (PortfolioValue, PortfolioRisk as separate concepts when they belong under Portfolio).

**DO NOT** group by technical layers or implementation patterns (Factories, Builders, Repositories).
