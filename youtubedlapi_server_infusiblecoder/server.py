import argparse
import uvicorn
from .version import __version__

"""
    A server for providing the app anywhere, no need for GAE
"""

def main():
    desc = """
           The yt-dlp API server.
           """

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        '-p', '--port',
        default=9191,
        type=int,
        help='The port the server will use. The default is: %(default)s',
    )

    parser.add_argument(
        '--host',
        default='localhost',
        type=str,
        help='The host the server will use. The default is: %(default)s',
    )

    parser.add_argument(
        '--log-level',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Log level for the server. The default is: %(default)s',
    )

    parser.add_argument('--version', action='store_true',
                        help='Print the version of the server')

    args = parser.parse_args()
    if args.version:
        print(__version__)
        exit(0)

    # Ensure the Flask application is imported here
    from .app import app

    # Convert Flask app to ASGI
    uvicorn.run(app, host=args.host, port=args.port, log_level=args.log_level)
