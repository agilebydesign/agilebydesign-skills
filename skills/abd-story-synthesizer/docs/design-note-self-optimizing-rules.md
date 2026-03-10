# Design Note: Self-Optimizing Rules and Scanners

## Problem

Rules guide synthesis and scanners validate output, but there's no feedback loop. A rule that keeps failing wastes the user's time with corrections. A scanner that never catches anything wastes compute. A rule prompt that doesn't prevent the violation it's supposed to prevent is a weak rule — but nobody tracks this.

## Vision

Every aspect of the skill — not just synthesis output but process steps too (did you create run-0? did you record corrections properly? did you use the right naming convention?) — should be validated by rules with scanners. Scanner results feed back into rule quality, creating a self-optimizing skill.

## Feedback Loop

```
Rule → Scanner → Result History → Optimization Decision → Rule/Scanner Update
```

1. **Everything is a rule.** Not just "use verb-noun format" but also "create run-0.md during session creation," "record corrections with DO/DON'T format," "use -session suffix for session files," "produce first-cut output files not inline scaffolds."

2. **Every rule has a scanner.** Each scanner detects violations of its rule in the output (interaction tree, domain model, session file, run logs).

3. **Track results per rule per session.** Build a history:

```
RuleResult
- String ruleId
- String sessionId
- String runId
- Boolean passed
- String violationSnippet (when failed)
- String scannerUsed
- Number catchCount (scanner catches per session)
- Number failCount (rule failures per session — user corrections for this rule)
```

4. **Optimize dynamically based on history:**

| Signal | Meaning | Action |
|---|---|---|
| failCount high + catchCount low | Scanner is weak — doesn't detect the problem | Improve scanner logic |
| failCount high + catchCount high | Rule prompt is weak — AI reads it but still violates | Rewrite the DO/DON'T, add more examples, increase injection weight |
| failCount zero across N sessions | Rule is well-learned — AI consistently follows it | Reduce injection priority (don't inject every time, save context window) |
| catchCount zero across N sessions | Scanner never finds anything | Disable scanner for that rule (reduce noise and runtime) |
| failCount spikes after rule change | Rule change made things worse | Revert or revise the change |

## Orchestrator Agent

An orchestrator skill reads run logs across sessions, correlates scanner results to rules, and proposes adjustments:

- **Input:** All `runs/run-N.md` files across all sessions in all skill spaces, scanner result logs
- **Analysis:** Which rules fail most? Which scanners catch most? Which rules have been promoted from corrections? Which corrections keep recurring without promotion?
- **Output:** Proposed rule rewrites, scanner enable/disable, new rules from recurring unpromoted corrections

## Implementation Stages

### Stage 1: Manual (current)
- Corrections in run logs, manual promotion to skill rules
- Scanners run on demand via `build.py validate`
- No tracking of scanner results over time

### Stage 2: Track scanner results
- `build.py validate` writes results to a JSON log alongside the run log
- Format: `[{ruleId, passed, violationSnippet, scannerUsed, timestamp}]`
- History accumulates per session

### Stage 3: Process rules + scanners
- Add scanners for process steps (session naming, run-0 creation, correction format, promoted-to-skill table)
- These scanners check session files and run logs, not just interaction tree / domain model

### Stage 4: Dynamic optimization
- Orchestrator agent reads result history, proposes rule/scanner changes
- Threshold-based: if scanner catch rate for a rule drops below X% across N sessions, disable scanner
- If rule fail rate stays above Y% after Z sessions, flag for human review or auto-rewrite

### Stage 5: Autonomous improvement
- Orchestrator runs another agent with the skill against test contexts
- Compares output to expected corrections
- Iterates rule prompts until scanner catch rate meets threshold
- Human approves promoted changes

## Open Questions

- What's the right threshold for "well-learned" (disable scanner)? 0 failures across 5 sessions? 10?
- Should rule injection priority be weighted by fail rate, or just binary (inject / don't inject)?
- How to handle rules that conflict (one rule says "enumerate all stories" for story-granularity, another says "don't enumerate" for scaffold-pattern)?
- Where does the result history live? Per skill space? Global across all skill spaces?
