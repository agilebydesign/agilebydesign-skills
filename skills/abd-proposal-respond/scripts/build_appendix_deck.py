#!/usr/bin/env python3
"""
Build appendix PowerPoint deck from Accelerator Table.

Usage:
  python build_appendix_deck.py --table <Accelerator_Table.md> [--output <path.pptx>]

Reads appendix mappings from the table. Requires appendix_config.json in the table's
directory with: style_deck, onedrive_root. Or set env: APPENDIX_STYLE_DECK, APPENDIX_ONEDRIVE_ROOT.

If project has its own script (e.g. build_jbom_appendix_deck.py), run that instead.
"""
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    import win32com.client
except ImportError:
    win32com = None


def _parse_slide_numbers(s: str) -> list[int]:
    """Parse '**1, 2**' or '**25, 26, 27, 28**' -> [1, 2] or [25,26,27,28]."""
    s = re.sub(r"\*\*", "", s).strip()
    nums = []
    for part in re.split(r"[,;]\s*", s):
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            nums.extend(range(int(lo.strip()), int(hi.strip()) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def _url_to_local_path(url: str, onedrive_root: Path) -> Path | None:
    """Convert SharePoint URL to local OneDrive path."""
    try:
        decoded = urllib.parse.unquote(url)
        decoded = decoded.split("?")[0]
        if "Assets" in decoded:
            m = re.search(r"Assets/([^?]+\.pptx)", decoded)
            if m:
                rel = m.group(1).replace("/", os.sep)
                return onedrive_root / rel
        if "Shared" in decoded and "Documents" in decoded:
            m = re.search(r"Shared%20Documents/([^?]+\.pptx)", url)
            if m:
                rel = urllib.parse.unquote(m.group(1)).replace("/", os.sep)
                return onedrive_root.parent / rel
    except Exception:
        pass
    return None


def parse_accelerator_table(
    md_path: Path,
    onedrive_root: Path,
    search_roots: list[Path] | None = None,
) -> list[tuple[str, str, list[tuple[Path, list[int]]]]]:
    """
    Parse Accelerator Table.md Summary Table.
    Returns: [(code, title, [(src_path, slide_indices), ...]), ...]
    """
    text = md_path.read_text(encoding="utf-8")
    sections = {}
    link_re = re.compile(r"\[Link\]\((https://[^)]+)\)")
    roots = search_roots or [onedrive_root]

    def resolve_file(filename: str) -> Path | None:
        for root in roots:
            p = root / filename
            if p.exists():
                return p
            alt = f"1) {filename}" if "Human Centric" in filename or "Story Writing" in filename else filename
            p = root / alt
            if p.exists():
                return p
        return None

    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) >= 5 and cells[0].startswith("**") and cells[0].endswith("**"):
            code = cells[0].strip("*").strip()
            title = cells[1]
            slide_file = cells[2]
            slide_numbers = cells[3]
            link_match = link_re.search(line)
            url = link_match.group(1) if link_match else ""
            slides = _parse_slide_numbers(slide_numbers)
            path = _url_to_local_path(url, onedrive_root) if url else None
            if path is None:
                path = resolve_file(slide_file)
            if path and slides:
                key = (code, title)
                if key not in sections:
                    sections[key] = []
                sections[key].append((path, slides))

    result = []
    seen = set()
    for (code, title), sources in sections.items():
        if (code, title) not in seen:
            seen.add((code, title))
            result.append((code, title, sources))
    return result


def load_config(table_path: Path) -> tuple[Path | None, Path | None, list[Path]]:
    """Load style_deck, onedrive_root, search_roots from appendix_config.json or env."""
    table_dir = table_path.parent
    config_path = table_dir / "appendix_config.json"
    style_deck = None
    onedrive_root = None
    search_roots = []

    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
            sd = data.get("style_deck")
            od = data.get("onedrive_root")
            sr = data.get("search_roots", [])
            if sd:
                style_deck = Path(sd) if Path(sd).is_absolute() else table_dir / sd
            if od:
                onedrive_root = Path(od)
            for r in sr:
                search_roots.append(Path(r) if Path(r).is_absolute() else table_dir / r)
        except (json.JSONDecodeError, OSError):
            pass

    if style_deck is None:
        style_deck = os.environ.get("APPENDIX_STYLE_DECK")
        style_deck = Path(style_deck) if style_deck else None
    if onedrive_root is None:
        onedrive_root = os.environ.get("APPENDIX_ONEDRIVE_ROOT")
        onedrive_root = Path(onedrive_root) if onedrive_root else None
    if not search_roots and onedrive_root:
        search_roots = [onedrive_root]

    return style_deck, onedrive_root, search_roots


def build_deck(
    table_path: Path,
    output_path: Path,
    style_deck: Path,
    onedrive_root: Path,
    search_roots: list[Path] | None = None,
) -> None:
    """Build PowerPoint deck from accelerator table."""
    if win32com is None:
        print("ERROR: pywin32 required. pip install pywin32")
        sys.exit(1)

    sections = parse_accelerator_table(table_path, onedrive_root, search_roots)
    if not sections:
        print("No appendix sections found in table.")
        sys.exit(1)

    try:
        import pythoncom
        pythoncom.CoInitialize()
    except ImportError:
        pass

    powerpoint = win32com.client.gencache.EnsureDispatch("PowerPoint.Application")
    powerpoint.Visible = 1
    style_pres = powerpoint.Presentations.Open(str(style_deck), WithWindow=False)
    time.sleep(0.5)
    slides = style_pres.Slides

    divider_layout_idx = 2
    for i in range(1, min(slides.Count + 1, 90)):
        try:
            s = slides.Item(i)
            if s.Shapes.HasTitle:
                title = s.Shapes.Title.TextFrame.TextRange.Text.strip()
                if title.startswith("Appendix") or "Appendix:" in title:
                    for j in range(1, style_pres.SlideMaster.CustomLayouts.Count + 1):
                        if style_pres.SlideMaster.CustomLayouts.Item(j).Name == s.CustomLayout.Name:
                            divider_layout_idx = j
                            break
                    break
        except Exception:
            pass

    n = slides.Count
    if n > 0:
        rng = slides.Range(list(range(1, n + 1)))
        rng.Delete()

    style_pres.SaveAs(str(output_path))
    time.sleep(0.5)

    title_layout = style_pres.SlideMaster.CustomLayouts.Item(1)
    s1 = slides.AddSlide(1, title_layout)
    try:
        for i in range(1, s1.Shapes.Count + 1):
            sh = s1.Shapes(i)
            if sh.HasTextFrame:
                sh.TextFrame.TextRange.Text = "Appendix: Accelerators"
                break
    except Exception:
        pass

    dest_index = 2
    for code, title, sources in sections:
        try:
            layout = style_pres.SlideMaster.CustomLayouts.Item(divider_layout_idx)
            div_slide = slides.AddSlide(dest_index, layout)
        except Exception:
            layout = style_pres.SlideMaster.CustomLayouts.Item(2)
            div_slide = slides.AddSlide(dest_index, layout)
        try:
            for i in range(1, div_slide.Shapes.Count + 1):
                sh = div_slide.Shapes(i)
                if sh.HasTextFrame:
                    sh.TextFrame.TextRange.Text = f"Appendix {code}: {title}"
                    break
        except Exception:
            pass
        dest_index += 1

        for src_path, slide_indices in sources:
            src_path = Path(src_path)
            if not src_path.exists():
                print(f"WARNING: Source not found: {src_path}")
                continue
            src_pres = None
            try:
                src_pres = powerpoint.Presentations.Open(str(src_path), WithWindow=False)
                time.sleep(0.2)
                slide_count = src_pres.Slides.Count
                for idx in slide_indices:
                    if idx > slide_count:
                        continue
                    src_pres.Slides.Range([idx]).Copy()
                    slides.Paste(dest_index)
                    dest_index += 1
            except Exception as e:
                print(f"WARNING: Failed on {src_path.name}: {e}")
            finally:
                if src_pres:
                    try:
                        src_pres.Close()
                    except Exception:
                        pass
                    time.sleep(0.3)

    style_pres.Save()
    style_pres.Close()
    powerpoint.Quit()
    print(f"Created: {output_path}")


def main():
    args = sys.argv[1:]
    table_path = None
    output_path = None
    i = 0
    while i < len(args):
        if args[i] == "--table" and i + 1 < len(args):
            table_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        else:
            i += 1

    if not table_path or not table_path.exists():
        print("Usage: python build_appendix_deck.py --table <Accelerator_Table.md> [--output <path.pptx>]")
        print("Create appendix_config.json in table dir with style_deck, onedrive_root.")
        print("Or set APPENDIX_STYLE_DECK, APPENDIX_ONEDRIVE_ROOT.")
        sys.exit(1)

    if output_path is None:
        output_path = table_path.parent / "Appendix_Accelerators.pptx"

    style_deck, onedrive_root, search_roots = load_config(table_path)
    if not style_deck or not style_deck.exists():
        print("ERROR: style_deck not found. Set appendix_config.json or APPENDIX_STYLE_DECK.")
        sys.exit(1)
    if not onedrive_root or not onedrive_root.exists():
        print("ERROR: onedrive_root not found. Set appendix_config.json or APPENDIX_ONEDRIVE_ROOT.")
        sys.exit(1)

    build_deck(table_path, output_path, style_deck, onedrive_root, search_roots)


if __name__ == "__main__":
    main()
