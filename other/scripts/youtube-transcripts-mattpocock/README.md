# YouTube Channel Transcript Downloader

Downloads a transcript for **every video** on a YouTube channel. Defaults to
Matt Pocock's channel — <https://www.youtube.com/@mattpocockuk>.

## How it works

For each video, the script tries these sources **in order** and stops at the
first success:

1. **Existing YouTube subtitles** (manually authored, English variants) via `yt-dlp`.
2. **Auto-generated YouTube captions** via `yt-dlp`.
3. **`youtube-transcript-api`** — a different public endpoint that occasionally
   returns captions when `yt-dlp` can't reach them.
4. **Local transcription with OpenAI Whisper** — downloads the audio track and
   runs it through the open-source Whisper model on your machine. This is the
   "create the transcript using a public service" fallback. No API key needed.

Whisper is optional. Pass `--no-whisper` to skip it (videos with no captions
will simply be recorded as failed in `index.json`).

## Requirements

- Python 3.9+
- `yt-dlp` on `PATH` (`pip install -U yt-dlp`)
- **For the Whisper fallback only:** `ffmpeg` on `PATH` and the
  `openai-whisper` package. On Debian/Ubuntu: `sudo apt install ffmpeg`.

Install everything at once:

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Full channel (Matt Pocock)
./download_transcripts.sh

# A different channel
./download_transcripts.sh --channel-url https://www.youtube.com/@somechannel

# Test run: first 3 videos only
./download_transcripts.sh --limit 3

# Skip the local Whisper fallback (captions-only mode)
./download_transcripts.sh --no-whisper

# Re-process everything (overwrites existing transcripts)
./download_transcripts.sh --force

# Larger Whisper model for better accuracy (slower, needs more RAM)
./download_transcripts.sh --whisper-model small
```

Or invoke the Python script directly:

```bash
python download_transcripts.py --help
```

## Output layout

Everything lands under `./transcripts/` (override with `--out-dir`):

```
transcripts/
  index.json                              # metadata for every processed video
  <video_id>__<title-slug>.txt            # plain-text transcript
  <video_id>__<title-slug>.vtt            # original WebVTT (only when downloaded from YouTube)
  <video_id>__<title-slug>.source.txt     # provenance: youtube | youtube-api | whisper:<model>
```

`index.json` records the video id, title, URL, duration, chosen source, output
paths, and any error — handy for auditing or resuming.

## Notes

- The script is **resumable**. Re-running skips videos that already have a
  `.txt` output unless you pass `--force`.
- YouTube throttles heavy scraping. If you enumerate a very large channel you
  may see occasional 429s from `yt-dlp`; the script logs and moves on.

## Troubleshooting

- **"Sign in to confirm you're not a bot"** from `yt-dlp`, or an
  `IpBlocked` / `RequestBlocked` error from `youtube-transcript-api`:
  YouTube blocks most cloud-provider IP ranges (AWS, GCP, Azure, etc.).
  Run the script from a residential/office network, or supply cookies via
  `yt-dlp --cookies-from-browser <browser>` (edit the script or wrap
  `yt-dlp` in an alias). See
  <https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp>.
- **`yt-dlp` warns about missing JS runtime:** install Deno
  (`curl -fsSL https://deno.land/install.sh | sh`) or Node, then re-run.
  Modern YouTube extraction sometimes needs one.
- **Whisper is slow:** the default `base` model is CPU-friendly but not fast.
  Use `--whisper-model tiny` for a quick pass, or run on a machine with a
  CUDA GPU (Whisper auto-detects it).
- The Whisper fallback uses the `base` model by default (~140 MB, CPU-friendly).
  Use `--whisper-model small`, `medium`, or `large` for better quality; those
  need progressively more RAM and time.
- WebVTT → plain text is done in-process. Rolling / duplicated auto-caption
  lines are collapsed so the resulting `.txt` reads naturally.
