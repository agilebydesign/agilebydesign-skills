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
