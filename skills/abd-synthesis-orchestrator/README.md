# abd-synthesis-orchestrator

Drives the synthesis workflow (create_strategy → run_slice → validate → correct) using abd-story-synthesizer. Integrates the synthesizer's three-layer self-correction pipeline, archives session output for history, and optionally version-controls skill changes on a git branch with rollback on regression.

## Run

```bash
python C:\dev\agilebydesign-skills\skills\abd-synthesis-orchestrator\scripts\run_orchestrator.py --skill-space <path-to-skill-space>
```

### With self-correction and version control

```bash
python scripts/run_orchestrator.py --skill-space C:/dev/mm3e --correct-level all --branch orchestrator
```

### Key features

- **Self-correction pipeline**: `--correct-level run|session|skill|all` — captures corrections in run logs, folds into session strategy, and promotes to skill rules
- **Session archival**: copies output to `C:\dev\synchronizer_runs` at end of session (configurable via `--archive-dir`)
- **Skill version control**: `--branch <name>` commits skill improvements, rolls back on regression

See [SKILL.md](./SKILL.md) for all options.
