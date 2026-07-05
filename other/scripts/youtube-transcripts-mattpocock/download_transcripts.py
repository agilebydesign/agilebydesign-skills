#!/usr/bin/env python3
"""
Download transcripts for every video on a YouTube channel.

Default target: Matt Pocock's channel — https://www.youtube.com/@mattpocockuk

Strategy
--------
1. Enumerate every video on the channel with ``yt-dlp`` (flat listing, no download).
2. For each video, try to download an existing transcript in this order:
     a. Manually-authored English subtitles (best quality).
     b. YouTube's auto-generated English captions (usually available).
     c. Transcript from the ``youtube-transcript-api`` public endpoint
        (a different pathway; occasionally returns subs when yt-dlp can't).
3. If none of the above yields a transcript, fall back to generating one:
     - Download the audio track with ``yt-dlp``.
     - Transcribe it locally with OpenAI Whisper (open source, free,
       runs on CPU). Whisper is the "public service" fallback.

Outputs
-------
Everything is written under ``./transcripts/`` (override with ``--out-dir``):

    transcripts/
      index.json                     # metadata for every processed video
      <video_id>__<slug>.txt         # plain-text transcript
      <video_id>__<slug>.vtt         # original WebVTT (when available)
      <video_id>__<slug>.source.txt  # one word: youtube | youtube-api | whisper

The script is safely resumable: if a transcript already exists for a video
it is skipped unless ``--force`` is passed.

Usage
-----
    pip install -r requirements.txt
    python download_transcripts.py                   # Matt Pocock, default
    python download_transcripts.py --channel-url URL # any other channel
    python download_transcripts.py --limit 5         # first 5 videos only
    python download_transcripts.py --no-whisper      # skip local transcription
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional

DEFAULT_CHANNEL_URL = "https://www.youtube.com/@mattpocockuk"
DEFAULT_OUT_DIR = Path("transcripts")
DEFAULT_LANGS = ("en", "en-US", "en-GB", "en-IN", "en-AU", "en-CA")
WHISPER_DEFAULT_MODEL = "base"

log = logging.getLogger("yt-transcripts")


# ---------------------------------------------------------------------------
# data model
# ---------------------------------------------------------------------------


@dataclass
class VideoRecord:
    video_id: str
    title: str
    url: str
    duration_s: Optional[int] = None
    source: Optional[str] = None  # youtube | youtube-api | whisper | None
    transcript_path: Optional[str] = None
    vtt_path: Optional[str] = None
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


_SLUG_STRIP = re.compile(r"[^a-zA-Z0-9._-]+")


def slugify(text: str, max_len: int = 60) -> str:
    slug = _SLUG_STRIP.sub("-", text).strip("-").lower()
    return slug[:max_len] or "video"


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(
            f"Required binary '{name}' is not on PATH. "
            f"Install it (e.g. `pip install {name}` or your OS package manager) and retry."
        )
    return path


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    log.debug("$ %s", " ".join(cmd))
    return subprocess.run(cmd, check=False, text=True, capture_output=True, **kwargs)


# ---------------------------------------------------------------------------
# step 1: enumerate videos on the channel
# ---------------------------------------------------------------------------


def list_channel_videos(channel_url: str, limit: Optional[int] = None) -> list[VideoRecord]:
    """Return a list of VideoRecord for every video on the channel.

    Uses ``yt-dlp --flat-playlist --dump-json`` against ``<channel>/videos``,
    which is the cheapest way to enumerate uploads (no per-video HTTP hit).
    """
    yt_dlp = require_binary("yt-dlp")
    # Normalise to the /videos tab so we hit the uploads list specifically.
    target = channel_url.rstrip("/")
    if not target.endswith("/videos"):
        # /@handle -> /@handle/videos; channel/UCxxx -> channel/UCxxx/videos
        target = f"{target}/videos"

    log.info("enumerating videos on %s ...", target)
    cmd = [
        yt_dlp,
        "--flat-playlist",
        "--dump-json",
        "--no-warnings",
        "--ignore-errors",
        target,
    ]
    if limit:
        cmd += ["--playlist-end", str(limit)]

    proc = run(cmd)
    if proc.returncode != 0 and not proc.stdout.strip():
        raise SystemExit(f"yt-dlp failed to list channel:\n{proc.stderr}")

    records: list[VideoRecord] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        vid = item.get("id")
        if not vid or item.get("_type") == "playlist":
            continue
        title = item.get("title") or vid
        url = item.get("url") or f"https://www.youtube.com/watch?v={vid}"
        if url.startswith("http") is False:
            url = f"https://www.youtube.com/watch?v={vid}"
        records.append(
            VideoRecord(
                video_id=vid,
                title=title,
                url=url,
                duration_s=item.get("duration"),
            )
        )
    log.info("found %d videos", len(records))
    return records


# ---------------------------------------------------------------------------
# step 2a: try yt-dlp for existing subtitles
# ---------------------------------------------------------------------------


def _find_vtt(directory: Path, video_id: str) -> Optional[Path]:
    # yt-dlp writes files like "<id>.<lang>.vtt"
    for p in directory.glob(f"{video_id}.*.vtt"):
        return p
    return None


def try_download_subs_via_ytdlp(
    video_url: str,
    video_id: str,
    workdir: Path,
    langs: Iterable[str] = DEFAULT_LANGS,
) -> Optional[Path]:
    """Download subtitles (manual first, then auto) into workdir. Returns .vtt path or None."""
    yt_dlp = require_binary("yt-dlp")
    lang_expr = ",".join(langs)

    # Attempt 1: manually-authored subs only.
    manual = [
        yt_dlp,
        "--skip-download",
        "--write-subs",
        "--sub-langs", lang_expr,
        "--sub-format", "vtt",
        "--no-warnings",
        "-o", str(workdir / f"{video_id}.%(ext)s"),
        video_url,
    ]
    run(manual)
    vtt = _find_vtt(workdir, video_id)
    if vtt:
        return vtt

    # Attempt 2: auto-generated subs.
    auto = [
        yt_dlp,
        "--skip-download",
        "--write-auto-subs",
        "--sub-langs", lang_expr,
        "--sub-format", "vtt",
        "--no-warnings",
        "-o", str(workdir / f"{video_id}.%(ext)s"),
        video_url,
    ]
    run(auto)
    return _find_vtt(workdir, video_id)


# ---------------------------------------------------------------------------
# step 2b: try youtube-transcript-api as a secondary source
# ---------------------------------------------------------------------------


def try_youtube_transcript_api(video_id: str) -> Optional[str]:
    """Return plain-text transcript string, or None if unavailable.

    Handles both the legacy (<=0.6.x) and the current (>=1.x) API surfaces of
    ``youtube-transcript-api``:
      * legacy: ``YouTubeTranscriptApi.get_transcript(video_id, languages=...)``
        returned a list of ``{"text": ..., "start": ..., "duration": ...}`` dicts.
      * v1.x:   ``YouTubeTranscriptApi().fetch(video_id, languages=...)`` returns
        a ``FetchedTranscript`` whose ``.snippets`` items expose ``.text``.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError:
        return None

    langs = list(DEFAULT_LANGS)
    try:
        if hasattr(YouTubeTranscriptApi, "get_transcript"):
            chunks = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)  # type: ignore[attr-defined]
            texts = [c.get("text", "") for c in chunks]
        else:
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=langs)
            snippets = getattr(fetched, "snippets", None) or list(fetched)
            texts = []
            for s in snippets:
                t = getattr(s, "text", None)
                if t is None and isinstance(s, dict):
                    t = s.get("text", "")
                if t:
                    texts.append(t)
    except Exception as e:  # noqa: BLE001 — library raises many custom errors
        log.debug("youtube-transcript-api failed for %s: %s", video_id, e)
        return None

    joined = "\n".join(t.strip() for t in texts if t and t.strip())
    return joined or None


