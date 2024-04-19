# -*- coding: utf-8 -*-

from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description_txt = (this_directory / "README.md").read_text()

setup(
    name="youtubedlapi_server_infusiblecoder",
    version="3.7.10",
    description="An API server based on yt-dlp",
    long_description=long_description_txt,
    long_description_content_type="text/markdown",
    author="Syed Usama Ahmad",
    author_email="syedusama5556@gmail.com",
    url="https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder",
    packages=["youtubedlapi_server_infusiblecoder"],
    entry_points={
        "console_scripts": [
            "youtubedlapi-server-infusiblecoder = youtubedlapi_server_infusiblecoder.server:main",
        ],
    },

    install_requires=[
        "fastapi",
        "Flask>=3.0.3",  # Ensuring version is updated to 3.0.3 as specified
        "yt_dlp>=2024.4.9",  # Corrected formatting to match typical Python package naming conventions
        "Flask-Caching",  # This is correct, noting duplication with flask_caching; potentially only one is needed
        "flask_caching",  # Review if both Flask-Caching and flask_caching are needed, as these might be a duplication
        "gevent",  # Ensure compatibility with both Flask and FastAPI if using this for asynchronous handling in Flask
        "uvicorn[standard]",  # Including 'standard' extras for additional functionality
        "bilix",  # Specific version may be required, depending on latest updates or features needed
        "httpx",  # Asynchronous HTTP client for FastAPI and potentially Flask async contexts
        "asgiref",  # Required for asynchronous apps, generally a dependency of Django/Channels but may be used with FastAPI for compatibility layers
        "gunicorn",  # WSGI HTTP Server for UNIX to serve Flask apps, ensure compatibility with Flask versions
        "redis",  # Commonly used for caching and session storage, crucial for tasks requiring quick data retrieval
        "celery",  # Asynchronous task queue/job queue based on distributed message passing
    ],

    classifiers=[
        "Topic :: Multimedia :: Video",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: Public Domain",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
    ],
)
