---
name: abd-synthesis-orchestrator
description: Drives the synthesis workflow (create_strategy, run_slice, validate) using abd-story-synthesizer. Use when running orchestrated story synthesis, shaping content into interaction tree and state model, or when the user asks to run the synthesis orchestrator.
---

# Synthesis Orchestrator

Drives the full synthesis flow: create_strategy -> run_slice (per slice) -> validate. Uses abd-story-synthesizer for instructions and validation. Supports checkpointing and stop-on-repeated-errors.

## When to Apply

- User asks to run the synthesis orchestrator
- User wants to orchestrate story synthesis from source material
- User mentions "run orchestrator", "synthesis workflow", or "synthesis orchestrator"

## CRITICAL: Orchestrator as Single Entry Point

**When the orchestrator is active, all instructions for the synthesizer MUST go through the orchestrator to the agent.**

- Do NOT create `strategy.md`, `interaction-tree.md`, or `state-model.md` yourself.
- Do NOT run `build.py get_instructions` directly and hand output to the agent.
- The orchestrator generates instructions and saves them to `runs/slice-N-run-M-instructions.md` (or create_strategy instructions). The agent receives those instructions from the orchestrator's output.
- Flow: Orchestrator → instructions file → Agent. Never bypass the orchestrator.

## Prerequisites

- Synthesizer skill (abd-story-synthesizer) installed
- Skill space folder set to a folder that exists

  Run with `--skill-space <path>`: `python scripts/run_orchestrator.py --skill-space C:/dev/agile_bots_demo/mm3e`

## Config Location (IMPORTANT)

**abd-config.json MUST live in the synthesizer skill, NOT in the skill space.**

| Location | Contains | Config? |
|----------|----------|---------|
| `abd-story-synthesizer/conf/abd-config.json` | Engine config (skills, context_paths, skill_space_path) | **YES** — config goes here |
| Skill space (e.g. `mm3e/`) | Content to synthesize (goal.md, context/, docs/) | **NO** — never put abd-config in the skill space |

The skill space is the workspace/content root. The engine reads config from the synthesizer skill and uses `skill_space_path` in that config to find the workspace. 

## Run the Orchestrator

From abd-synthesis-orchestrator:

```bash
cd .../agilebydesign-skills/skills/abd-synthesis-orchestrator
python scripts/run_orchestrator.py --skill-space <path-to-skill-space>
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--skill-space` | required | Path to skill space folder; orchestrator passes to synthesizer (orchestrator does not set it) |
| `--slice N` | all | Run only slice N (1-based) |
| `--checkpoint` | stage | When to pause: never, stage, slice, run |
| `--max-consecutive-failures` | 3 | Stop after N consecutive validation failures |
| `--max-inner-iterations` | 5 | Max validate->correct->re-run iterations per slice |
| `--stop-on-correction` | off | Exit immediately on first validation failure; fix and re-run |
| `--strategy-only` | off | Stop after strategy creation (test run); skip slice runs |
| `--test-mode` | off | Stop at every step; prompt accepts N to do N runs then exit; state persisted for resume |
| `--max-runs N` | - | (test-mode) Max runs this session; then exit and save state for resume |
| `--correct-level` | run | Correction depth on failure: none, run, session, skill, all |
| `--archive-dir` | `C:\dev\synchronizer_runs` | Directory to archive session output at end |
| `--no-archive` | off | Skip session archival at end |
| `--branch NAME` | - | Git branch for skill version control; commits on pass, rolls back on regression |
| `--no-rollback` | off | Disable automatic rollback of skill changes when output degrades |

### Typical Workflow

1. Run with default checkpoint (stage): orchestrator pauses after each slice for human verification
2. At checkpoint: run agent with saved instructions in `skill-space/story-synthesizer/runs/slice-N-run-M-instructions.md`
3. Press Enter to continue after agent produces output
4. Use `--checkpoint never` for fully automated runs (e.g. CI)

### Test Mode (sync run with agent tracking)

1. Run `--test-mode`: stops at every step (create_strategy, each run_slice, each validate)
2. At each checkpoint: run agent, then press Enter to continue 1 run, or type a number (e.g. 5) to do N runs then exit
3. State is saved to `skill-space/story-synthesizer/runs/orchestrator-state.json` when you exit
4. Re-run with `--test-mode` to resume from where you left off
5. Use `--max-runs N` to do N runs then exit (e.g. agent says "proceed with 3 runs" → `--max-runs 3`)

## Self-Correction Pipeline

The orchestrator integrates with the synthesizer's three-layer correction system. Use `--correct-level` to control depth:

| Level | What happens on validation failure |
|-------|------------------------------------|
| `none` | No correction — just log and re-run |
| `run` (default) | `correct_run`: capture DO/DO NOT in run log with wrong/correct examples |
| `session` | `run` + `correct_session`: fold corrections into session strategy for future runs |
| `skill` | `run` + `session` + `correct_skill`: promote corrections to skill rules (cross-project) |
| `all` | All three layers in one shot |

Correction instructions are saved to `runs/slice-N-run-M-corrections.md` alongside the run instructions.

## Session Archival

At the end of every session, the orchestrator copies the `story-synthesizer/` output to an archive directory for history. Default: `C:\dev\synchronizer_runs\<skill-space-name>\<timestamp>\`.

- Use `--archive-dir <path>` to change the archive location
- Use `--no-archive` to skip archival

## Skill Version Control

Use `--branch <name>` to enable git-based version control for the synthesizer skill:

1. On validation **pass** with `--correct-level skill` or `all`: skill changes are committed to the branch
2. On validation **fail** with `--rollback-on-regression`: skill changes are rolled back to the pre-correction state
3. Use `--no-rollback` to keep skill changes even when output degrades (for manual review)

Typical usage:

```bash
python scripts/run_orchestrator.py --skill-space C:/dev/mm3e --correct-level all --branch orchestrator
```

This creates a traceable history of skill evolution driven by session corrections.

## Workflow (Essential Instructions)

**Lifecycle stages:** shaping → discovery → exploration → specification. Each slice goes through all four stages in order.

**Strategy validation:** (1) Does the strategy make sense from an identification perspective? (2) Does it slice to cover the full domain model? Slices must validate the entire domain (concepts, effects, attributes; commonality or diversity).

**Validation flow:** Run `validate` from the synthesizer skill (includes scanners). On failure, the correction pipeline runs automatically at the configured level (`--correct-level`). Correction instructions are saved for the agent.

**Re-runs:** When re-running the same stage, use corrections from the previous run as input.

**Output storage:** Per-run files in runs/; consolidated output in interaction-tree.md and state-model.md. Strategy and output are workspace-specific (skill-space); the synthesizer reads from and writes to the workspace.

## Output

All output is in the skill space folder:

- Instructions: `skill-space/story-synthesizer/runs/slice-N-run-M-instructions.md`
- Run logs: `skill-space/story-synthesizer/runs/run-N.md`
- Artifacts: `skill-space/story-synthesizer/interaction-tree.md`, `state-model.md`
