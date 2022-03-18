# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='youtubedlapi_server_infusiblecoder',
    version='1.9',
    description='An API server based on youtube_dl',
    long_description='Get the videos from different sites using a server running youtube_dl',
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
        'yt_dlp >= 2022.3.8.2',
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
