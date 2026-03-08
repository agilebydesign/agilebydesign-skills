# Core Definitions

## Ace-Skill

An ace-skill is a structured skill with:
- **content/** — Markdown: core, process, strategy, output, validation
- **rules/** — DO/DO NOT rules, scanners (JSON)
- **scripts/** — Build script (and scaffold for agile-skill-build)
- **AGENTS.md** — Assembled output (built from content)

## Agile Skill Build (agile-skill-build)

The skill that creates and scales ace-skills. Provides scaffold and build scripts that delegate to the engine.
