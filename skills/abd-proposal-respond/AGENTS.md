# Core Definitions

<!-- section: proposal.core.definitions -->
## Concepts

- **ProposalSource** — Client RFP, Q&A, requirements (PDF, PPTX, DOCX, XLSX, etc.)
- **Memory** — Converted and chunked content; searchable via RAG (ace-context-to-memory)
- **ResponseFolder** — Output area for response artifacts; created alongside proposal material; symlinked from project
- **Strategy** — Response plan: which questions, in what order, format guidance, DO/DO NOT corrections
- **Accelerator** — A lettered appendix reference (A, B, C, …) that answers cite; typically a framework, method, or approach with source slides. Defined by appendix letter and framework name.
- **Accelerator Table** — Markdown table that defines and accumulates accelerators: appendix letter, framework name, slide file, slide numbers, URL. Each answer reference adds or updates a row; built in real time.

## What This Skill Does

- Convert proposal material to memory (via ace-context-to-memory)
- Create response folder and symlink
- Propose a strategy (question coverage, order, format)
- Answer questions using memory RAG
- **Define and accumulate accelerators** — When answers reference `*See Appendix X (Name)*`, define the accelerator (appendix letter, framework name) and accumulate it in the Accelerator Table with slide file, slide numbers, and URL. Each reference adds or updates a row.
- **Correct** — When user says "correct," add DO/DO NOT to the strategy document; re-run

## Pattern from Shaping (what we reuse)

- **Inject prompt** — Instructions are assembled per operation and injected into the AI prompt
- **Strategy** — A strategy document (`response/strategy.md`) holds the plan and accumulated corrections
- **Correct** — Corrections go into the strategy (DO/DO NOT with wrong/correct examples); do not just fix the answer in place

## Dependency: ace-context-to-memory

- Convert documents to markdown and chunks
- Index for semantic search
- Run `search_memory "<query>"` when answering questions

---

# Process Overview

<!-- section: proposal.process.intro -->
Respond to a client proposal by converting materials to memory, creating a strategy, and answering questions. Work in small batches. **Correct** means add DO/DO NOT to the strategy—do not just fix the answer.

1. **Setup** — Convert to memory; create response folder; symlink.
2. **Strategy first** — Analyze documents; propose response plan; save to `response/strategy.md`. Get approval.
3. **Answer a few questions** — Use memory RAG. 3–5 per batch. Get approval.
4. **Iterate** — Corrections → add DO/DO NOT to strategy; re-run or proceed.

### When the user says

- "Create strategy," "propose plan" → **create_strategy**
- "Answer questions," "next batch" → **answer_questions**
- "Correct," "fix that," "wrong" → **improve_strategy** (add DO/DO NOT to strategy; re-run)
- "Proceed," "expand" → **proceed_slice**

### Output Paths

- **Strategy:** `response/strategy.md`
- **Response artifacts:** `response/` (symlinked)
- **Accelerator Table:** `Accelerator Table.md` (or alongside response md); updated in real time when answers reference appendix

<!-- section: proposal.process.accelerators -->
## Accelerators

When answers reference `*See Appendix X (Name)*`, define the accelerator and accumulate it in the **Accelerator Table** immediately. Add or update row: Appendix letter, framework name, slide file, slide numbers, URL. Keep URLs in table. When done, run `build_appendix_deck.py --table <path> [--output <path>]` to assemble the appendix deck.

<!-- section: proposal.process.post_strategy.review -->
## Corrections

When user says "correct" or feedback implies a reusable rule: add **DO** or **DO NOT** to the strategy with wrong/correct examples. Re-run until approved.

---

# Strategy Phase

<!-- section: proposal.strategy.starting -->
## Common Response Instructions (Starting Template)

Include in `response/strategy.md` as baseline. Adapt per RFP.

**Structure:** Lead paragraph → bulleted list with **Bold labels** → source references.

**Lead paragraph — DO:** Articulate outcomes in the client's language. "Our firm would aim to accomplish [concrete outcomes]." "We will achieve these outcomes through:"

**Lead paragraph — DON'T:** Do not restate the question generically.

