#!/usr/bin/env python3
"""
Resolve OneDrive path to SharePoint base URL for shareable links.

When content is in OneDrive (e.g. Shared Documents), local paths are not shareable.
This module maps OneDrive path prefixes to SharePoint base URLs so generated
markdown can include links usable by anyone with access.

Usage (as module):
  from onedrive_to_sharepoint import get_sharepoint_base_for_path
  base, query = get_sharepoint_base_for_path(Path("C:/Users/.../OneDrive - Org/Shared Documents/Assets/file.pptx"))

Config: sharepoint_mapping.json in skill root. Add entries for each OneDrive root.
"""

import json
import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "sharepoint_mapping.json"


def _load_mappings() -> list[tuple[str, str, str]]:
    """Load (onedrive_prefix, sharepoint_base, sharepoint_query) from config."""
    if not CONFIG_PATH.exists():
        return []
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        out = []
        for m in data.get("mappings", []):
            prefix = m.get("onedrive_prefix", "").strip()
            base = m.get("sharepoint_base", "").strip().rstrip("/")
            query = m.get("sharepoint_query", "csf=1&web=1")
            if prefix and base:
                out.append((prefix, base, query))
        return out
    except (json.JSONDecodeError, OSError):
        return []


def path_is_onedrive(file_path: Path) -> bool:
    """True if path appears to be under OneDrive (contains 'OneDrive' in path)."""
    path_str = str(file_path.resolve()).replace("\\", "/")
    return "onedrive" in path_str.lower()


def extract_onedrive_prefix(file_path: Path) -> str | None:
    """
    Extract OneDrive folder name from path, e.g. 'OneDrive - Agile by Design'.
    Returns None if path is not under OneDrive.
    """
    path_str = str(file_path.resolve()).replace("\\", "/")
    idx = path_str.lower().find("onedrive")
    if idx < 0:
        return None
    # Take from "OneDrive" until next / or end
    rest = path_str[idx:]
    end = rest.find("/")
    if end > 0:
        return rest[:end]
    return rest


def get_sharepoint_base_for_path(file_path: Path) -> tuple[str | None, str]:
    """
    If file_path is under a configured OneDrive prefix, return (sharepoint_base, query).
    Otherwise return (None, "").

    sharepoint_base is the URL prefix; append URL-encoded relative path + ?query for full link.
    """
    path_str = str(file_path.resolve())
    # Normalize for Windows
    path_str = path_str.replace("\\", "/")
    mappings = _load_mappings()
    for prefix, base, query in mappings:
        # Check if path contains the OneDrive prefix (e.g. "OneDrive - Agile by Design")
        if prefix in path_str:
            # Find where the prefix starts and get the part after it for relative path
            idx = path_str.find(prefix)
            after_prefix = path_str[idx + len(prefix) :].lstrip("/\\")
            # The SharePoint base typically ends at "Shared Documents" - we use it as-is
            # and the relative path (after prefix) gets appended
            return base, query
    return None, ""


def get_sharepoint_url_for_file(file_path: Path, sharepoint_base: str, query: str) -> str:
    """Build full SharePoint URL for a file. Caller provides base from get_sharepoint_base_for_path."""
    from urllib.parse import quote

    path_str = str(file_path.resolve())
    path_str = path_str.replace("\\", "/")
    mappings = _load_mappings()
    for prefix, base, _ in mappings:
        if prefix in path_str:
            idx = path_str.find(prefix)
            after_prefix = path_str[idx + len(prefix) :].lstrip("/\\")
            # If base ends with Shared%20Documents, avoid duplicating; use path after "Shared Documents"
            if "Shared Documents" in after_prefix or "Shared%20Documents" in after_prefix:
                for sep in ("Shared Documents/", "Shared Documents\\", "Shared%20Documents/", "Shared%20Documents\\"):
                    if sep in after_prefix:
                        after_prefix = after_prefix.split(sep, 1)[-1]
                        break
            encoded = quote(after_prefix, safe="/")
            return f"{base.rstrip('/')}/{encoded}?{query}"
    return ""


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python onedrive_to_sharepoint.py <file_path>")
        print("Returns SharePoint base URL if path is under configured OneDrive.")
        sys.exit(0)
    p = Path(sys.argv[1])
    base, query = get_sharepoint_base_for_path(p)
    if base:
        url = get_sharepoint_url_for_file(p, base, query)
        print(f"SharePoint base: {base}")
        print(f"Full URL: {url}")
    else:
        print("No mapping for this path. Add to sharepoint_mapping.json")
