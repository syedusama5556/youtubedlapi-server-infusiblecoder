# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='youtubedlapi_server_infusiblecoder',
    version='3.0',
    description='An API server based on yt-dlp',
    long_description='A REST API server for getting the info for videos from different sites, powered by yt-dlp',
    author='Syed Usama Ahmad',
    author_email='syedusama5556@gmail.com',
    url='https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder',
    packages=['youtubedlapi_server_infusiblecoder'],
    entry_points={
        'console_scripts': [
            'youtubedlapi-server-infusiblecoder = youtubedlapi_server_infusiblecoder.server:main',
        ],
    },

    install_requires=[
        'Flask',
        'yt_dlp >= 2022.11.11',
    ],

    classifiers=[
        'Topic :: Multimedia :: Video',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
