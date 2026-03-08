---
name: agile-skill-build
description: Agile Skill Build — Create and scale ace-skills. Scaffold new skills and assemble content into AGENTS.md. Use when creating or scaling a skill with the standard ace-skill structure.
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# Agile Skill Build

Create and scale ace-skills. Scaffold creates the directory; build assembles content into AGENTS.md.

## When to Use

- User wants to create a new ace-skill
- User has markdown/prompts describing the skill
- Regenerating AGENTS.md after content changes

## Scripts

- **scaffold.py** — `--name ace-<name>` creates the skill directory
- **build.py** — Assembles content → AGENTS.md

See `content/script-invocation.md` for params and sequencing.
