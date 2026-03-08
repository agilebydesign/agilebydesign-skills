# Script Change Recommendations

Analysis of where scripts need to change to support: (1) create strategy (with slices), (2) perform runs on a slice.

## Summary

| Component | Change |
|-----------|--------|
| **script-invocation.md** | ✅ Updated — two-phase flow, strategy passed into API, component-based rule filtering |
| **skill-config.json** | Add `run_slice` operation (or alias `generate_slice` → run_slice) |
| **build.py** | Add `run_slice` to usage; accept `--strategy` path; pass strategy into engine |
| **instructions.py** (synthesizer) | Accept strategy (path or parsed); parse components; filter rules by component tags |
| **engine.py** | Accept strategy path/content; expose components for rule filtering |
| **Post-synthesis review** | Consider adding `review_corrections` operation |

---

## 0. Strategy passed into API (component-based filtering)

**Design:** The strategy is passed into the API (path or content), not only read from workspace. The strategy declares **components** to render (epic, story, step, scenario, examples, domain_concept). The engine parses the strategy for these components and uses them to filter rules — only rules whose tags intersect with in-scope components are included in the assembled prompt.

**Flow:** `build.py --strategy path` → engine loads strategy → parses components → instructions loads rules → filters by component tags → assembles prompt with strategy markdown + filtered rules.

**Bespoke strategies:** A custom strategy can mix components (e.g. discovery + mapping + domain concepts + examples at sub-epic level). Examples can be scoped at different levels. See `content/rules-tagging-proposal.md` and `content/strategy.md`.

---

## 1. skill-config.json

**Current:** `create_strategy`, `generate_slice`, `improve_strategy`

**Change:** Add `run_slice` with same sections as `generate_slice`, or rename `generate_slice` → `run_slice`. The process uses "runs" not "generate slice" — `run_slice` is clearer.

```json
"run_slice": ["story_synthesizer.process.intro", "story_synthesizer.strategy.slices.running", ...]
```

Keep `generate_slice` as alias for backward compatibility if desired.

---

## 2. build.py

**Current:** `get_instructions <operation>` with operations: create_strategy, generate_slice, improve_strategy

**Change:**
- Add `run_slice` to the usage message.
- Add `--strategy path/to/strategy.md` — pass strategy path into the engine. Engine uses it for component parsing and rule filtering.
- Optionally: `get_instructions run_slice [N]` — pass run/slice index so instructions can inject "Run N" or run log path. Not strictly required; AI can infer from user message and workspace.

```python
# Usage: python build.py get_instructions <operation> [--strategy path] [run_index]
# Operations: create_strategy, run_slice, generate_slice, improve_strategy
```

---

## 3. instructions.py (synthesizer)

**Current:** Strategy is read from `engine.strategy_path` and injected as markdown for `generate_slice`, `run_slice`, `improve_strategy`, etc.

**Change:** Strategy is passed into the API (path or content). Parse strategy for **components** (epic, story, step, scenario, examples, domain_concept). Filter rules by component tags — only include rules whose tags intersect with in-scope components. See `content/rules-tagging-proposal.md`.

```python
# Accept strategy from engine (path or parsed structure)
# Parse strategy for components (Comprehensiveness Criteria modes)
# When loading rules: filter by component tags
# if operation in ("generate_slice", "run_slice", ...) and strategy:
#   components = parse_strategy_components(strategy)
#   rules = load_rules_filtered_by_tags(rules_dir, components)
```

---

## 4. engine.py

**Current:** `strategy_path` is set from workspace; `_create_output_dirs` creates `output_root/slice-1` for each skill.

**Change:**
- Accept strategy path or content as input (from build.py `--strategy`). Expose `strategy_path` or `strategy_content` and parsed `components` for rule filtering.
- Parse strategy for components (Comprehensiveness Criteria modes: epic, story, step, scenario, examples, domain_concept). See `content/strategy.md`.
- For abd-story-synthesizer, create `runs/` instead of (or in addition to) `slice-1`. Process says output goes to `story-synthesizer/` and run logs to `story-synthesizer/runs/run-N.md`. The engine should ensure `runs/` exists.

```python
# Accept strategy_path override from CLI
# components = parse_strategy_components(strategy_path.read_text())
# Expose engine.components for instructions.py rule filtering

# In _create_output_dirs, for abd-story-synthesizer:
if "story-synthesizer" in skill_name or skill_name == "abd-story-synthesizer":
    (output_root / "runs").mkdir(parents=True, exist_ok=True)
```

---

## 5. Post-synthesis review

**Process says:** "Once all runs are done, have the AI review all corrections collected in the run log and determine what needs to change in the rules and/or instructions."

**Gap:** No `review_corrections` or `post_synthesis_review` operation. The AI would need instructions for this phase.

**Change:** Add operation `review_corrections` with sections that tell the AI to:
- Read all run logs in `runs/`
- Identify patterns in corrections
- Propose updates to strategy or skill rules
- Not produce new output — only analyze and recommend

---

## 6. Run log injection (optional)

For re-runs, the AI needs the run log (corrections). Options:

**A. No injection** — Instructions say "when re-running, read the run log from `runs/run-N.md`" and AI infers N from user message. Works today.

**B. Pass run index** — `get_instructions run_slice 2` injects "Run log: runs/run-1.md" (previous run for this slice). Requires engine to track slice→run mapping. More complex.

**Recommendation:** A. Keep it simple; user says "re-run slice 1" and AI knows to read runs/ and find the relevant log.

---

## 7. Output paths

Process specifies:
- **Strategy:** `<skill-space>/story-synthesizer/strategy.md`
- **Output:** `<skill-space>/story-synthesizer/` (Interaction Tree, State Model)
- **Runs:** `<skill-space>/story-synthesizer/runs/run-N.md`

Engine's `strategy_path` already prefers `workspace/story-synthesizer/strategy.md`. Good.

Engine's `_create_output_dirs` creates output folders. For story-synthesizer, ensure `runs/` exists.
