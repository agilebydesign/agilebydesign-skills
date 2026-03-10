---
title: State Model — Resource Concept Naming
impact: HIGH
tags: discovery, domain
scanner: domain_resource_naming
---

## Concepts as Resources

**DO** name concepts as nouns (resources): Order, Portfolio, Voucher, not OrderManager, InstructionPreparer.

**DO** give concepts both Properties and Operations where behavior exists — no anemic concepts (only Properties, no Operations).

**DO NOT** use Manager/Service/Handler/Preparer/Builder suffixes. Name after the resource itself.

**DO NOT** create concepts that are only data carriers with no Operations.

**DO NOT** pass another concept's data to it — concepts own their data. Encapsulation: don't pass another concept's Properties as parameters to its Operations.
