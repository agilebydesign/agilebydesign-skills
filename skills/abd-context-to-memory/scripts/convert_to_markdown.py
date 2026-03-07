"""
Convert source files to markdown for agent memory.

Usage:
  python convert_to_markdown.py --memory <source_path>   # folder: all supported files
  python convert_to_markdown.py --memory <source_path> --sharepoint-base <url>  # inject SharePoint URLs
  python convert_to_markdown.py --file <file_path>      # single file only

When source is in OneDrive, SharePoint URLs are auto-injected from sharepoint_mapping.json
so links work for anyone. Configure mappings in skills/abd-context-to-memory/sharepoint_mapping.json

Run from workspace root. Writes markdown alongside each source file (same folder).
Requires: pip install "markitdown[all]"

CRITICAL: Use --file when user asks for ONE file. Use --memory only when user
explicitly wants a folder processed. Do not process entire folders when user
specifies a single file.
"""

import os
import sys
from pathlib import Path
from urllib.parse import quote

try:
    from markitdown import MarkItDown
except ImportError:
    print('Missing dependency. Run: pip install "markitdown[all]"')
    sys.exit(1)

# Import OneDrive→SharePoint resolution from same scripts dir
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
try:
    from onedrive_to_sharepoint import (
        get_sharepoint_base_for_path,
        get_sharepoint_url_for_file,
        path_is_onedrive,
        extract_onedrive_prefix,
    )
except ImportError:
    def get_sharepoint_base_for_path(p):
        return (None, "")
    def get_sharepoint_url_for_file(p, b, q):
        return ""
    def path_is_onedrive(p):
        return False
    def extract_onedrive_prefix(p):
        return None

from _config import ROOT, ASSETS, ensure_root

ensure_root()

SUPPORTED = {
    ".pdf", ".pptx", ".docx", ".xlsx", ".xls",
    ".html", ".htm", ".txt", ".csv", ".json", ".xml",
}

_md = MarkItDown()

DEFAULT_SHAREPOINT_QUERY = "csf=1&web=1"

# Track OneDrive prefixes we've already warned about (no mapping)
_onedrive_warned_prefixes: set[str] = set()

_SKILL_ROOT = _scripts_dir.parent


def _print_onedrive_mapping_instructions(prefix: str) -> None:
    """Print instructions for adding a SharePoint mapping when OneDrive has no config."""
    config_path = _SKILL_ROOT / "sharepoint_mapping.json"
    add_script = _scripts_dir / "add_sharepoint_mapping.py"
    try:
        script_rel = add_script.relative_to(ROOT)
    except ValueError:
        script_rel = add_script
    print("\n" + "=" * 70)
    print("WARNING: Source is in OneDrive but no SharePoint mapping is configured.")
    print(f"  OneDrive folder: {prefix}")
    print("  Links in the generated markdown will use local paths (not shareable).")
    print()
    print("To add shareable SharePoint links:")
    print("  1. Open any file from this OneDrive folder in SharePoint/OneDrive web.")
    print("  2. Copy the URL from the browser address bar.")
    print("  3. Add the mapping (paste your URL; script will derive the base):")
    print(f'     python {script_rel} --prefix "{prefix}" --base "<paste_url_here>"')
    print()
    print("  Or with a file path (prefix is auto-detected):")
    print(f'     python {script_rel} --path "<file_in_onedrive>" --base "<paste_url_here>"')
    print()
    print(f"  Or edit {config_path.name} and add an entry to the mappings array.")
    print("=" * 70 + "\n")


