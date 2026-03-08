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
- `--path` (optional): Output path. Default: `skills/<name>` relative to engine root.

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