**Bullet prose — DO:** Explain method and mechanism. 2–3 substantive sentences per bullet.

**Bullet prose — DON'T:** Do not use "We will [verb]... to achieve [outcome]" for every bullet. Explain *how*.

**Bullet labels — DO:** Use approach/method names. Name what we do, not the output.

**Tailoring — DO:** Connect each bullet to the specific question. Use the question's language.

See `rules/response-format.md` for full DO/DO NOT. Add project-specific corrections as you iterate.

<!-- section: proposal.strategy.phase -->
1. **Analyze** the proposal sources — question coverage, priorities, assumptions.
2. **Present** the strategy — which questions, in what order, format guidance.
3. **Validate** — User reviews; refine until approved.
4. **Save** to `response/strategy.md`.

<!-- section: proposal.strategy.criteria -->
## Strategy Criteria

**Tone** — Voice, formality, perspective (e.g. aspirational, direct, collaborative).

**Level of detail** — How deep per question (full answer, draft, placeholder; technical vs executive).

**Audience** — Who reads this (evaluators, technical reviewers, executives); tailor accordingly.

**References or examples to speak to** — Which sources, case studies, or prior work to cite; what evidence to invoke.

<!-- section: proposal.strategy.slices.running -->
## Running Batches

1. **Answer 3–5 questions** — User reviews and corrects.
2. **Corrections → strategy** — Add DO/DO NOT with wrong/correct examples. Re-run until approved.
3. **Proceed** — Next batch or expand scope.
4. **Correct** — "Correct" means correct the strategy; do not just fix the answer in place.

<!-- section: proposal.strategy.corrections -->
## Corrections Format

Each **DO** or **DO NOT** must include:
- The rule
- **Example (wrong):** What was done incorrectly
- **Example (correct):** What it should be

Re-run until the user approves.

**Use memory RAG** — Run `search_memory "<query>"` and cite retrieved chunks when answering.

**Optional: index our work** — After each batch (or when strategy changes), run `index_memory --path response/` so subsequent answers can reference prior work and corrections.

<!-- section: proposal.strategy.accelerators -->
## Accelerators (Lettered Appendix)

Answers may refer to accelerators — typically `*See Appendix X (Full Name)*` at the end of bullets. The author (or AI) may suggest an accelerator when a framework, method, or approach warrants a slide appendix.

**Define and accumulate in real time** — When writing or revising answers, define each referenced accelerator (appendix letter, framework name) and accumulate it in the **Accelerator Table** (e.g. `Accelerator Table.md`). Add or update a row with slide file, slide numbers, and URL. The table grows as answers are written. Keep URLs in the table for now.

**Table format:**
| Appendix | Framework Name | Slide File | Slide Numbers | Url |
|----------|----------------|------------|---------------|-----|
| **A** | Lean Change | Lean Change Approach Slides.pptx | **1, 2** | [Link](url) |

**When done** — Run `build_appendix_deck.py` (or project-specific script) to assemble the appendix deck from the table. Default output: derived from the table md name (e.g. `Accelerator Table.md` → `Appendix_Accelerators.pptx`). Override with `--output <path>`.

---

# Output Structure

## Response Folder

- **Location:** `<proposal_folder>/response/`
- **Symlink:** Project has `response` → proposal response folder
- **Contents:** `strategy.md`, answers (per batch or single file), `Accelerator Table.md` (when accelerators are used)

## Accelerator Table

- **Location:** Same folder as response md (e.g. `workspace/jbom response/Accelerator Table.md`) or `response/Accelerator Table.md`
- **Format:** Markdown table with columns: Appendix | Framework Name | Slide File | Slide Numbers | Url
- **Define and accumulate:** In real time as answers reference `*See Appendix X (Name)*`; add or update rows with slide file, numbers, URL
- **Build:** Run `build_appendix_deck.py` when done to assemble appendix deck; default output derived from table path, or `--output <path>`

## Strategy Document

```markdown
# Response Strategy: [Proposal Name]

## Question Coverage
[Which questions, source, priority]

## Order
[Which to answer first]

## DO / DO NOT (from corrections)
- **DO** — [rule]
  - Example (wrong): ...
  - Example (correct): ...
```

