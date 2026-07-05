import yt_dlp
from yt_dlp.networking.impersonate import ImpersonateTarget

ydl = yt_dlp.YoutubeDL()
director = ydl._request_director
for name, handler in director.handlers.items():
    print(f"Handler: {name} - {type(handler).__name__}")
    if hasattr(handler, "is_supported_target"):
        t = ImpersonateTarget(client="firefox")
        print(f"  supports firefox: {handler.is_supported_target(t)}")
        print(f"  supported targets: {len(list(handler.supported_targets))}")
    else:
        print(f"  no impersonation support")
