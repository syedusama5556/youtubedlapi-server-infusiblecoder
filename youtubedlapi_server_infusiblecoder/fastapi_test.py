import json
import logging
import re
import asyncio
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
from yt_dlp.version import __version__ as yt_dlp_version
from httpx import AsyncClient
from bilix.sites.bilibili import api as bilibili_api

from version import __version__

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        logging.info(f"Extracting video info from URL: {url} with params: {extra_params}")
        # Run yt_dlp operations in a thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, lambda: yt_dlp_extract(ydl_params, url))
        logging.info("Video extraction successful.")
        return res
    except Exception as e:
        logging.error(f"Error during video extraction: {e}")
        raise HTTPException(status_code=500, detail="Video extraction failed")

def yt_dlp_extract(params, url):
    with SimpleYDL(params) as ydl:
        return ydl.extract_info(url, download=False)


async def flatten_result(result):
    if result is None:
        # Handle the case where result is None
        # You can log this and return an empty list, or handle it differently as needed
        print("Received None result in flatten_result")  # Replace with logging if available
        return []

    try:
        r_type = result.get('_type', 'video')

        if r_type == 'video':
            return [result]
        elif r_type in ['playlist', 'compat_list']:
            videos = []
            for entry in result.get('entries', []):
                videos.extend(await flatten_result(entry))
            return videos
        else:
            raise ValueError(f"Unsupported type in result: {r_type}")
    except Exception as e:
        print(f"Error in flatten_result: {e}")  # Replace with logging if available
        raise



@app.get("/api/info")
async def info(url: str, flatten: Optional[bool] = True):
    try:
        result = await get_videos(url, {})
        if result is None:
            raise HTTPException(status_code=404, detail="No data found for provided URL")
        if flatten:
            result = await flatten_result(result)
        return {"url": url, "videos": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/play")
async def play(url: str):
    try:
        result = await get_videos(url, {})
        if not result or not result.get('entries'):
            raise HTTPException(status_code=404, detail="No playable content found")
        return RedirectResponse(url=result['entries'][0]['url'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/extractors")
async def list_extractors():
    return {"extractors": [{'name': ie.IE_NAME, 'working': ie.working()} for ie in yt_dlp.gen_extractors()]}

@app.get("/api/version")
async def version():
    return {'yt-dlp': yt_dlp_version,'youtubedlapi-server-infusiblecoder': __version__}

@app.get("/api/bili")
async def get_bilibili_info(url: str):
    if not re.match(r"https?://(?:www\.)?bilibili\.com/video/[a-zA-Z0-9]+", url):
        raise HTTPException(status_code=400, detail="Only Bilibili video URLs are supported.")
    async with AsyncClient(**bilibili_api.dft_client_settings) as client:
        video_info = await bilibili_api.get_video_info(client, url)
        return json.loads(video_info.model_dump_json())

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)}
    )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=9191)
