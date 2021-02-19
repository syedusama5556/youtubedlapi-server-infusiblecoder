API
===

API methods
-----------

.. http:get:: /api/info

    Get the video information

    :query url: The video url
    :query boolean flatten: If ``True`` return a list of dictionaries in the ``videos`` field.
        Otherwise a single dictionary will be returned in the ``info`` field.

        .. versionchanged:: 0.2

            The default value is ``False``.

        .. deprecated:: 0.2

            This parameter will be removed in a future version, you'll have to implemenent this functionality in your client.

    :query \*: A whitelist of extra parameters are passed directly to the ``YoutubeDL`` object.
        Currently it supports: |info-extra-params|.
        See the `youtube-dl documentation <https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L92>`_ for more info


    :resheader Content-Type: ``application/json``
    :resheader Access-Control-Allow-Origin: ``*``

    :status 200: On success
    :status 400: For invalid query parameters
    :status 500: If the extraction fails

    |ex-request|

    .. sourcecode:: http

        GET /api/info?url=http://www.ted.com/talks/dan_dennett_on_our_consciousness.html&flatten=False HTTP/1.1

    **Example response**

    .. include:: example_info.rst.inc

    |ex-request|

    .. sourcecode:: http

        GET /api/info?url=http://www.ted.com/talks/dan_dennett_on_our_consciousness.html&flatten=True HTTP/1.1

    **Example response**

    .. include:: example_info_flatten.rst.inc


.. http:get:: /api/play

    Extract the info and redirect to the URL of the first video found for the requested URL.
    Useful for media players that accept HTTP URLs.
    Accepts the same parameters as :http:get:`/api/info`.

    :status 302: On success
    :status 400: For invalid query parameters
    :status 500: If the extraction fails

    .. versionadded:: 0.3

        Added endpoint.

    |ex-request|

    .. sourcecode:: http

        GET /api/play?url=http://www.ted.com/talks/dan_dennett_on_our_consciousness.html HTTP/1.1

    |ex-response|

    .. sourcecode:: http

        HTTP/1.0 302 FOUND
        Content-Type: text/html; charset=utf-8
        Location: http://download.ted.com/talks/DanDennett_2003-1500k.mp4?dnt

    |ex-request|

    .. sourcecode:: http

        GET /api/play?url=http://www.ted.com/talks/dan_dennett_on_our_consciousness.html&format=bestaudio HTTP/1.1

    |ex-response|

    .. sourcecode:: http

        HTTP/1.0 302 FOUND
        Content-Type: text/html; charset=utf-8
        Location: https://hls.ted.com/videos/DanDennett_2003/audio/600k.m3u8?uniqueId=5ed2e870


.. http:get:: /api/extractors

    Get the available extractors

    :resheader Content-Type: ``application/json``
    :resheader Access-Control-Allow-Origin: ``*``
    :status 200: On success

    |ex-request|

    .. sourcecode:: http

        GET /api/extractors HTTP/1.1

    |ex-response|

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Access-Control-Allow-Origin: *
        Content-Type: application/json

        {
            "extractors": [
                {
                    "name": "vimeo",
                    "working": true
                },
                {
                    "name": "TED",
                    "working": true
                },
                ...
            ]

        }


.. http:get:: /api/version

    Get the youtube-dl and youtubedlapi-server-infusiblecoder version

    :resheader Content-Type: ``application/json``
    :resheader Access-Control-Allow-Origin: ``*``
    :status 200: On success

    .. versionadded:: 0.3

        Added endpoint.


    |ex-request|

    .. sourcecode:: http

        GET /api/version HTTP/1.1

    |ex-response|

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Access-Control-Allow-Origin: *
        Content-Type: application/json

        {
            "youtube-dl": "2016.04.19",
            "youtubedlapi-server-infusiblecoder": "0.2"
        }

Test server
-----------

You can try the API by doing requests to ``http://youtube-dl.appspot.com``.



.. |ex-request| replace:: **Example request**


.. |ex-response| replace:: **Example response**