# ---------------------------------------------------------------------------
# step 3: whisper fallback (audio -> text)
# ---------------------------------------------------------------------------


def transcribe_with_whisper(
    video_url: str,
    video_id: str,
    workdir: Path,
    model_name: str = WHISPER_DEFAULT_MODEL,
) -> Optional[str]:
    """Download audio via yt-dlp and transcribe locally with Whisper."""
    try:
        import whisper  # type: ignore  # openai-whisper package
    except ImportError:
        log.warning(
            "whisper not installed; skipping local transcription. "
            "Install with: pip install -U openai-whisper (and ffmpeg on PATH)."
        )
        return None
    if not shutil.which("ffmpeg"):
        log.warning("ffmpeg not on PATH; whisper cannot decode audio. Skipping.")
        return None

    yt_dlp = require_binary("yt-dlp")
    audio_out_tmpl = str(workdir / f"{video_id}.%(ext)s")
    log.info("[%s] downloading audio for whisper ...", video_id)
    dl = run([
        yt_dlp,
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "--no-warnings",
        "-o", audio_out_tmpl,
        video_url,
    ])
    if dl.returncode != 0:
        log.warning("[%s] audio download failed: %s", video_id, dl.stderr.splitlines()[-1] if dl.stderr else "unknown")
        return None

    audio_path = next(workdir.glob(f"{video_id}.mp3"), None)
    if not audio_path:
        log.warning("[%s] no audio file produced", video_id)
        return None

    log.info("[%s] transcribing with whisper (%s) ...", video_id, model_name)
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio_path), verbose=False)
    return (result.get("text") or "").strip() or None


# ---------------------------------------------------------------------------
# vtt -> plain text
# ---------------------------------------------------------------------------


_VTT_TIMING = re.compile(r"\d\d:\d\d[:.]\d\d")
_VTT_TAG = re.compile(r"<[^>]+>")