<!-- section: proposal.output.answer_format -->
## Answer Format

- Use `search_memory "<query>"` before drafting
- Cite source (document, section, slide/page)
- Follow Content Voice when applicable

---

# Validation

## Pre-Strategy

- [ ] Proposal material in memory
- [ ] Response folder created
- [ ] Symlink exists

<!-- section: proposal.validation.pre_answer -->
## Pre-Answer

- [ ] Strategy approved
- [ ] 3–5 questions per batch
- [ ] `search_memory` used
- [ ] Sources cited

<!-- section: proposal.validation.correction -->
## Correction

When user says "correct":
- [ ] DO or DO NOT added to strategy with examples
- [ ] Re-run with corrected guidance
- [ ] User approval before proceeding

---

# Script Invocation

Run from workspace root. Set `CONTENT_MEMORY_ROOT` if workspace differs from cwd.

## setup_response.py

Creates response folder and symlink for proposal response workflow.

**When to call:** Before creating strategy; when starting a new proposal response.

**Usage:**
```bash
python skills/ace-proposal-respond/scripts/setup_response.py --proposal <proposal_folder> [--project <project_root>]
```

**Parameters:**
- `--proposal` (required): Folder containing proposal material (e.g. `workspace/jbom response`)
- `--project` (optional): Project root for symlink (default: CONTENT_MEMORY_ROOT or cwd)

**Example:**
```bash
python skills/ace-proposal-respond/scripts/setup_response.py --proposal "workspace/jbom response"
```

**Output:** Creates `<proposal_folder>/response/` and symlink `<project_root>/response` → response folder.

---

## ace-context-to-memory (dependency)

Convert proposal material to memory and index for RAG. Run before answering questions.

**link_workspace_source.py** — Link proposal folder to source (if not already):
```bash
python skills/ace-context-to-memory/scripts/link_workspace_source.py --path "workspace/jbom response" --name "JBOM"
```

**index_memory.py** — Full pipeline (convert → chunk → embed):
```bash
python skills/ace-context-to-memory/scripts/index_memory.py --path "source/JBOM"
```

**search_memory.py** — Semantic search when answering questions:
```bash
python skills/ace-context-to-memory/scripts/search_memory.py "<query>" --k 5
```

---

## build_appendix_deck.py

Assembles the appendix deck from the Accelerator Table. Run when response is done and accelerators have been accumulated.

**When to call:** After completing answers that reference accelerators; when ready to produce the appendix PowerPoint.

**Usage:**
```bash
python skills/ace-proposal-respond/scripts/build_appendix_deck.py --table <accelerator_table_path> [--output <pptx_path>]
```

**Parameters:**
- `--table` (required): Path to Accelerator Table.md (e.g. `workspace/jbom response/Accelerator Table.md`)
- `--output` (optional): Output PPTX path. Default: derived from table path (e.g. `Appendix_Accelerators.pptx` in same folder)

**Example:**
```bash
python skills/ace-proposal-respond/scripts/build_appendix_deck.py --table "workspace/jbom response/Accelerator Table.md"
python skills/ace-proposal-respond/scripts/build_appendix_deck.py --table "workspace/jbom response/Accelerator Table.md" --output "workspace/jbom response/JBOM_Appendix_Accelerators.pptx"
```

**Config:** Create `appendix_config.json` in the table's directory:
```json
{
  "style_deck": "path/to/PO_Training.pptx",
  "onedrive_root": "C:/Users/.../OneDrive - Org/Shared Documents/Assets",
  "search_roots": ["path/to/Agile Thinking", "path/to/Client Engagements"]
}
```
Or set `APPENDIX_STYLE_DECK`, `APPENDIX_ONEDRIVE_ROOT` env vars.

**Note:** Project-specific builds (e.g. `build_jbom_appendix_deck.py`) may exist with hardcoded style deck and paths. The skill script is a generic entry point; extend or replace per project.

---

## build.py

Assembles content into AGENTS.md.

**Usage:**
```bash
cd skills/ace-proposal-respond
python scripts/build.py
```

---
