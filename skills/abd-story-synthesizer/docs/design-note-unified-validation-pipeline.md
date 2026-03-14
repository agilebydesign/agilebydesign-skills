# Design Note: Unified Validation Pipeline

## Goal

Merge AI model validation (Steps 8–10) with rule-based scanners into one pipeline: deterministic order, single validation log, fix-by-default (report-only when requested). "Fix validations" means apply both AI pass findings and scanner findings.

## Current Gap

- **AI pass** (scenario walkthrough, anemia critique, base/inheritance check): Produces `run-N-validation.md` but is not wired into `build.py validate`. When user says "fix validations," AI often ignores AI pass output.
- **Scanners**: Run on `build.py validate`; violations printed to stdout only. No single log; no fix vs report mode.
- **Rules**: Injected as guidance and have scanners, but AI pass content lives in `pieces/ai_passes.md` — not in rules.

## Proposed Architecture

### 1. Rules Own Everything

- **Fold AI pass into rules.** Steps 8–10 become rules (or rule clusters) in `rules/`:
  - `domain-model-validation-scenario-walkthrough` — scenario/message walkthrough
  - `domain-model-validation-anemia-critique` — anemia, centralization, data bags
  - `domain-model-validation-base-inheritance` — shared protocol, missing bases (e.g. CharacterTrait)

- **Each rule has:**
  - `order` — deterministic execution order (lower = run first). Explicit only; tags do not imply order.
  - `tags` — e.g. `[foundational, domain, discovery]` for scoping (which rules apply to session), not order.
  - `type` — `ai_pass` | `scanner` (or `scanner` only if a scanner exists)
  - `scanner` — scanner name when automatable

- **Tags = scope only.** They filter which rules run for a session type. Order is explicit per rule (`order: 1`, `order: 2`, …).

### 2. Single Validation Log: `run-N-validation.md`

All findings (AI pass + scanners) go into one log. Format:

```markdown
# Run N — Validation

## Phase 1: AI Pass (order 100–199)

### Step 8: Scenario / Message Walkthrough
- [ ] Pass / Correction
- Finding: ...

### Step 9: Anemia / Centralization Critique
- [ ] Pass / Correction
- Finding: ...

### Step 10: Base and Inheritance Check
- [ ] Pass / Correction
- **Correction:** Add CharacterTrait base; AbilityRank, Defense, Skill, Advantage extend it.

## Phase 2: Scanners (order 200+)

| rule_id | severity | message | location | status |
|---------|----------|---------|----------|--------|
| verb-noun-format | WARN | ... | L42 | fixed |
| domain-sync | ERROR | ... | domain-model.md | pending |

## Summary
- Total findings: N
- Fixed: M
- Pending: K
- Mode: fix | report
```

### 3. Execution Flow

```
1. Resolve rules by scope (strategy tags) → ordered list by order
2. Split into ai_pass rules vs scanner rules (by type or scanner presence)
3. Run AI pass first (invoke get_instructions for each ai_pass rule, or batch as model_validation)
   → AI produces findings → append to run-N-validation.md
4. Run scanners in order
   → Append violations to same log
5. Apply fixes (unless --report-only)
   → Default: fix. During build: always fix.
   → Report mode: write log only, do not edit files
```

### 4. Fix vs Report Mode

| Context | Default | Flag |
|---------|---------|------|
| `build.py validate` during run_slice/build | **fix** | — |
| `build.py validate` standalone | **fix** | — |
| User says "validate, report only" / "just report" | report | `--report-only` |

- **Fix mode**: Write log, then AI (or human) applies corrections. Re-validate until clean or user stops.
- **Report mode**: Write log only. No edits. User reviews and fixes manually.

### 5. Rule Frontmatter (Extended)

```yaml
---
title: Base and Inheritance Check
impact: HIGH
tags: [foundational, domain]
order: 110
type: ai_pass
scanner: null  # or e.g. domain_base_inheritance when scanner exists
---
```

For rules with both AI guidance and a scanner: `type: ai_pass` + `scanner: domain_base_inheritance`. AI pass runs first (produces narrative findings); scanner runs later (produces structured violations). Both append to the same log.

### 6. Implementation Phases

**Phase A: Log unification**
- `build.py validate` writes to `runs/run-N-validation.md` (or session-scoped path)
- Scanners append to log in order
- Add `--report-only` flag; default remains fix
- Add `--output path` to specify log location

**Phase B: Explicit order**
- Add `order` to rule frontmatter (or scanners.json)
- Registry sorts rules by `order` before execution
- Tags stay for scoping only; they do not affect execution order

**Phase C: AI pass as rules**
- Create rules for Steps 8, 9, 10 in `rules/`
- `get_instructions model_validation` becomes "run AI pass rules in order"
- AI pass output appended to same validation log
- When "fix validations": instructions include "read run-N-validation.md; apply all findings; re-validate"

**Phase D: Scanners for AI-pass checks (where possible)**
- e.g. "CharacterTrait base exists when AbilityRank, Defense, Skill, Advantage exist" → `domain_base_inheritance` scanner
- Scanner runs after AI pass; catches cases AI missed or confirms AI findings

### 7. "Fix Validations" Instructions

When user says "fix validations," the injected instructions must include:

1. Read `runs/run-N-validation.md` (latest run)
2. Apply all findings (AI pass + scanner) to domain-model, interaction-tree, diagrams
3. Re-run `build.py validate` (no --report-only)
4. Iterate until clean or user stops

This ensures both AI pass and scanner output are in scope.

## Open Questions

- Where does run-N come from when validating outside a run? (Latest run in session, or require `--run N`.)
- Should AI pass rules be batched (one LLM call for 8+9+10) or separate? (Batching saves cost; separation allows finer ordering.)
