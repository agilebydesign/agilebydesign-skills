# Core Definitions

## Ace-Skill

An ace-skill is a structured skill with:
- **content/** — Markdown: core, process, strategy, output, validation
- **rules/** — DO/DO NOT rules, scanners (JSON)
- **scripts/** — Build script (and scaffold for agile-skill-build)
- **AGENTS.md** — Assembled output (built from content)

## Agile Skill Build (agile-skill-build)

The skill that creates and scales ace-skills. Provides scaffold and build scripts that delegate to the engine.

---

# Ace-Build Process

Build new ace-skills. Use when the user wants to create a skill with the standard ace-skill structure.

## Process

1. **Scaffold** — Run `scaffold.py --name ace-<name>` to create the directory.
2. **Fill content** — AI or user fills core, process, strategy, output, validation from markdown/prompts/text.
3. **Complete gaps** — If pieces are missing, user completes them.
4. **Build** — Run `build.py` to assemble AGENTS.md.

When creating an ace-skill:

1. User provides markdown, prompts, or text describing the skill.
2. AI uses Build-ACE to scaffold (if new) or identifies target skill.
3. AI fills content pieces from input. If insufficient, report gaps.
4. User completes missing pieces.
5. AI reruns build when all pieces are complete.

---

# Strategy

For ace-build, strategy is implicit: scaffold → fill content → build. No separate strategy phase.

---

# Output Structure

After build, the skill contains:

- **AGENTS.md** — Merged content for agent consumption
- **metadata.json** — Skill metadata
- **SKILL.md** — Skill descriptor
- **README.md** — Usage instructions

Content merge order: core → process → strategy → output → validation.

---

# Validation

Before considering the skill complete:

- [ ] All content pieces filled (core, process, strategy, output, validation)
- [ ] build.py runs without error
- [ ] AGENTS.md produced and non-empty
- [ ] metadata.json has name and version

---

# Script Invocation

AI guidance for calling Agile Skill Build scripts. Run from `agilebydesign-skills` root.

## scaffold.py

Creates a new ace-skill directory with content/, rules/, scripts/.

**When to call:** When the user wants to create a new ace-skill.

**Usage:**
```bash
python skills/agile-skill-build/scripts/scaffold.py --name ace-<name> [--path skills/ace-<name>]
```

**Parameters:**
- `--name` (required): Skill name, e.g. `ace-foo`, `ace-shaping`
- `--path` (optional): Output path. Default: `skills/<name>` relative to repo root.

**Example:**
```bash
python skills/agile-skill-build/scripts/scaffold.py --name ace-foo
```

**Output:** Creates `skills/ace-foo/` with content/, rules/, scripts/, and standard files.

---

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage (from agile-skill-build itself):**
```bash
cd skills/agile-skill-build
python scripts/build.py
```

**Usage (from any scaffolded skill):**
```bash
cd skills/ace-<name>
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core, process, strategy, output, validation.

**Sequencing:** Run scaffold first → fill content → run build when complete.

---
