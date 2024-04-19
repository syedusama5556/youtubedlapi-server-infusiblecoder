import functools
import json
import logging
import re
import traceback
import sys

import asyncio
import celery
from httpx import AsyncClient
from bilix.sites.bilibili import api as bilibili_api

from flask import Flask, Blueprint, current_app, jsonify, request, redirect, abort, make_response
import yt_dlp
from yt_dlp.version import __version__ as yt_dlp_version

# Import celery configuration
from youtubedlapi_server_infusiblecoder import celery_config  # Adjust import as necessary

from .version import __version__
from flask_caching import Cache

from celery import Celery

app = Flask(__name__)
app.config.from_pyfile('../application.cfg', silent=True)
app.config.from_mapping({
    'DEBUG': True,
    'CACHE_TYPE': "SimpleCache",
    'CACHE_DEFAULT_TIMEOUT': 300
})
# Explicitly set each configuration item
app.config.update(
    broker_url=celery_config.broker_url,
    result_backend=celery_config.result_backend,
    task_serializer=celery_config.task_serializer,
    result_serializer=celery_config.result_serializer,
    accept_content=celery_config.accept_content,
    timezone=celery_config.timezone,
    enable_utc=celery_config.enable_utc
)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['result_backend'], broker=app.config['broker_url'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

mycele = make_celery(app)

class SimpleYDL(yt_dlp.YoutubeDL):
    def __init__(self, *args, **kargs):
        super(SimpleYDL, self).__init__(*args, **kargs)
        self.add_default_info_extractors()




@mycele.task
def add(x, y):
    return x + y

@mycele.task
def get_videos(url, extra_params):
    ydl_params = {
        'format': 'best',
        'cachedir': False,
        'logger': logging.getLogger('youtube-dl'),
        'source_address': '0.0.0.0',  # Make sure this is appropriate for your network configuration
    }
    ydl_params.update(extra_params)

    print(f"Starting video extraction from URL: {url} with params: {extra_params}")
    try:
        logging.info(f"Starting video extraction from URL: {url} with params: {extra_params}")
        with SimpleYDL(ydl_params) as ydl:
            res = ydl.extract_info(url, download=False)
            print(f"Result: {res}")
            if res is None:
                logging.warning("No data returned from yt-dlp extraction.")
                return {}
            return res
    except Exception as e:
        logging.error(f"Error during video extraction: {e}", exc_info=True)
        # Raising here will propagate the exception back to .get()
        raise


api = Blueprint('api', __name__, url_prefix='/api')

def route_api(subpath, *args, **kwargs):
    return api.route(subpath, *args, **kwargs)

def set_access_control(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, tuple):
            response = make_response(result[0], result[1])
        else:
            response = make_response(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper

@api.errorhandler(Exception)
def handle_internal_server_error(error):
    logging.error(traceback.format_exc())
    return jsonify({'error': 'Internal server error. Please try again later.'}), 500

@api.errorhandler(yt_dlp.utils.DownloadError)
@api.errorhandler(yt_dlp.utils.ExtractorError)
def handle_yt_dlp_error(error):
    logging.error(traceback.format_exc())
    return jsonify({'error': 'Failed to download content. Please check the provided URL and try again.'}), 500

class WrongParameterTypeError(ValueError):
    def __init__(self, value, type, parameter):
        super().__init__(f'"{parameter}" expects a {type}, got "{value}"')

@api.errorhandler(WrongParameterTypeError)
def handle_wrong_parameter(error):
    logging.error(traceback.format_exc())
    return jsonify({'error': str(error)}), 400

@api.before_request
def block_on_user_agent():
    user_agent = request.user_agent.string
    if user_agent in current_app.config.get('FORBIDDEN_USER_AGENTS', []):
        abort(429)

def query_bool(value, name, default=None):
    if value is None:
        return default
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise WrongParameterTypeError(value, 'bool', name)


ALLOWED_EXTRA_PARAMS = {
    'format': str,
    'playliststart': int,
    'playlistend': int,
    'playlist_items': str,
    'playlistreverse': bool,
    'matchtitle': str,
    'rejecttitle': str,
    'writesubtitles': bool,
    'writeautomaticsub': bool,
    'allsubtitles': bool,
    'subtitlesformat': str,
    'subtitleslangs': list,
}


@api.route('/test')
@set_access_control
def test_add():
    result = add.delay(4, 4).get(timeout=10)
    return jsonify({'result': result})


@api.route('/info')
@set_access_control
def info():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL parameter is required'}), 400
        extra_params = {k: request.args[k] for k in request.args if k in ALLOWED_EXTRA_PARAMS}
        async_result = get_videos.delay(url, extra_params)
        result = async_result.get(timeout=10)  # May raise celery.exceptions.TimeoutError
        if not result:
            return jsonify({'error': 'No data found for the provided URL'}), 404
        return jsonify({'url': url, 'info': result})
    except celery.exceptions.TimeoutError:
        return jsonify({'error': 'Timeout while fetching video info'}), 504
    except Exception as e:
        logging.error(f"Error fetching video info: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@api.route('/play')
@set_access_control
def play():
    result = get_videos(request.args['url'], {}).get(timeout=10)
    if not result or not result.get('url'):
        return jsonify({'error': 'No playable content found for the provided URL'}), 404
    return redirect(result['url'])

@api.route('/extractors')
@set_access_control
def list_extractors():
    ie_list = [{
        'name': ie.IE_NAME,
        'working': ie.working(),
    } for ie in yt_dlp.gen_extractors()]
    return jsonify(extractors=ie_list)

@api.route('/version')
@set_access_control
def version():
    result = {
        'yt-dlp': yt_dlp_version,
        'youtubedlapi-server-infusiblecoder': __version__,
    }
    return jsonify(result)

@api.route('/bili')
@set_access_control
def get_bilibili_info():
    """
    Synchronous endpoint to get video information from a Bilibili video URL.
    """
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'URL parameter is required'})
        
        if not re.match(r"https?://(?:www\.)?bilibili\.com/video/[a-zA-Z0-9]+", url):
            return jsonify({'error': 'Only Bilibili video URLs are supported.'})

        async def fetch_info():
            async with AsyncClient(**bilibili_api.dft_client_settings) as client:
                return await bilibili_api.get_video_info(client, url)

        video_info = asyncio.run(fetch_info())
        response_data = json.loads(video_info.model_dump_json())
        return jsonify(response_data) 
    except Exception as err:
        logging.error(traceback.format_exc())
        return jsonify({'error': 'Failed to fetch video information.', 'details': str(err)})

app.register_blueprint(api)
from asgiref.wsgi import WsgiToAsgi
app_asgi = WsgiToAsgi(app)
