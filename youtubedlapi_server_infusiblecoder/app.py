import functools
import logging
import traceback
import sys

from flask import Flask, Blueprint, current_app, jsonify, request, redirect, abort, make_response
import yt_dlp
from yt_dlp.version import __version__ as yt_dlp_version

from .version import __version__


if not hasattr(sys.stderr, 'isatty'):
    # In GAE it's not defined and we must monkeypatch
    sys.stderr.isatty = lambda: False


class SimpleYDL(yt_dlp.YoutubeDL):
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
        'logger': current_app.logger.getChild('youtube-dl'),
    }
    ydl_params.update(extra_params)

    try:
        current_app.logger.info(f"Extracting video info from URL: {url} with params: {extra_params}")
        with SimpleYDL(ydl_params) as ydl:
            res = ydl.extract_info(url, download=False)
        current_app.logger.info("Video extraction successful.")
        return res
    except Exception as e:
        current_app.logger.error(f"Error during video extraction: {e}")
        raise 


def flatten_result(result):
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
                videos.extend(flatten_result(entry))
            return videos
        else:
            raise ValueError(f"Unsupported type in result: {r_type}")
    except Exception as e:
        print(f"Error in flatten_result: {e}")  # Replace with logging if available
        raise


api = Blueprint('api', __name__)


def route_api(subpath, *args, **kargs):
    return api.route('/api/' + subpath, *args, **kargs)


def set_access_control(f):
    @functools.wraps(f)
    def wrapper(*args, **kargs):
        result = f(*args, **kargs)

        # Check if the result is a tuple (body, status_code)
        if isinstance(result, tuple):
            # Create a response object from the tuple
            response = make_response(result[0], result[1])
        else:
            response = make_response(result)

        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper


@api.errorhandler(Exception)
def handle_internal_server_error(error):
    logging.error(traceback.format_exc())
    result = jsonify({'error': 'Internal server error. Please try again later.'})
    result.status_code = 500
    return result

@api.errorhandler(yt_dlp.utils.DownloadError)
@api.errorhandler(yt_dlp.utils.ExtractorError)
def handle_yt_dlp_error(error):
    logging.error(traceback.format_exc())
    result = jsonify({'error': 'Failed to download content. Please check the provided URL and try again.'})
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
    try:
        url = request.args['url']
        extra_params = {}
        for k, v in request.args.items():
            if k in ALLOWED_EXTRA_PARAMS:
                convertf = ALLOWED_EXTRA_PARAMS[k]
                if convertf == bool:
                    def convertf(x): return query_bool(x, k)
                elif convertf == list:
                    def convertf(x): return x.split(',')
                extra_params[k] = convertf(v)
        result = get_videos(url, extra_params)
        if result is None:
            # Handle the case where result is None
            # You can log this error or handle it as per your application's needs
            print(f"No result returned from get_videos for URL: {url}")  # Replace with logging
            return None  # Or handle it differently as needed
        return result
    except:
        return None
        
@route_api('info')
@set_access_control
def info():
    try:
        url = request.args['url']
        result = get_result()
        if result is None:
            return jsonify({'error': 'No data found for the provided URL'}), 404

        key = 'info'
        if query_bool(request.args.get('flatten'), 'flatten', True):
            result = flatten_result(result)
            key = 'videos'
        result = {
            'url': url,
            key: result,
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Error  {e}'}), 500

@route_api('play')
def play():
    result = flatten_result(get_result())
    if result is None or not result:
        return jsonify({'error': 'No playable content found for the provided URL'}), 404

    return redirect(result[0]['url'])


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
        'yt-dlp': yt_dlp_version,
        'youtubedlapi-server-infusiblecoder': __version__,
    }
    return jsonify(result)


app = Flask(__name__)
app.register_blueprint(api)
app.config.from_pyfile('../application.cfg', silent=True)