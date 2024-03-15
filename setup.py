# -*- coding: utf-8 -*-

from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description_txt = (this_directory / "README.md").read_text()

setup(
    name="youtubedlapi_server_infusiblecoder",
    version="3.7.7",
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
        "Flask>=3.0.2",
        "yt_dlp >= 2023.12.30",
        "Flask-Caching",
        "flask_caching",
        "gevent",
        "uvicorn",
        "bilix", 
        "httpx",
        "asgiref",
        "gunicorn",
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
