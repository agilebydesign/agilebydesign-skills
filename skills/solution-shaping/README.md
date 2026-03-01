# Solution Shaping

Shape source material into an **Interaction Tree** and **State Model** — a story map and domain model. Guides AI agents when shaping requirements into epics, sub-epics, and stories with associated domain concepts.

## Install

```bash
npx skills add agilebydesign/agilebydesign-skills --skill solution-shaping
```

## When to Use

- Shaping requirements from source documents into a story map
- Deriving epics and stories from user journeys or business flows
- Building an Interaction Tree (hierarchical actor exchanges)
- Modeling domain state concepts (State Model)
- Defining story granularity and slice order

## Rule Categories

| Category | Rules |
|----------|-------|
| Source & Scope | Derive from source, Logical/domain level, Speculation and assumptions |
| Hierarchy | Parent granularity, Sequential order |
| State & Structure | Required state, Resulting state, Failure modes, Concept scoping, Structured concepts |
| Interaction | Supporting actor and Response, Story granularity |

## Structure

- **SKILL.md** — Main entry; when to apply; quick reference
- **AGENTS.md** — Full compiled document (built from rules and content)
- **rules/** — Individual rule files (DO/DO NOT format)
- **content/** — Core definitions, output structure, validation, shaping process
- **scripts/build_agents_md.py** — Build script to regenerate AGENTS.md

## Build

```bash
cd skills/solution-shaping
python scripts/build_agents_md.py
```

## License

MIT
