[![PyPI](https://img.shields.io/pypi/v/youtubedlapi-server-infusiblecoder)](https://pypi.org/project/youtubedlapi-server-infusiblecoder/)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

youtubedlapi-server-infusiblecoder
=====================

A REST API server for video info, downloads, and streaming — powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) (nightly).

Requires **Python >= 3.11**. Uses [uv](https://docs.astral.sh/uv/) for package management.
The Docker image includes [Deno](https://deno.land) + [FFmpeg](https://ffmpeg.org) for JavaScript extractors and video merging.

Installation
------------

```bash
pip install youtubedlapi-server-infusiblecoder
```

Or from source:

```bash
git clone https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder
cd youtubedlapi-server-infusiblecoder
pip install uv
uv sync
```

### Docker

```bash
docker build -t youtubedlapi .
docker run -p 9191:9191 youtubedlapi
```

Usage
-----

```bash
uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191
```

Or via the CLI:

```bash
youtubedlapi-server-infusiblecoder --host 0.0.0.0 --port 9191
```

Dependencies
------------

The server auto-detects these at startup:

| Dep | Required for |
|-----|-------------|
| [curl-cffi](https://github.com/lexiforest/curl_cffi) | Browser impersonation (TLS fingerprint bypass) — enables **Dailymotion** |
| [yt-dlp-ejs](https://github.com/yt-dlp/ejs) + Deno/Node | Full YouTube extractor support |
| [FFmpeg](https://ffmpeg.org) | Merging bestvideo+bestaudio, post-processing |
| [brotli](https://github.com/google/brotli) | Brotli content encoding support |
| [websockets](https://github.com/aaugustin/websockets) | WebSocket-based downloads |
| [pycryptodomex](https://github.com/Legrandin/pycryptodome) | AES-128 HLS stream decryption |
| [mutagen](https://github.com/quodlibet/mutagen) | Thumbnail embedding |

Install any missing deps with:

```bash
pip install curl-cffi yt-dlp-ejs brotli websockets pycryptodomex mutagen
```

API Endpoints
-------------

All responses are JSON unless noted.

### Info

| Endpoint | Description |
|----------|-------------|
| `GET /api/info?url=<url>&flatten=true` | Full video/playlist info from yt-dlp |
| `GET /api/formats?url=<url>` | All available formats (resolution, codec, bitrate, filesize) |
| `GET /api/subtitles?url=<url>` | Available subtitle languages |
| `GET /api/search?q=<query>&limit=10` | Search videos on supported sites |

### Download & Stream

| Endpoint | Description |
|----------|-------------|
| `GET /api/download?url=<url>&format_id=best` | Download a video, returns a temp streaming link (auto-expires 1h, 500MB cap, auto-merges video+audio with ffmpeg) |
| `GET /api/stream/<file_id>` | Stream the downloaded file (supports range requests for seeking) |
| `GET /api/stream/<file_id>?download=1` | Force-download the file with original filename |
| `GET /api/audio?url=<url>` | Get best audio-only stream URL |
| `GET /api/play?url=<url>` | Redirect to the video's direct stream URL |

### Server

| Endpoint | Description |
|----------|-------------|
| `GET /api/extractors` | List all supported sites/extractors |
| `GET /api/version` | yt-dlp & server versions |
| `GET /api/status` | Check installed deps (ffmpeg, deno, node, js_runtimes) |
| `GET /api/bili?url=<bilibili-url>` | Bilibili video info (via bilix) |

### Example: Download & Stream Flow

```bash
# 1. Download a video
curl "http://localhost:9191/api/download?url=https://youtube.com/watch?v=..."
# → { "file_id": "abc123", "stream_url": "/api/stream/abc123", ... }

# 2. Stream it (open in browser or player)
curl "http://localhost:9191/api/stream/abc123" -o video.mp4

# 3. Or embed in a video tag / VLC
# vlc http://localhost:9191/api/stream/abc123
```

Sample Usage (Tested URLs)
--------------------------

All tested with the latest nightly yt-dlp.

```bash
# YouTube — info, formats, subtitles, audio, search
curl "http://localhost:9191/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&flatten=true"
curl "http://localhost:9191/api/formats?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
curl "http://localhost:9191/api/subtitles?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
curl "http://localhost:9191/api/audio?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
curl "http://localhost:9191/api/search?q=never+gonna+give+you+up&limit=3"

# Vimeo
curl "http://localhost:9191/api/info?url=https://vimeo.com/76979871&flatten=true"

# TED
curl "http://localhost:9191/api/info?url=https://www.ted.com/talks/chloe_valdary_how_love_can_help_repair_social_inequality&flatten=true"

# Dailymotion (requires curl-cffi)
curl "http://localhost:9191/api/info?url=https://www.dailymotion.com/video/xal2ebm&flatten=true"

# Bilibili
curl "http://localhost:9191/api/bili?url=https://www.bilibili.com/video/BV1GJ411x7"
```

### Handling Failed Sites

These are known limitations — no server-side fix possible:

| Site | Issue |
|------|-------|
| Spotify | DRM protected, not supported by yt-dlp |
| Instagram (image posts) | No video available |
| TikTok (blocked regions) | IP blocked from accessing the post |
| Facebook | API parse error — needs yt-dlp extractor update |

Project Structure
-----------------

```
src/
└── youtubedlapi_server_infusiblecoder/   # Python package
    ├── app.py         # FastAPI app with all endpoints
    ├── server.py      # CLI entry point
    ├── __init__.py
    ├── __main__.py
    └── version.py
deploy/              # Docker, K8s, GAE, Heroku configs
docs/                # Sphinx documentation
devscripts/          # Build & publish scripts
test/                # Tests
```

Development
-----------

```bash
uv sync --group dev
uv run pytest
```


License
-------

Released to the public domain.
