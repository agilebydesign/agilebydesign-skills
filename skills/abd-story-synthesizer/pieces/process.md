# Process Overview

Your task is to **synthesize** context into an **Interaction Tree** and **Domain Model** — a hierarchical structure of meaningful exchanges between actors, plus the domain concepts and state that support them.

See `pieces/interaction.md` for the Interaction Tree data model. 

See `pieces/domain.md` for the Domain Model data model.

Within each phase: **Human** → **AI** invokes script → **Script** returns instructions → **AI** produces output → **Human** updates and adjusts → **AI** incorporates changes. Do not rely on AGENTS.md alone.

---

## Phase 1: Set Work Area and Prepare Context

| Human                                           | AI / Script                                      | AI                                                          | Human → AI                    |
| ----------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------- | ----------------------------- |
| Says "set path", "new workspace", or "continue" | Runs `build.py get_config`, validates context    | Reports paths; checks context readiness; asks if needed     | Confirms or provides new path |

Before starting or continuing work, establish where output goes and ensure context is ready.

**Set path:** Edit `conf/abd-config.json` and set `"skill_space_path": "/path/to/workspace"`. Output goes to `<skill_space_path>/story-synthesizer/`. Context paths are owned by the skill space's `conf/abd-config.json`.

**Get path:** Run `get_config` to see where the skill is currently pointed.

```bash
cd skills/abd-story-synthesizer
python scripts/build.py get_config
```

### Context Readiness

After setting the work area, the engine automatically checks context readiness. Each check cascades — if an earlier step is missing, fix it before proceeding. See `pieces/context.md` for full details on each step.

**1. Chunking** — Are source documents (PDF, PPTX, DOCX) chunked to markdown? `get_instructions` validates automatically. If unchunked or stale → ask user: "Context needs chunking. Set it up?" If yes → run `abd-context-to-memory` pipeline.

**2. Concept Tracking** — Does `terms_report.json` exist? If not → run `concept_tracker.py seed` (optional) → `scan` → `report`.

**3. Concept Deep Analysis** — Has the concept report been reviewed with deep reads of source chunks? If not → for each high-frequency term cluster, read 3–5 representative chunks, extract mechanically distinct categories.

**4. Variation Analysis** — Per model from deep analysis: what's consistent, what varies, what's a story vs example. Saved to `context_analysis.json` under each model's `variation` key.

Each step is run once per workspace. Skip if already done and context hasn't changed.

---

## Phase 3: Start Session


| Human                                        | AI / Script                                       | AI                                             | Human → AI                                 |
| -------------------------------------------- | ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| Says "start a session" or "create a session" | Invokes script `get_instructions create_strategy` | Produces session file with strategy and slices | Updates and adjusts → incorporates changes |


Create, open, or continue an existing session. Name it (user-provided or AI-derived from context). The session file stores strategy: Level of Detail, Scope, Foundational Object Models, Interaction Scaffold, and slices. Variation analysis lives in `context_analysis.json` (from context preparation). Option: carry slices over from a previous session (e.g. Exploration reuses Discovery slices) or create new slices.

**Session path:** `<skill-space>/story-synthesizer/<session-name>/<session-name>-session.md`

**Naming convention:** Session files end with `-session.md`. The session folder `<session-name>/` contains the session file, the first-cut output files (`interaction-tree.md`, `domain-model.md`), and a `runs/` folder for run logs.

The session/strategy declares **tags in scope** (e.g. `discovery`, `interaction_tree`, `stories`, `domain`, `steps`). The engine filters rules by tags. See `pieces/session.md` for session content, slices, discriminators, and tag definitions.

**Session creation is a run (run-0).** Treat it exactly like any other run: produce output, validate with `build.py validate`, fix violations, record corrections in `runs/run-0.md`. The user reviews and corrects strategy, foundational models, variation analysis, and first-cut output files. Run `build.py validate` on `interaction-tree.md` and `domain-model.md` before session creation is considered done. Corrections feed into run 1 — they are not lost.

**Script:**

```bash
python scripts/build.py get_instructions create_strategy
```

---

## Phase 4: Execute a Run


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