def convert_one(
    src: Path,
    out_dir: Path,
    source_ref: bool = True,
    src_base: Path | None = None,
    sharepoint_base: str | None = None,
    sharepoint_query: str | None = None,
    memory_name: str | None = None,
    logical_rel: Path | None = None,
) -> Path:
    """Convert one file to markdown. Returns output path."""
    out_dir.mkdir(parents=True, exist_ok=True)

    text = _md.convert(str(src)).text_content

    # Auto-resolve SharePoint URL when source is in OneDrive (from sharepoint_mapping.json)
    if sharepoint_base is None:
        od_base, od_query = get_sharepoint_base_for_path(src)
        if od_base:
            sharepoint_base = od_base
            sharepoint_query = sharepoint_query or od_query
        elif path_is_onedrive(src):
            prefix = extract_onedrive_prefix(src)
            if prefix and prefix not in _onedrive_warned_prefixes:
                _onedrive_warned_prefixes.add(prefix)
                _print_onedrive_mapping_instructions(prefix)

    if source_ref:
        added = False
        rel_posix = None
        if logical_rel is not None:
            rel_posix = logical_rel.as_posix()
        elif src_base is not None:
            try:
                rel_posix = src.relative_to(src_base).as_posix()
            except (ValueError, OSError):
                pass
        if memory_name and rel_posix:
            path_part = f"source/{memory_name}/{rel_posix}"
            if sharepoint_base:
                q = sharepoint_query or DEFAULT_SHAREPOINT_QUERY
                url_part = get_sharepoint_url_for_file(src, sharepoint_base, q)
                if url_part:
                    text = f"<!-- Source: {path_part} | {url_part} -->\n\n" + text
                    added = True
                else:
                    encoded = quote(rel_posix, safe="/")
                    url_part = f"{sharepoint_base.rstrip('/')}/{encoded}?{q}"
                    text = f"<!-- Source: {path_part} | {url_part} -->\n\n" + text
                    added = True
            else:
                # Local path reference
                local = (ROOT / "source" / memory_name / rel_posix).as_uri()
                text = f"<!-- Source: {path_part} | {local} -->\n\n" + text
                added = True
        if not added and sharepoint_base:
            # Single file or path under OneDrive: use full SharePoint URL
            url_part = get_sharepoint_url_for_file(src, sharepoint_base, sharepoint_query or DEFAULT_SHAREPOINT_QUERY)
            if url_part:
                path_part = str(src.relative_to(src.parent)) if src_base else src.name
                text = f"<!-- Source: {path_part} | {url_part} -->\n\n" + text
                added = True
        if not added:
            try:
                rel = src.relative_to(ROOT)
                url = (ROOT / rel).as_uri()
                text = f"<!-- Source: {rel.as_posix()} | {url} -->\n\n" + text
            except (ValueError, OSError):
                pass

    out = out_dir / (src.stem + ".md")
    out.write_text(text, encoding="utf-8")
    return out


def _run_file_mode(file_path: str) -> None:
    """Convert a single file to markdown. Only processes that file."""
    p = Path(file_path)
    if not p.is_absolute():
        for base in (ASSETS, ROOT):
            candidate = base / file_path
            if candidate.is_file():
                p = candidate
                break
    if not p.is_file():
        print(f"File not found: {file_path}")
        return
    if p.suffix.lower() not in SUPPORTED:
        print(f"Unsupported format: {p.suffix}. Supported: {sorted(SUPPORTED)}")
        return

    out_dir = p.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"File: {p.name} -> {out_dir}/\n")
    try:
        memory_name = p.parent.name if p.parent != Path(".") else p.stem
        logical_rel = Path(p.name)
        out = convert_one(
            p,
            out_dir,
            memory_name=memory_name,
            logical_rel=logical_rel,
        )
        kb = out.stat().st_size // 1024
        print(f"Done: 1 file converted ({kb} KB)")
    except (Exception, BaseException) as e:
        print(f"FAIL  {type(e).__name__}: {e}")


def _walk_with_logical_path(
    root: Path, logical_prefix: Path, followlinks: bool = True
) -> list[tuple[Path, Path]]:
    """Walk directory, yield (file_path, logical_rel) preserving logical structure through symlinks."""
    out: list[tuple[Path, Path]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=followlinks):
        dp = Path(dirpath)
        try:
            rel = dp.relative_to(root)
        except ValueError:
            rel = Path(logical_prefix.name)  # fallback if resolved outside
        logical_rel = logical_prefix / rel if rel != Path(".") else logical_prefix
        for name in filenames:
            p = dp / name
            if p.suffix.lower() in SUPPORTED:
                try:
                    if p.is_file():
                        out.append((p, logical_rel / name))
                except OSError:
                    pass
    return out


