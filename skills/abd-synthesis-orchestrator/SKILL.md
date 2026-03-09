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

## Workflow (Essential Instructions)

**Lifecycle stages:** shaping → discovery → exploration → specification. Each slice goes through all four stages in order.

**Strategy validation:** (1) Does the strategy make sense from an identification perspective? (2) Does it slice to cover the full domain model? Slices must validate the entire domain (concepts, effects, attributes; commonality or diversity).

**Validation flow:** Run `validate` from the synthesizer skill (includes scanners). Check: (a) run was successful, (b) run produced good content. If not approved → add correction to run log; next run uses corrections as input.

**Re-runs:** When re-running the same stage, use corrections from the previous run as input.

**Output storage:** Per-run files in runs/; consolidated output in interaction-tree.md and state-model.md. Strategy and output are workspace-specific (skill-space); the synthesizer reads from and writes to the workspace.

## Output

All output is in the skill space folder:

- Instructions: `skill-space/story-synthesizer/runs/slice-N-run-M-instructions.md`
- Run logs: `skill-space/story-synthesizer/runs/run-N.md`
- Artifacts: `skill-space/story-synthesizer/interaction-tree.md`, `state-model.md`
