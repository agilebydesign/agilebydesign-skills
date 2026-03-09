# Script Invocation

AI guidance for calling abd-story-synthesizer scripts.

## Strategy and runs

1. **Iterative Strategy** — Strategy runs through every run. First run: create strategy document, build tree and Domain Model, spot patterns. Create output as you go — do not wait for approval before producing tree and Domain Model.
2. **Perform runs** — Each run produces output for a slice. Runs iterate (user reviews → corrections to run log → re-run) until approved. Then next slice. Every run examines all runs for new patterns; if found, add to strategy.

## Strategy passed into API

The strategy is **passed into the API** (not just embedded in markdown). The strategy declares **tags in scope** — e.g. `shaping`, `discovery`, `interaction_tree`, `stories`, `domain`, `steps`, etc. The engine filters rules by tags: include a rule if any of its tags matches any in-scope tag. Strategy can declare by mode, component, or explicitly — tags do everything. See `content/rules-tagging-proposal.md` and strategy section "1 - Comprehensiveness Criteria and Tags in Scope".

**Bespoke strategies:** A custom strategy can mix components (e.g. discovery + mapping to stories + domain concepts + examples at sub-epic level). Examples can be scoped at different levels — the strategy defines where.

## build.py get_instructions

Gets the assembled prompt for an operation from the Engine. **You MUST call this before producing any shaping output.** Do not rely on AGENTS.md alone — run the command and inject its output. The strategy (path or content) is passed in; the engine parses it for components and filters rules accordingly.

**Rules injection:** Operations that include `story_synthesizer.validation.rules` (create_strategy, run_slice, generate_slice, validate_run, validate_slice) inject rules from `rules/*.md` **filtered by tags in scope**. All runs get validated, but validation uses different rules depending on what you synthesize — domain rules for domain output, step rules for steps, example rules for examples, etc. Rules are injected based on the strategy's declared tags. Each rule must have YAML frontmatter with `tags: [shaping, discovery, interaction_tree, story, domain, ...]`. See `rules/README.md` for the full tag set.

**When to call:**

| Operation | User says | Notes |
|-----------|-----------|-------|
| `create_strategy` | "build a strategy", "create the strategy", "analyze and propose breakdown", "propose slices" | Produces strategy with slices and builds tree/state model. Injects shaping rules (`rules/`) so the agent applies them. Creates output as you go. |
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

**Skill space:** Set `skill_space_path` in `conf/abd-config.json` to point to your workspace (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/` (strategy.md, runs/, interaction-tree.md, domain-model.md). Engine root is always the synthesizer skill — no CLI param.

**Output:** The assembled prompt (sections + strategy doc + context). Rules are filtered by the strategy's in-scope components. **You MUST run this command and inject its output into your response.** Do not skip this step — the Engine assembles the correct sections, strategy, and paths. Never proceed without calling it first.

## build.py validate

Runs rule-based scanners on the interaction tree and Domain Model. Scanners are defined in `rules/*.md` (frontmatter `scanner:` field) and implemented in `scripts/scanners/`. Uses regex and native Python only; optional grammar/AST when deps available.

**Scanner mode:** With NLTK (grammar) or mistune (AST) installed, scanner mode is **full**. Without them, the scanner runs automatically in **nerfed** mode (regex-only checks). The validate command prints `Scanner mode: full` or `Scanner mode: nerfed` at startup.

**When to call:** After producing or updating interaction tree or Domain Model output. Use when the user says "validate" or "run validation" or "check the output."

**Usage:**
```bash
cd skills/abd-story-synthesizer
python scripts/build.py validate
python scripts/build.py validate path/to/interaction-tree.md
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
