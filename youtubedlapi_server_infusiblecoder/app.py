import json
import logging
import re
import asyncio
import uuid
import shutil
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Query
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
from yt_dlp.version import __version__ as yt_dlp_version
from httpx import AsyncClient
from bilix.sites.bilibili import api as bilibili_api

from .version import __version__

app = FastAPI(title="yt-dlp API Server", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = Path("temp_downloads")
TEMP_DIR.mkdir(exist_ok=True)
# ponytail: simple dict store, swap to DB if multi-instance needed
_downloads = {}

class SimpleYDL(yt_dlp.YoutubeDL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_default_info_extractors()

async def get_videos(url: str, extra_params: dict):
    ydl_params = {
        'format': 'best',
        'cachedir': False,
        'logger': logging.getLogger('youtube-dl'),
    }
    ydl_params.update(extra_params)

    try:
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, lambda: yt_dlp_extract(ydl_params, url))
        return res
    except Exception as e:
        logging.error(f"Error during video extraction: {e}")
        raise HTTPException(status_code=500, detail=f"Video extraction failed: {str(e)}")

def yt_dlp_extract(params, url):
    with SimpleYDL(params) as ydl:
        return ydl.extract_info(url, download=False)

async def flatten_result(result):
    if result is None:
        return []
    try:
        r_type = result.get('_type', 'video')
        if r_type == 'video':
            return [result]
        elif r_type in ['playlist', 'compat_list']:
            videos = []
            for entry in result.get('entries', []):
                if entry:
                    videos.extend(await flatten_result(entry))
            return videos
        else:
            raise ValueError(f"Unsupported type in result: {r_type}")
    except Exception as e:
        logging.error(f"Error in flatten_result: {e}")
        raise

def clean_old_downloads(max_age: int = 3600):
    now = time.time()
    expired = [fid for fid, d in _downloads.items() if now - d['created'] > max_age]
    for fid in expired:
        info = _downloads.pop(fid, None)
        if info:
            p = Path(info['path'])
            if p.exists():
                p.unlink(missing_ok=True)

# --- Existing endpoints ---

@app.get("/api/info")
async def info(url: str, flatten: Optional[bool] = True):
    try:
        result = await get_videos(url, {})
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for provided URL")
        if flatten:
            result = await flatten_result(result)
        return {"url": url, "videos": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/play")
async def play(url: str):
    try:
        result = await get_videos(url, {})
        if not result or not result.get('entries'):
            raise HTTPException(status_code=404, detail="No playable content found")
        return RedirectResponse(url=result['entries'][0]['url'])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/extractors")
async def list_extractors():
    return {"extractors": [{'name': ie.IE_NAME, 'working': ie.working()} for ie in yt_dlp.gen_extractors()]}

@app.get("/api/version")
async def version():
    return {'yt-dlp': yt_dlp_version, 'youtubedlapi-server-infusiblecoder': __version__}

@app.get("/api/bili")
async def get_bilibili_info(url: str):
    if not re.match(r"https?://(?:www\.)?bilibili\.com/video/[a-zA-Z0-9]+", url):
        raise HTTPException(status_code=400, detail="Only Bilibili video URLs are supported.")
    async with AsyncClient(**bilibili_api.dft_client_settings) as client:
        video_info = await bilibili_api.get_video_info(client, url)
        return json.loads(video_info.model_dump_json())

# --- New endpoints ---

@app.get("/api/formats")
async def list_formats(url: str):
    """List all available formats for a video."""
    result = await get_videos(url, {})
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    formats = result.get('formats', [])
    # Return minimal useful format info
    return {
        "url": url,
        "title": result.get('title'),
        "formats": [{
            "format_id": f.get('format_id'),
            "ext": f.get('ext'),
            "resolution": f.get('resolution') or f"{f.get('height', '?')}p",
            "filesize": f.get('filesize') or f.get('filesize_approx'),
            "tbr": f.get('tbr'),
            "vcodec": f.get('vcodec'),
            "acodec": f.get('acodec'),
            "fps": f.get('fps'),
        } for f in formats]
    }

@app.get("/api/subtitles")
async def list_subtitles(url: str):
    """List available subtitles for a video."""
    result = await get_videos(url, {'writesubtitles': True})
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    subs = result.get('subtitles', {})
    return {"url": url, "title": result.get('title'), "subtitles": subs}

@app.get("/api/search")
async def search(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(10, description="Max results"),
):
    """Search for videos on supported sites."""
    extra_params = {
        'default_search': 'ytsearch',
        'extract_flat': 'in_playlist',
    }
    result = await get_videos(q, extra_params)
    if not result or not result.get('entries'):
        raise HTTPException(status_code=404, detail="No results found")
    entries = result['entries'][:limit]
    return {
        "query": q,
        "results": [{
            "id": e.get('id'),
            "title": e.get('title'),
            "url": e.get('url') or e.get('webpage_url'),
            "duration": e.get('duration'),
            "thumbnail": e.get('thumbnail'),
            "channel": e.get('channel') or e.get('uploader'),
        } for e in entries]
    }

@app.get("/api/audio")
async def get_audio(url: str, format_id: Optional[str] = "bestaudio/best"):
    """Redirect to best audio stream URL."""
    result = await get_videos(url, {'format': format_id})
    if not result:
        raise HTTPException(status_code=404, detail="No audio found")
    if result.get('entries'):
        url_to_use = result['entries'][0].get('url')
    else:
        url_to_use = result.get('url')
    if not url_to_use:
        raise HTTPException(status_code=404, detail="No audio stream URL found")
    return {"url": url, "audio_url": url_to_use, "title": result.get('title'), "ext": result.get('ext', 'unknown')}

@app.get("/api/download")
async def download_video(
    url: str,
    format_id: Optional[str] = Query("best", description="Format ID to download"),
    background_tasks: BackgroundTasks = None,
):
    """Download a video to the server and return a temp streaming link."""
    clean_old_downloads()
    out_dir = TEMP_DIR / uuid.uuid4().hex
    out_dir.mkdir(parents=True, exist_ok=True)
    out_tmpl = str(out_dir / "%(title)s.%(ext)s")

    ydl_params = {
        'format': format_id,
        'outtmpl': out_tmpl,
        'cachedir': False,
        'logger': logging.getLogger('youtube-dl'),
        'max_filesize': 500_000_000,  # ponytail: 500MB cap, remove if self-hosting big files
    }

    loop = asyncio.get_event_loop()
    try:
        info = await loop.run_in_executor(None, lambda: download_sync(ydl_params, url))
    except Exception as e:
        shutil.rmtree(out_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

    if not info:
        shutil.rmtree(out_dir, ignore_errors=True)
        raise HTTPException(status_code=404, detail="Download produced no file")

    file_path = info['filepath']
    file_id = uuid.uuid4().hex
    ext = Path(file_path).suffix.lower()
    # ponytail: naive content-type mapping
    mime_map = {
        '.mp4': 'video/mp4', '.webm': 'video/webm', '.mkv': 'video/x-matroska',
        '.avi': 'video/x-msvideo', '.mov': 'video/quicktime',
        '.mp3': 'audio/mpeg', '.m4a': 'audio/mp4', '.wav': 'audio/wav',
        '.ogg': 'audio/ogg', '.aac': 'audio/aac',
    }
    _downloads[file_id] = {
        'path': str(file_path),
        'title': info.get('title', Path(file_path).stem),
        'ext': ext,
        'mime': mime_map.get(ext, 'application/octet-stream'),
        'created': time.time(),
    }

    return {
        "url": url,
        "title": info.get('title'),
        "file_id": file_id,
        "stream_url": f"/api/stream/{file_id}",
        "download_url": f"/api/stream/{file_id}?download=1",
        "expires_in": "1 hour",
        "filesize": info.get('filesize', Path(file_path).stat().st_size),
    }

def download_sync(params, url):
    with SimpleYDL(params) as ydl:
        info = ydl.extract_info(url, download=True)
        if info and info.get('requested_downloads'):
            dl = info['requested_downloads'][0]
            info['filepath'] = dl.get('filepath')
            info['filesize'] = dl.get('filesize', 0)
        return info

@app.get("/api/stream/{file_id}")
async def stream_file(file_id: str, download: Optional[bool] = False):
    """Stream or download a previously downloaded file via temp link."""
    entry = _downloads.get(file_id)
    if not entry:
        raise HTTPException(status_code=404, detail="File not found or expired")
    path = Path(entry['path'])
    if not path.exists():
        _downloads.pop(file_id, None)
        raise HTTPException(status_code=404, detail="File expired or deleted")
    filename = f"{entry['title']}{entry['ext']}"
    if download:
        return FileResponse(str(path), media_type=entry['mime'], filename=filename, headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        })
    return FileResponse(str(path), media_type=entry['mime'], filename=filename, headers={
        "Accept-Ranges": "bytes",
    })

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)}
    )

# ponytail: skip background cleanup worker; downloads expire naturally via clean_old_downloads called per download