def vtt_to_text(vtt_path: Path) -> str:
    """Very forgiving WebVTT -> plain-text converter with de-duplication.

    YouTube auto-caption VTTs are heavily overlapped (each line reappears in the
    next cue as a "rolling" caption). We strip cue timings/tags and drop
    consecutive duplicate lines to produce readable text.
    """
    out_lines: list[str] = []
    last: Optional[str] = None
    for raw in vtt_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line == "WEBVTT" or line.startswith("NOTE") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line or _VTT_TIMING.match(line):
            continue
        if line.isdigit():  # cue index
            continue
        cleaned = _VTT_TAG.sub("", line).strip()
        if not cleaned or cleaned == last:
            continue
        out_lines.append(cleaned)
        last = cleaned
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# per-video pipeline
# ---------------------------------------------------------------------------


def process_video(
    rec: VideoRecord,
    out_dir: Path,
    *,
    use_whisper: bool,
    whisper_model: str,
    force: bool,
) -> VideoRecord:
    slug = slugify(rec.title)
    stem = f"{rec.video_id}__{slug}"
    txt_path = out_dir / f"{stem}.txt"
    vtt_path = out_dir / f"{stem}.vtt"
    source_marker = out_dir / f"{stem}.source.txt"

    if txt_path.exists() and not force:
        log.info("[%s] transcript already exists, skipping (use --force to overwrite)", rec.video_id)
        rec.transcript_path = str(txt_path)
        if vtt_path.exists():
            rec.vtt_path = str(vtt_path)
        rec.source = source_marker.read_text(encoding="utf-8").strip() if source_marker.exists() else "cached"
        return rec

    with tempfile.TemporaryDirectory(prefix=f"ytt-{rec.video_id}-") as tmp:
        workdir = Path(tmp)

        # (a) yt-dlp subtitles (manual then auto)
        try:
            vtt = try_download_subs_via_ytdlp(rec.url, rec.video_id, workdir)
        except SystemExit:
            raise
        except Exception as e:  # noqa: BLE001
            log.warning("[%s] yt-dlp subs error: %s", rec.video_id, e)
            vtt = None

        if vtt and vtt.exists():
            log.info("[%s] found subtitles via yt-dlp", rec.video_id)
            shutil.copy2(vtt, vtt_path)
            txt_path.write_text(vtt_to_text(vtt) + "\n", encoding="utf-8")
            source_marker.write_text("youtube\n", encoding="utf-8")
            rec.source = "youtube"
            rec.vtt_path = str(vtt_path)
            rec.transcript_path = str(txt_path)
            return rec

        # (b) youtube-transcript-api
        text = try_youtube_transcript_api(rec.video_id)
        if text:
            log.info("[%s] found transcript via youtube-transcript-api", rec.video_id)
            txt_path.write_text(text + "\n", encoding="utf-8")
            source_marker.write_text("youtube-api\n", encoding="utf-8")
            rec.source = "youtube-api"
            rec.transcript_path = str(txt_path)
            return rec

        # (c) whisper
        if use_whisper:
            try:
                text = transcribe_with_whisper(rec.url, rec.video_id, workdir, model_name=whisper_model)
            except Exception as e:  # noqa: BLE001
                log.warning("[%s] whisper error: %s", rec.video_id, e)
                text = None
            if text:
                log.info("[%s] generated transcript with whisper", rec.video_id)
                txt_path.write_text(text + "\n", encoding="utf-8")
                source_marker.write_text(f"whisper:{whisper_model}\n", encoding="utf-8")
                rec.source = f"whisper:{whisper_model}"
                rec.transcript_path = str(txt_path)
                return rec

    rec.error = "no transcript available (subs missing, api empty, whisper disabled or failed)"
    log.warning("[%s] %s", rec.video_id, rec.error)
    return rec


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--channel-url", default=DEFAULT_CHANNEL_URL, help="YouTube channel URL (default: Matt Pocock).")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), type=Path, help="Where to write transcripts.")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N videos (useful for testing).")
    parser.add_argument("--no-whisper", action="store_true", help="Disable local Whisper fallback.")
    parser.add_argument("--whisper-model", default=os.environ.get("WHISPER_MODEL", WHISPER_DEFAULT_MODEL),
                        help="Whisper model size: tiny|base|small|medium|large (default: base).")
    parser.add_argument("--force", action="store_true", help="Re-process videos even if a transcript already exists.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging.")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    videos = list_channel_videos(args.channel_url, limit=args.limit)
    if not videos:
        log.error("no videos found on %s", args.channel_url)
        return 1

    processed: list[VideoRecord] = []
    for i, rec in enumerate(videos, 1):
        log.info("[%d/%d] %s — %s", i, len(videos), rec.video_id, rec.title)
        try:
            processed.append(process_video(
                rec,
                out_dir,
                use_whisper=not args.no_whisper,
                whisper_model=args.whisper_model,
                force=args.force,
            ))
        except KeyboardInterrupt:
            log.warning("interrupted; writing partial index")
            break
        except Exception as e:  # noqa: BLE001
            log.exception("[%s] unhandled error", rec.video_id)
            rec.error = str(e)
            processed.append(rec)

    index_path = out_dir / "index.json"
    index_path.write_text(
        json.dumps([asdict(r) for r in processed], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    ok = sum(1 for r in processed if r.transcript_path and not r.error)
    failed = sum(1 for r in processed if r.error)
    log.info("done. %d transcripts, %d failed. Index: %s", ok, failed, index_path)
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
