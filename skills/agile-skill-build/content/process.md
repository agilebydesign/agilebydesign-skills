# Ace-Build Process

Build new ace-skills. Use when the user wants to create a skill with the standard ace-skill structure.

## Process

1. **Scaffold** — Run `scaffold.py --name ace-<name>` to create the directory.
2. **Fill content** — AI or user fills core, process, strategy, output, validation from markdown/prompts/text.
3. **Complete gaps** — If pieces are missing, user completes them.
4. **Build** — Run `build.py` to assemble AGENTS.md.

When creating an ace-skill:

1. User provides markdown, prompts, or text describing the skill.
2. AI uses Build-ACE to scaffold (if new) or identifies target skill.
3. AI fills content pieces from input. If insufficient, report gaps.
4. User completes missing pieces.
5. AI reruns build when all pieces are complete.
