# Script Invocation

AI guidance for calling ace-shaping scripts.

## build.py get_instructions

Gets the assembled prompt for an operation from the Engine. **Call this before producing any shaping output.**

**When to call:** When the user requests:
- `generate_slice` — "do slice 1", "generate the first slice", "proceed with slice 1", etc.
- `create_strategy` — "create the strategy", "analyze and propose breakdown", etc.
- `improve_strategy` — "improve the strategy based on feedback", etc.

**Usage:**
```bash
cd skills/ace-shaping
python scripts/build.py get_instructions generate_slice
```

**Output:** The assembled prompt (sections + strategy doc + context). **Inject this output into your response and follow it.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths.

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage:**
```bash
cd skills/ace-shaping
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core, process, strategy, output, validation.
