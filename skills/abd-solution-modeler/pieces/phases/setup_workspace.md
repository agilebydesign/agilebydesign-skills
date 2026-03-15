# Phase 0 — Setup Workspace

**Actor:** Code | **Full spec:** [requirements.md](../../docs/requirements.md) § Phase 0

## Purpose

Set solution workspace, resolve context location, and create the solution sub directory where all pipeline outputs go.

## Trigger

setup workspace, create solution dir, init solution, init workspace

## Inputs

- `conf/abd-config.json` — `solution_workspace`, `output_dir`
- Workspace root (current working directory) — fallback when config is empty

## Instructions

1. Read `conf/abd-config.json` for `solution_workspace` and `output_dir`
2. If `solution_workspace` is set, use it; else use current working directory
3. Create solution sub dir: `solution_workspace / output_dir`
4. Write `solution_dir_path` to config or a manifest so downstream phases know where to put files
5. Create `.gitkeep` or `README.md` in the solution dir so it is tracked

## Outputs

- Solution directory created at `{solution_workspace}/{output_dir}`
- `{solution_dir}/.solution-workspace` — one-line file with the absolute path (for AI phases to read)

## Run

```bash
python scripts/pipeline.py run 0
```

Or with override:

```bash
python scripts/setup_workspace.py --workspace <path> --output-dir <name>
```

Script: `scripts/setup_workspace.py`
