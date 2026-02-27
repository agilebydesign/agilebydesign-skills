---
name: export-markdown
description: >-
  Converts markdown files to Word (.docx). Use when the user wants to "export to
  Word", "convert markdown to docx", "save as Word", or produce a .docx from
  .md files.
---

# Export Markdown to Word

Convert markdown files to Microsoft Word (.docx) format. Handles headings, tables, bold, bullets, and paragraphs.

## When to Activate

- "Export to Word", "convert to docx", "save as Word"
- "Turn this markdown into a Word document"
- User has .md content and needs .docx output

## Usage

```bash
python scripts/md_to_docx.py input.md [output.docx]
```

- **input.md** (required): Path to markdown file
- **output.docx** (optional): Output path. If omitted, writes `input.docx` (same stem, .docx extension)

**Examples:**

```bash
# Same directory: writes approaches-slide.docx
python scripts/md_to_docx.py approaches-slide.md

# Explicit output path
python scripts/md_to_docx.py doc/notes.md output/notes.docx

# From workspace root
python skills/export-markdown/scripts/md_to_docx.py workspace/report.md report.docx
```

## Supported Markdown

| Element | Syntax |
|---------|--------|
| Headings | `#`, `##`, `###` |
| Tables | `| col | col |` |
| Bold | `**text**` |
| Bullets | `- item` |
| Horizontal rules | `---` |
| Paragraphs | Plain text |

## Requirements

```bash
pip install python-docx
```

## Script Location

Run from project root. Script path: `skills/export-markdown/scripts/md_to_docx.py`
