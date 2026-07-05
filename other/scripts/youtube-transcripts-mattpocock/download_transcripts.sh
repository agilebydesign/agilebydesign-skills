#!/usr/bin/env bash
# Thin wrapper: cd into this script's dir, run download_transcripts.py,
# forwarding any extra arguments (e.g. --limit, --no-whisper, --force).
#
# Usage:
#   ./download_transcripts.sh                 # Matt Pocock, full channel
#   ./download_transcripts.sh --limit 3       # first 3 videos only
#   ./download_transcripts.sh --channel-url URL

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$here"

PY="${PYTHON:-python3}"

if ! command -v yt-dlp >/dev/null 2>&1; then
    echo "error: yt-dlp is required. Install with: pip install -U yt-dlp" >&2
    exit 1
fi

exec "$PY" download_transcripts.py "$@"
