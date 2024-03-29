import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gae/lib'))

# Monkeypatch some yt_dlp. functions that use features not available in GAE
import yt_dlp
# Modifying yt_dlp .utils.get_cachedir doesn't work
yt_dlp.extractor.youtube.get_cachedir = lambda *args, **kargs: None


from youtubedlapi_server_infusiblecoder.app import app  # noqa: app is used by GAE
