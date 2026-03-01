# Agile by Design Agent Skills

Reusable agent skills from [Agile by Design](https://agilebydesign.com).

## Skills

### content-memory

Converts documents (PDF, PPTX, DOCX, XLSX, etc.) to markdown and chunks them for agent memory. Use when adding content to agent context, refreshing memory, or ingesting a folder of documents.

**Install:**

```bash
npx skills add agilebydesign/agilebydesign-skills --skill content-memory
```

**Usage:** See [skills/content-memory/SKILL.md](skills/content-memory/SKILL.md) for full instructions.

### solution-shaping

Shape source material into an Interaction Tree and State Model (story map and domain model). Use when shaping requirements, deriving epics and stories from source documents, or building a hierarchical structure of actor exchanges and domain concepts.

**Install:**

```bash
npx skills add agilebydesign/agilebydesign-skills --skill solution-shaping
```

**Usage:** See [skills/solution-shaping/SKILL.md](skills/solution-shaping/SKILL.md) for full instructions.

## Install All Skills

```bash
npx skills add agilebydesign/agilebydesign-skills
```

## Publish to skills.sh

1. Create the repository on GitHub: [github.com/agilebydesign/agilebydesign-skills](https://github.com/agilebydesign/agilebydesign-skills)
2. Push this content
3. Submit at [agentskill.sh/submit](https://agentskill.sh/submit) with `https://github.com/agilebydesign/agilebydesign-skills`
4. Skills appear on the leaderboard as users install them via `npx skills add`

## License

MIT
