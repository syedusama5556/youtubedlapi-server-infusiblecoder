youtubedlapi-server-infusiblecoder
#################

Run the API server

.. program:: youtubedlapi-server-infusiblecoder

.. option:: -p <port>, --port <port>

    The port the server will use. The default port is 9191

.. option:: --host HOST

    The host the server will use. The default host is localhost

.. option:: -h , --help

    Display the help text

.. option:: --version

    Print the version of the server

.. option:: --log-level {debug,info,warning,error,critical}

    Log level for the server. The default is: info

Examples
********

.. code:: bash

    youtubedlapi-server-infusiblecoder -p 8000 --host 127.0.0.1

Or directly with uvicorn:

.. code:: bash

    uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191 --workers 1
