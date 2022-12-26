[![Downloads](https://pepy.tech/badge/youtubedlapi-server-infusiblecoder)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![Downloads](https://pepy.tech/badge/youtubedlapi-server-infusiblecoder/month)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder/month)
[![Downloads](https://pepy.tech/badge/youtubedlapi-server-infusiblecoder/week)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder/week)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)


youtubedlapi-server-infusiblecoder
=====================

A REST API server for getting the info for videos from different sites, powered by `youtube-dl <http://rg3.github.io/youtube-dl/>`_.
The installation instructions and the documentation are available at `Read the Docs <https://youtubedlapi-server-infusiblecoder.readthedocs.io/>`_.

About
-----

``youtubedlapi-server-infusiblecoder`` is released to the public domain, read the `license <LICENSE>`_ for more info.


Example
-----

youtubedlapi-server-infusiblecoder -p 8000 --host 127.0.0.1 --number-processes 1

or

youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1

or for bg run 

nohup youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1 &

