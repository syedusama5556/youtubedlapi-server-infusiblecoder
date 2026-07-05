import yt_dlp
import json

params = {
    "quiet": True,
    "no_warnings": True,
    "extract_flat": False,
}

ydl = yt_dlp.YoutubeDL(params)
try:
    info = ydl.extract_info("https://www.dailymotion.com/video/xal2ebm", download=False)
    print(json.dumps({"title": info.get("title")}, indent=2))
except Exception as e:
    print(f"ERROR: {e}")
