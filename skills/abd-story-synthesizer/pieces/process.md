<!-- section: story_synthesizer.process -->
# Process Overview

Your task is to **synthesize** context into an **Interaction Tree** and **Domain Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them.

See `pieces/interaction.md` for the Interaction Tree data model. 

See `pieces/domain.md` for the Domain Model data model.

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

---

## Phase 1: Set Work Area


| Human                                           | AI / Script                | AI                                           | Human → AI                    |
| ----------------------------------------------- | -------------------------- | -------------------------------------------- | ----------------------------- |
| Says "set path", "new workspace", or "continue" | Runs `build.py get_config` | Reports current paths; sets new if requested | Confirms or provides new path |


Before starting or continuing work, establish where output goes. **New work:** set `skill_space_path` to point to the workspace. **Continue existing work:** get the current path and verify.

**Set path for new work area:** Edit `conf/abd-config.json` and set `"skill_space_path": "/path/to/workspace"` (e.g. mm3e). Output goes to `<skill_space_path>/story-synthesizer/`.

**Get path to continue:** Run `get_config` to see where the skill is currently pointed.

**Script:**

```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_config
```

**Output:** JSON with `engine_root`, `skill_space_path` (and `skill_path` as shorthand), `config_path`, and optionally `strategy_path`, `context_paths`. The script returns resolved paths from `conf/abd-config.json`.

---

## Phase 2: Start Session


| Human                                        | AI / Script                                       | AI                                             | Human → AI                                 |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| Says "start a session" or "create a session" | Invokes script `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts → incorporates changes |


Create, open, or continue an existing session. Name it (user-provided or AI-derived from context). The session file stores strategy: Level of Detail, Scope, Variation Analysis, and slices. Option: carry slices over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

**Session path:** `<skill-space>/story-synthesizer/sessions/<session-name>.md`

The session/strategy declares **tags in scope** (e.g. `discovery`, `interaction_tree`, `stories`, `domain`, `steps`). The engine filters rules by tags. See `pieces/session.md` for session content, slices, discriminators, and tag definitions.

**Script:**

```bash
python scripts/build.py get_instructions create_strategy
```

---

## Phase 3: Execute a Run


| Human                                                             | AI / Script                                 | AI                                | Human → AI                                 |
| ----------------------------------------------------------------- | ------------------------------------------- | --------------------------------- | ------------------------------------------ |
| Says "proceed," "build it," "run slice", "next run", "next slice" | Invokes script `get_instructions run_slice` | Produces run output for the slice | Updates and adjusts → incorporates changes |


Slices are completed through a run. One run per slice. A run may require multiple iterations (user reviews → corrections to run log → re-run) until approved. Corrections carry forward: run 2 applies corrections from run 1; run 3 applies corrections from runs 1 and 2.

**Output path:** `<skill-space>/story-synthesizer/` — Interaction Tree and Domain Model (format in `output/interaction-tree-output.md` and `output/domain-model-output.md`). **Run logs:** `<skill-space>/story-synthesizer/sessions/<session-name>/runs/run-N.md`

See `pieces/session.md` for slices. See `pieces/runs.md` for run lifecycle, run log structure, and corrections format.

**Script:**

```bash
python scripts/build.py get_instructions run_slice [--strategy path/to/strategy.md]
```

**You MUST call `get_instructions` before producing any synthesis output.** The Engine assembles the correct sections, strategy, and paths. Never proceed without calling it first.

**Build phase validation:** After producing output, run `build.py validate`. Fix any violations before marking the run complete — validation is part of the build phase. See Phase 4 and `pieces/validation.md`.

---

## Phase 4: Validate


| Human                                                                    | AI / Script                 | AI                                       | Human → AI                                 |
| ------------------------------------------------------------------------ | --------------------------- | ---------------------------------------- | ------------------------------------------ |
| Says "validate", "run validation", "check the output" (or after Phase 2) | Invokes `build.py validate` | Reports violations; fixes if build phase | Updates and adjusts → incorporates changes |


Run `build.py validate` (or `validate <path>`) to execute rule scanners. Report any violations. Validation behavior depends on scope and context:

### Validate Run

Validate **only the output of the current run**. Ignore previous work. Use when the user says "validate our run" or "check what we just did." **Fix violations before marking the run complete** — this is part of the build phase.

### Validate Slice

Validate **everything in the slice** — all accumulated output for that slice. Use when the user says "validate the slice" or "validate slice 1." **Fix violations before marking the run complete** — this is part of the build phase.

### Explicit Validate (User Request Only)

When the user **explicitly asks to validate** (e.g. "validate", "run validation", "check the output") **outside a build phase** — do **not** fix violations. Run validate, report violations, and leave with the reviewer. Do not edit files unless you are in a build phase (run_slice, validate_run, validate_slice).

See `pieces/validation.md` for the full validation checklist.

**Script:**

```bash
python scripts/build.py validate
python scripts/build.py validate path/to/interaction-tree.md
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions validate_slice
```

---

## Phase 5: Correct


| Human                                | AI / Script                                    | AI                                          | Human → AI                                 |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews output and gives corrections | Invokes script `get_instructions validate_run` | Applies corrections to run log (may re-run) | Updates and adjusts → incorporates changes |


Human reviews the run output and identifies mistakes. Corrections go to the run's Corrections section in the run log. Each correction must include a DO or DO NOT rule, an example of what was wrong, and the fix. AI may re-run the slice with corrections applied. 

See `pieces/runs.md` § Corrections Format and § When User Gives a Correction.

**Script:**

```bash
python scripts/build.py get_instructions validate_run
```

---

## Phase 6: Adjust


| Human                                        | AI / Script                                        | AI                                          | Human → AI                                 |
| -------------------------------------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews corrections, decides what to promote | Invokes script `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts → incorporates changes |


After all runs (or when the user wants), review corrections collected in run logs. Determine what needs to change. Incorporate into the session strategy and/or promote to the skill's rules those that apply across projects. The session file is the source of truth. 

See `pieces/session.md` § Patterns and `pieces/runs.md` § Patterns.

**Script:**

```bash
python scripts/build.py get_instructions improve_strategy
```

---

## Process Checklist

- [ ] **Session created and approved** — session file at `sessions/<session-name>.md` with strategy and slices; user approves before runs start
- [ ] **Run 1 produced** — output for first slice; run log written to `sessions/<session-name>/runs/run-1.md`
- [ ] **Run 1 approved** — user reviews; corrections to run log; re-run until approved
- [ ] **Run 2 … Run N** — each remaining slice: produce → review → corrections → re-run until approved
- [ ] **Review and Adjust** — review all corrections in run logs; incorporate into session strategy and/or promote to skill rules
