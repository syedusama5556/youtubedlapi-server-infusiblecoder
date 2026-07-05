[![PyPI](https://img.shields.io/pypi/v/youtubedlapi-server-infusiblecoder)](https://pypi.org/project/youtubedlapi-server-infusiblecoder/)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

youtubedlapi-server-infusiblecoder
=====================

A REST API server for getting video info from different sites, powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Requires Python >= 3.11. Uses [uv](https://docs.astral.sh/uv/) for package management.
Installs [Deno](https://deno.land) automatically in the Docker image (used by some yt-dlp extractors as a JavaScript runtime).

Installation
------------

```bash
# Install uv (if not installed)
pip install uv

# Clone and install
git clone https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder
cd youtubedlapi-server-infusiblecoder
uv sync
```

Or via pip:

```bash
pip install youtubedlapi-server-infusiblecoder
```

Usage
-----

```bash
uv run uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191 --workers 1 --log-level info
```

Or using the CLI:

```bash
uv run youtubedlapi-server-infusiblecoder --host 0.0.0.0 --port 9191
```

Run in background:

```bash
nohup uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191 --workers 1 --log-level info &
```

API Endpoints
-------------

### Info
- `GET /api/info?url=<video-url>` — Get video information
- `GET /api/formats?url=<video-url>` — List available formats/resolutions
- `GET /api/subtitles?url=<video-url>` — List available subtitles
- `GET /api/search?q=<query>&limit=10` — Search for videos on supported sites

### Playback
- `GET /api/play?url=<video-url>` — Redirect to video URL
- `GET /api/audio?url=<video-url>` — Get best audio stream URL
- `GET /api/download?url=<video-url>&format_id=best` — Download video, returns a temp streaming link
- `GET /api/stream/<file_id>` — Stream a downloaded file (temp link, expires in 1h)
- `GET /api/stream/<file_id>?download=1` — Force-download the temp file

### Server
- `GET /api/extractors` — List available extractors
- `GET /api/version` — Get version info
- `GET /api/bili?url=<bilibili-url>` — Get Bilibili video info

License
-------

Released to the public domain.
