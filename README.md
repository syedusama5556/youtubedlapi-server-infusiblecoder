[![PyPI](https://img.shields.io/pypi/v/youtubedlapi-server-infusiblecoder)](https://pypi.org/project/youtubedlapi-server-infusiblecoder/)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder/month)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![Downloads](https://static.pepy.tech/badge/youtubedlapi-server-infusiblecoder/week)](https://pepy.tech/project/youtubedlapi-server-infusiblecoder)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)



youtubedlapi-server-infusiblecoder
=====================

A REST API server for getting the info for videos from different sites, powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)_.
The installation instructions and the documentation are available at [Read the Docs](https://youtubedlapi-server-infusiblecoder.readthedocs.io/)_.

About
-----

``youtubedlapi-server-infusiblecoder`` is released to the public domain, read the [License](https://raw.githubusercontent.com/syedusama5556/youtubedlapi-server-infusiblecoder/master/LICENSE.md) for more info.


NEW Example Usage
-----
``uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 127.0.0.1 --port 9191 --workers 1 --log-level info``

or

``uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 0.0.0.0 --port 9191 --workers 1 --log-level info``

or for running in bacground 

``nohup uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 0.0.0.0 --port 9191 --workers 1 --log-level info &``

Run in BG with A Repeted Job To Restart Server When Its Down
------------------------------------------------------------

create a script named 'bgapi.sh' add below code in the file 

```#!/bin/bash
while true
do
uvicorn youtubedlapi_server_infusiblecoder.app:app_asgi --host 0.0.0.0 --port 9191 --workers 1 --log-level info
sleep 2500
done
```
save it then run this command to run it in the BG

``nohup ./bgapi.sh &``



Old Example Usage
-----

``youtubedlapi-server-infusiblecoder -p 8000 --host 127.0.0.1 --number-processes 1``

or

``youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1``

or for running in bacground 

``nohup youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1 &``

Run in BG with A Repeted Job To Restart Server When Its Down
------------------------------------------------------------

create a script named 'bgapi.sh' add below code in the file 

```#!/bin/bash
while true
do
youtubedlapi-server-infusiblecoder -p 9191 --host 0.0.0.0 --number-processes 1
sleep 2500
done
```
save it then run this command to run it in the BG

``nohup ./bgapi.sh &``