def _run_memory_mode(
    memory_path: str,
    sharepoint_base: str | None = None,
    sharepoint_query: str | None = None,
    subfolders: list[str] | None = None,
    memory_name_override: str | None = None,
) -> None:
    """Convert folder; write markdown alongside each source file (same folder)."""
    p = Path(memory_path)
    if p.is_absolute():
        src_full = p
    else:
        under_assets = ASSETS / memory_path
        under_root = ROOT / memory_path
        if under_assets.exists():
            src_full = under_assets
        elif under_root.exists():
            src_full = under_root
        else:
            print(f"Path not found: {memory_path}")
            return

    memory_name = memory_name_override or src_full.name

    # Build list of (file_path, logical_rel) - walk each subfolder to preserve logical paths through symlinks
    folders_to_walk: list[tuple[Path, Path]] = []
    if subfolders:
        for sub in subfolders:
            sub_path = src_full / sub.strip()
            if sub_path.exists():
                folders_to_walk.append((sub_path, Path(sub.strip())))
    if not folders_to_walk:
        folders_to_walk = [(src_full, Path("."))]

    files: list[tuple[Path, Path]] = []
    for root, logical_prefix in folders_to_walk:
        files.extend(_walk_with_logical_path(root, logical_prefix))
    files.sort(key=lambda x: str(x[1]))

    if not files:
        print(f"No supported files in {src_full}")
        return

    print(f"Source: {src_full}  ({len(files)} files) -> same folder\n")

    ok, fail = [], []
    for i, (f, logical_rel) in enumerate(files, 1):
        out_dir = f.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        label = str(logical_rel) if logical_rel != Path(".") else f.name
        print(f"  [{i}/{len(files)}] {label} ... ", end="", flush=True)
        try:
            out = convert_one(
                f,
                out_dir,
                sharepoint_base=sharepoint_base,
                sharepoint_query=sharepoint_query,
                memory_name=memory_name,
                logical_rel=logical_rel,
            )
            kb = out.stat().st_size // 1024
            print(f"OK  ({kb} KB)")
            ok.append(label)
        except (Exception, BaseException) as e:
            print(f"FAIL  {type(e).__name__}: {e}")
            fail.append((label, str(e)))

    print(f"\nDone: {len(ok)} converted, {len(fail)} failed.")
    if fail:
        for n, e in fail:
            print(f"  {n}: {e}")


def main():
    file_idx = next((i for i, a in enumerate(sys.argv) if a == "--file"), None)
    if file_idx is not None and file_idx + 1 < len(sys.argv):
        _run_file_mode(sys.argv[file_idx + 1])
        return

    memory_idx = next((i for i, a in enumerate(sys.argv) if a == "--memory"), None)
    if memory_idx is not None and memory_idx + 1 < len(sys.argv):
        sb_idx = next((i for i, a in enumerate(sys.argv) if a == "--sharepoint-base"), None)
        sq_idx = next((i for i, a in enumerate(sys.argv) if a == "--sharepoint-query"), None)
        f_idx = next((i for i, a in enumerate(sys.argv) if a == "--folders"), None)
        mn_idx = next((i for i, a in enumerate(sys.argv) if a == "--memory-name"), None)
        sb = sys.argv[sb_idx + 1] if sb_idx is not None and sb_idx + 1 < len(sys.argv) else None
        sq = sys.argv[sq_idx + 1] if sq_idx is not None and sq_idx + 1 < len(sys.argv) else None
        mn = sys.argv[mn_idx + 1] if mn_idx is not None and mn_idx + 1 < len(sys.argv) else None
        folders = []
        if f_idx is not None and f_idx + 1 < len(sys.argv):
            j = f_idx + 1
            while j < len(sys.argv) and not sys.argv[j].startswith("--"):
                folders.append(sys.argv[j])
                j += 1
        _run_memory_mode(sys.argv[memory_idx + 1], sharepoint_base=sb, sharepoint_query=sq, subfolders=folders or None, memory_name_override=mn)
        return

    print("Usage:")
    print("  python convert_to_markdown.py --file <file_path>     # single file only")
    print("  python convert_to_markdown.py --memory <source_path> # folder (all files)")
    print("  python convert_to_markdown.py --memory <source_path> --sharepoint-base <url> [--sharepoint-query <query>]")
    print("  python convert_to_markdown.py --memory <source_path> --folders <sub1> <sub2> ...  # process only these subfolders (for symlinked dirs)")
    print("  Use --file when user asks for ONE file. Use --memory only for folders.")


if __name__ == "__main__":
    main()