**Before starting a run:** Check for unrecorded corrections from session creation or previous runs. If unsure, run `python scripts/build.py get_instructions correct_run` to review the chat for missed corrections.

**Build phase validation:** After producing output, run `build.py validate`. Fix any violations before marking the run complete — validation is part of the build phase. See Phase 3 and `pieces/validation.md`.

---

## Phase 5: Validate


| Human                                                                    | AI / Script                 | AI                                       | Human → AI                                 |
| ------------------------------------------------------------------------ | --------------------------- | ---------------------------------------- | ------------------------------------------ |
| Says "validate", "run validation", "check the output" (or after Phase 1) | Invokes `build.py validate` | Reports violations; fixes if build phase | Updates and adjusts → incorporates changes |


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

## Phase 6: Correct


| Human                                | AI / Script                                    | AI                                          | Human → AI                                 |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews output and gives corrections | Invokes script `get_instructions validate_run` | Applies corrections to run log (may re-run) | Updates and adjusts → incorporates changes |


Human reviews the run output and identifies mistakes. Corrections go to the run's Corrections section in the run log. Each correction must include a DO or DO NOT rule, an example of what was wrong, and the fix. AI may re-run the slice with corrections applied. 

See `pieces/runs.md` § Corrections Format and § When User Gives a Correction.

**Checking for missed corrections:** Run `get_instructions correct_run` to review the chat for unrecorded changes. Run `correct_all` to do the full correction pipeline (run → session → skill) in one shot.

**Script:**

```bash
python scripts/build.py get_instructions validate_run
python scripts/build.py get_instructions correct_run
python scripts/build.py get_instructions correct_all
```

---

## Phase 7 : Adjust


| Human                                        | AI / Script                                        | AI                                          | Human → AI                                 |
| -------------------------------------------- | -------------------------------------------------- | ------------------------------------------- | ------------------------------------------ |
| Reviews corrections, decides what to promote | Invokes script `get_instructions improve_strategy` | Updates session strategy and/or skill rules | Updates and adjusts → incorporates changes |


After all runs (or when the user wants), review corrections collected in run logs (including `run-0.md` from session creation). Determine what needs to change. Incorporate into the session strategy and/or promote to the skill's rules those that apply across projects. The session file is the source of truth.

**When promoting corrections to the skill**, record the fix details in the run log's "Promoted to Skill" section — a table with: Correction, Target file, and Change (a from→to snapshot, not the full diff). This creates a traceable history of why each rule or piece was added or changed.

See `pieces/session.md` § Patterns and `pieces/runs.md` § Patterns.

**Script:**

```bash
python scripts/build.py get_instructions improve_strategy
```

### Three layers of correction

Corrections flow through three layers. Each layer builds on the previous — don't skip ahead, but don't stop at recording either. Be aggressive about suggesting what should change at each layer.


| Layer           | Operation         | Where                                            | What happens                                                                                            |
| --------------- | ----------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **1. Record**   | `correct_run`     | Run log (`runs/run-N.md`)                        | DO/DO NOT captured with wrong/correct examples. The fix is applied to the output files.                 |
| **2. Strategy** | `correct_session` | Session file (`*-session.md`)                    | Correction incorporated into session strategy so future runs in this session follow it.                 |
| **3. Skill**    | `correct_skill`   | Skill rules/pieces (`rules/*.md`, `pieces/*.md`) | Correction promoted to a skill rule or process piece. Recorded in "Promoted to Skill" table in run log. |
| **All**         | `correct_all`     | All three in sequence                            | Runs all three layers: record → strategy → skill.                                                       |


**Don't give up on making changes.** Each layer builds on the previous. Be aggressive in suggestions at every layer — propose the change, let the user decide.

---

## Process Checklist

- **Session created and approved** — session file at `sessions/<session-name>.md` with strategy and slices; user approves before runs start
- **Run 1 produced** — output for first slice; run log written to `sessions/<session-name>/runs/run-1.md`
- **Run 1 approved** — user reviews; corrections to run log; re-run until approved
- **Run 2 … Run N** — each remaining slice: produce → review → corrections → re-run until approved
- **Review and Adjust** — review all corrections in run logs; incorporate into session strategy and/or promote to skill rules

