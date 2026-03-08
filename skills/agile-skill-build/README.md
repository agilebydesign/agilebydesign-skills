# Agile Skill Build

Create and scale ace-skills with the standard structure. Delegates to the Agile Context Engine.

## Scaffold

From `agilebydesign-skills` root:

```bash
python skills/agile-skill-build/scripts/scaffold.py --name ace-foo
```

Creates `skills/ace-foo/` with content/, rules/, scripts/.

## Build

```bash
cd skills/agile-skill-build
python scripts/build.py
```

**If `python` fails** with "The file cannot be accessed by the system" or "The system cannot execute the specified program":

Your `python` is likely the Windows Store stub (`WindowsApps\python.exe`), which often breaks. **Fix:** Install Python from [python.org](https://python.org) (not the Store), and check "Add Python to PATH" during install. This gives you a real `python.exe` that works.

Assembles content/*.md into AGENTS.md.

## Process

1. Scaffold (or use existing skill)
2. Fill content pieces from markdown/prompts
3. Run build when complete
