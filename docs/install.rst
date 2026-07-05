Install the server
##################

How to install **youtubedlapi-server-infusiblecoder**

Requirements
************

- Python >= 3.11
- `uv <https://docs.astral.sh/uv/>`_ (recommended) or pip

Using uv (recommended)
**********************

.. code:: bash

    git clone https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder
    cd youtubedlapi-server-infusiblecoder
    uv sync

Then run with:

.. code:: bash

    uv run uvicorn youtubedlapi_server_infusiblecoder.app:app --host 0.0.0.0 --port 9191

Using pip
*********

.. code:: bash

    pip install youtubedlapi-server-infusiblecoder

Then run with:

.. code:: bash

    youtubedlapi-server-infusiblecoder --host 0.0.0.0 --port 9191

From source
***********

.. code:: bash

    git clone https://github.com/syedusama5556/youtubedlapi-server-infusiblecoder
    cd youtubedlapi-server-infusiblecoder
    pip install -e .

Then run:

.. code:: bash

    youtubedlapi-server-infusiblecoder --host 0.0.0.0 --port 9191
