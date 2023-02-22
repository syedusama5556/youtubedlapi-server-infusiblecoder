import functools
import logging
import traceback
import sys

from flask import Flask, Blueprint, current_app, jsonify, request, redirect, abort
import yt_dlp

from yt_dlp import YoutubeDL
from .version import __version__
import subprocess
import os
import json

if not hasattr(sys.stderr, 'isatty'):
    # In GAE it's not defined and we must monkeypatch
    sys.stderr.isatty = lambda: False


class SimpleYDL(YoutubeDL):
    def __init__(self, *args, **kargs):
        super(SimpleYDL, self).__init__(*args, **kargs)
        self.add_default_info_extractors()


def get_videos(url, extra_params):
    '''
    Get a list with a dict for every video founded
    '''
    ydl_params = {
        'format': 'best',
        'cachedir': False,
        'logger': current_app.logger.getChild('yt-dlp'),
    }
    ydl_params.update(extra_params)
    ydl = SimpleYDL(ydl_params)
    res = ydl.extract_info(url, download=False)
    return res


def flatten_result(result):
    r_type = result.get('_type', 'video')
    if r_type == 'video':
        videos = [result]
    elif r_type == 'playlist':
        videos = []
        for entry in result['entries']:
            videos.extend(flatten_result(entry))
    elif r_type == 'compat_list':
        videos = []
        for r in result['entries']:
            videos.extend(flatten_result(r))
    return videos


api = Blueprint('api', __name__)


def route_api(subpath, *args, **kargs):
    return api.route('/api/' + subpath, *args, **kargs)


def set_access_control(f):
    @functools.wraps(f)
    def wrapper(*args, **kargs):
        response = f(*args, **kargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper


@api.errorhandler(yt_dlp.utils.DownloadError)
@api.errorhandler(yt_dlp.utils.ExtractorError)
def handle_youtube_dl_error(error):
    logging.error(traceback.format_exc())
    result = jsonify({'error': str(error)})
    result.status_code = 500
    return result


class WrongParameterTypeError(ValueError):
    def __init__(self, value, type, parameter):
        message = '"{}" expects a {}, got "{}"'.format(parameter, type, value)
        super(WrongParameterTypeError, self).__init__(message)


@api.errorhandler(WrongParameterTypeError)
def handle_wrong_parameter(error):
    logging.error(traceback.format_exc())
    result = jsonify({'error': str(error)})
    result.status_code = 400
    return result


@api.before_request
def block_on_user_agent():
    user_agent = request.user_agent.string
    forbidden_uas = current_app.config.get('FORBIDDEN_USER_AGENTS', [])
    if user_agent in forbidden_uas:
        abort(429)


def query_bool(value, name, default=None):
    if value is None:
        return default
    value = value.lower()
    if value == 'true':
        return True
    elif value == 'false':
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


def get_result():
    url = request.args['url']
    extra_params = {}
    for k, v in request.args.items():
        if k in ALLOWED_EXTRA_PARAMS:
            convertf = ALLOWED_EXTRA_PARAMS[k]
            if convertf == bool:
                convertf = lambda x: query_bool(x, k)
            elif convertf == list:
                convertf = lambda x: x.split(',')
            extra_params[k] = convertf(v)
    return get_videos(url, extra_params)


@route_api('info')
@set_access_control
def info():
    url = request.args['url']
    if 'instagram.com' in url or 'fb.watch' in url or 'facebook.com' in url:
        result = subprocess.run(["yt-dlp", "--dump-json", "--no-cache-dir", str(url)], stdout=subprocess.PIPE, shell=True, encoding='utf-8')
        result = json.loads(result.stdout)
        key = 'info'
        if query_bool(request.args.get('flatten'), 'flatten', False):
            result = flatten_result(result)
            key = 'videos'
        result = {
            'url': url,
            key: result,
        }
        return jsonify(result)
    else:  
        result = get_result()
        key = 'info'
        if query_bool(request.args.get('flatten'), 'flatten', False):
            result = flatten_result(result)
            key = 'videos'
        result = {
            'url': url,
            key: result,
        }
        return jsonify(result)
 

@route_api('play')
def play():
    result = flatten_result(get_result())
    return redirect(result[0]['url'])


# def getInsta(url):
#     result = subprocess.run(["yt-dlp", "--dump-json", "--no-cache-dir", str(url)], stdout=subprocess.PIPE, shell=True, encoding='utf-8')
#     result = json.loads(result.stdout)
#     key = 'info'
#     if query_bool(request.args.get('flatten'), 'flatten', False):
#         result = flatten_result(result)
#         key = 'videos'
#     result = {
#         'url': url,
#         key: result,
#     }
#     return jsonify(result)


@route_api('extractors')
@set_access_control
def list_extractors():
    ie_list = [{
        'name': ie.IE_NAME,
        'working': ie.working(),
    } for ie in yt_dlp.gen_extractors()]
    return jsonify(extractors=ie_list)


@route_api('version')
@set_access_control
def version():
    result = {
        'yt-dlp': str(yt_dlp.version.__version__),
        'youtube-dl-api-server': __version__,
    }
    return jsonify(result)

app = Flask(__name__)
app.register_blueprint(api)
app.config.from_pyfile('../application.cfg', silent=True)
