# Domain Model Format

**Full spec:** `docs/requirements.md` § Core Modeling Formats.

## Module

```
### Module

- name — module name
- concepts — list of tightly related domain concepts
```

## Domain Concept

```
**ConceptName** [foundational] : <Base Concept if any>

- <type> property

      <collaborating concepts if any>

- <type> operation(<param>, ...)

      <collaborating concepts if any>

- Interactions: interaction nodes this concept is used by

- examples: list of domain concept tables in interaction tree using this concept
```

## Guidelines

- Prefer **composition** over inheritance
- Use `Dictionary<K,V>` when items are keyed
- Use `List<T>` only when ordering matters
- Avoid central "service/manager" concepts
