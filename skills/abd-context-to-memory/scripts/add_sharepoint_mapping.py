#!/usr/bin/env python3
"""
Add a OneDrive → SharePoint mapping so context-to-memory can generate shareable links.

Usage:
  python add_sharepoint_mapping.py --prefix "OneDrive - Agile by Design" --base "https://...sharepoint.com/.../Shared%20Documents"
  python add_sharepoint_mapping.py --path <file_in_onedrive> --base "<full_sharepoint_url>"

With --path: extracts the OneDrive prefix from the file path.
With --base: accepts full SharePoint URL; strips file path and query to get base.

Run from workspace root. Updates sharepoint_mapping.json in the skill.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "sharepoint_mapping.json"

DEFAULT_QUERY = "csf=1&web=1"


def _extract_base_from_url(url: str) -> str:
    """
    Strip file path and query from a SharePoint URL to get the document library base.
    E.g. https://.../Shared%20Documents/Assets/file.pptx?csf=1&web=1
     -> https://.../Shared%20Documents
    """
    parsed = urlparse(url)
    path = parsed.path or ""
    # Remove trailing filename (has extension like .pptx, .pdf, .docx)
    if "/" in path:
        parts = path.rstrip("/").split("/")
        # Drop last part if it looks like a file (has extension)
        if parts and re.search(r"\.[a-z0-9]+$", parts[-1], re.I):
            parts = parts[:-1]
        path = "/".join(parts)
    base = urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))
    return base.rstrip("/")


def _extract_prefix_from_path(file_path: Path) -> str | None:
    """Extract OneDrive folder name from path, e.g. 'OneDrive - Agile by Design'."""
    path_str = str(file_path.resolve()).replace("\\", "/")
    idx = path_str.lower().find("onedrive")
    if idx < 0:
        return None
    rest = path_str[idx:]
    end = rest.find("/")
    if end > 0:
        return rest[:end]
    return rest


def add_mapping(prefix: str, base: str, query: str = DEFAULT_QUERY) -> bool:
    """Add or update mapping. Returns True if config was changed."""
    if not prefix or not base:
        return False
    base = base.strip().rstrip("/")
    data = {"description": "OneDrive path prefix -> SharePoint base URL for shareable links.", "mappings": []}
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            data.setdefault("mappings", [])
        except (json.JSONDecodeError, OSError):
            pass

    mappings = data["mappings"]
    for m in mappings:
        if m.get("onedrive_prefix", "").strip() == prefix:
            m["sharepoint_base"] = base
            m["sharepoint_query"] = query
            CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            return True

    mappings.append({"onedrive_prefix": prefix, "sharepoint_base": base, "sharepoint_query": query})
    CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def main():
    args = sys.argv[1:]
    prefix = None
    base = None
    path_arg = None
    query = DEFAULT_QUERY

    i = 0
    while i < len(args):
        if args[i] == "--prefix" and i + 1 < len(args):
            prefix = args[i + 1]
            i += 2
        elif args[i] == "--base" and i + 1 < len(args):
            base = args[i + 1]
            i += 2
        elif args[i] == "--path" and i + 1 < len(args):
            path_arg = args[i + 1]
            i += 2
        elif args[i] == "--query" and i + 1 < len(args):
            query = args[i + 1]
            i += 2
        else:
            i += 1

    if not base:
        print("Usage:")
        print('  add_sharepoint_mapping.py --prefix "OneDrive - Org" --base "<sharepoint_base_url>"')
        print("  add_sharepoint_mapping.py --path <file_in_onedrive> --base \"<full_sharepoint_url>\"")
        print()
        print("  --base: SharePoint base URL (or full file URL; script will strip to base)")
        print("  --prefix: OneDrive folder name (e.g. 'OneDrive - Agile by Design')")
        print("  --path: File path under OneDrive; prefix is extracted automatically")
        print("  --query: Optional. Default: csf=1&web=1")
        sys.exit(1)

    base = _extract_base_from_url(base)

    if path_arg and not prefix:
        p = Path(path_arg)
        if not p.is_file():
            print(f"File not found: {path_arg}")
            sys.exit(1)
        prefix = _extract_prefix_from_path(p)
        if not prefix:
            print(f"Path does not appear to be under OneDrive: {path_arg}")
            sys.exit(1)
        print(f"Detected OneDrive prefix: {prefix}")

    if not prefix:
        print("Provide --prefix or --path with a file under OneDrive.")
        sys.exit(1)

    if add_mapping(prefix, base, query):
        print(f"Added mapping: {prefix} -> {base}")
        print(f"Updated {CONFIG_PATH}")
    else:
        print("Failed to add mapping.")
        sys.exit(1)


if __name__ == "__main__":
    main()
