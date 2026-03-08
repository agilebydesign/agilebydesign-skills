# Script Invocation

AI guidance for calling abd-story-synthesizer scripts.

## Two-phase flow

1. **Create strategy** — Analyze source, propose Epic/Story breakdown and **slices**, save to `strategy.md`. Do not produce output until approved.
2. **Perform runs** — Each run produces output for a slice. Runs iterate (user reviews → corrections to run log → re-run) until approved. Then next slice.

## Strategy passed into API

The strategy is **passed into the API** (not just embedded in markdown). The strategy declares a **collection of components** to render: `epic`, `story`, `step`, `scenario`, `examples`, `domain_concept`. The engine uses those components to filter rules — only rules tagged for in-scope components are included. See `content/rules-tagging-proposal.md` for component-based filtering.

**Bespoke strategies:** A custom strategy can mix components (e.g. discovery + mapping to stories + domain concepts + examples at sub-epic level). Examples can be scoped at different levels — the strategy defines where.

## build.py get_instructions

Gets the assembled prompt for an operation from the Engine. **Call this before producing any shaping output.** The strategy (path or content) is passed in; the engine parses it for components and filters rules accordingly.

**When to call:**

| Operation | User says | Notes |
|-----------|-----------|-------|
| `create_strategy` | "create the strategy", "analyze and propose breakdown", "propose slices" | Produces strategy with slices. No output until approved. |
| `run_slice` | "do slice 1", "run slice 2", "proceed with slice 1", "re-run slice 1" | Performs a run on a slice. Strategy passed in; components drive rule filtering. Use `generate_slice` if that alias is configured. |
| `validate_run` | "validate our run", "check what we just did" | Validate only the output of the current run. Ignores previous work. |
| `validate_slice` | "validate the slice", "validate slice 1", "check the slice" | Validate everything in the slice — all accumulated output for that slice. |
| `improve_strategy` | "improve the strategy based on feedback" | Refines strategy before runs. |

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_instructions create_strategy
python scripts/build.py get_instructions run_slice [--strategy path/to/strategy.md]
```

**With custom skill space (e.g. mm3e):**
```bash
python scripts/build.py get_instructions create_strategy --engine-root C:\dev\agile_bot_demos\mm3e
python scripts/build.py get_instructions run_slice --engine-root C:\dev\agile_bot_demos\mm3e [--strategy path/to/strategy.md]
```
Output goes to `<engine-root>/story-synthesizer/` (strategy.md, runs/, interaction-tree.md, state-model.md). Ensure `conf/abd-config.json` exists at engine-root with `skill_space_path` and `skills` configured.

**Output:** The assembled prompt (sections + strategy doc + context). Rules are filtered by the strategy's in-scope components. **Inject this output into your response and follow it.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths.

## build.py validate

Runs rule-based scanners on the interaction tree and state model. Scanners are defined in `rules/*.md` (frontmatter `scanner:` field) and implemented in `scripts/scanners/`. Uses regex and native Python only; optional grammar/AST when deps available.

**Scanner mode:** With NLTK (grammar) or mistune (AST) installed, scanner mode is **full**. Without them, the scanner runs automatically in **nerfed** mode (regex-only checks). The validate command prints `Scanner mode: full` or `Scanner mode: nerfed` at startup.

**When to call:** After producing or updating interaction tree or state model output. Use when the user says "validate" or "run validation" or "check the output."

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py validate
python scripts/build.py validate path/to/interaction-tree.md
python scripts/build.py validate --engine-root C:\dev\agile_bot_demos\mm3e
```

**Output:** Prints violations (rule_id, message, location, snippet). Exit code 0 always — violations are reported so the AI can create a violation report or fix them during a build phase.

**AI behavior:**
- **Build phase** (validate_run, validate_slice as part of run_slice): Report violations and fix them before marking complete.
- **Explicit validate** (user said "validate" outside a build): Report violations only. Do not fix — leave with reviewer. Do not edit files in front of the user unless in a build phase.

## build.py

Assembles content/*.md into AGENTS.md.

**When to call:** After content pieces are filled (or when regenerating AGENTS.md).

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py
```

**Output:** Writes `AGENTS.md` with merged content in order: core, process, strategy, output, validation.

---

## Script change recommendations

See `content/script-changes.md` for full analysis of where scripts need to change.
