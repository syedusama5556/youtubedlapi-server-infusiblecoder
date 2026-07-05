[![PyPI](https://img.shields.io/pypi/v/youtubedlapi-server-infusiblecoder)](https://pypi.org/project/youtubedlapi-server-infusiblecoder/)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

youtubedlapi-server-infusiblecoder
=====================

A REST API server for getting video info from different sites, powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

Requires Python >= 3.11. Uses [uv](https://docs.astral.sh/uv/) for package management.

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

- `GET /api/info?url=<video-url>` — Get video information
- `GET /api/play?url=<video-url>` — Redirect to video URL
- `GET /api/extractors` — List available extractors
- `GET /api/version` — Get version info
- `GET /api/bili?url=<bilibili-url>` — Get Bilibili video info

License
-------

Released to the public domain.
