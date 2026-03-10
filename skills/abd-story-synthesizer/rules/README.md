# Rules

Discovery, identification, and validation rules for the story synthesizer. Rules are Markdown files with YAML frontmatter.

**Rule format:** Each rule has a **DO** with example and a **DO NOT** with example.

## Tag format (required)

Each rule **must** have YAML frontmatter with `tags`:

```yaml
---
title: Rule name
impact: HIGH | MEDIUM | LOW
tags: [discovery, interaction_tree, story, domain]
---
```

**Tag set:** `discovery`, `exploration`, `specification`, `interaction_tree`, `stories`, `domain`, `steps`, `steps_edge_cases`, `examples`, `scenarios`

Use the tags that apply to the rule. Include a rule if any of its tags matches any tag the session/strategy declares in scope. Session type (Discovery, Exploration, Specification) determines scope; see `pieces/session.md` Session Types table.

**Validation is scoped to what you synthesize.** All runs get validated, but the rules injected depend on tags in scope — domain rules for domain output, step rules for steps, example rules for examples, etc. The engine filters rules by strategy tags so only relevant rules are injected.

## How to get rules injected

**You MUST call the build script** — rules are not in AGENTS.md alone. The Engine assembles sections and injects rules when you run:

```bash
cd <skill-root>/abd-story-synthesizer
python scripts/build.py get_instructions create_strategy
python scripts/build.py get_instructions run_slice [--strategy path/to/strategy.md]
```

| Operation       | When to use                          | Injects rules |
|----------------|--------------------------------------|----------------|
| `create_strategy` | Strategy phase, identification criteria | Yes            |
| `run_slice`       | Runs, slice output                   | Yes            |
| `generate_slice`  | Alias for run_slice                   | Yes            |
| `correct_run`     | Record missed corrections to run log  | No             |
| `correct_session` | Incorporate corrections into strategy | No             |
| `correct_skill`   | Promote corrections to skill rules    | No             |
| `correct_all`     | All three correction layers in sequence | No           |
| `validate_run`    | Validate current run output           | Yes            |
| `validate_slice`  | Validate slice output                 | Yes            |

**Do not skip this step.** The AI must run `get_instructions` and inject its output before producing any synthesis output. Rules are included automatically when the operation includes `story_synthesizer.validation.rules`.

## Validation scanners

Rules with frontmatter `scanner: <name>` are used by `python scripts/build.py validate` to run rule-based checks on the interaction tree and Domain Model. See `scripts/scanners/` for implementations.
