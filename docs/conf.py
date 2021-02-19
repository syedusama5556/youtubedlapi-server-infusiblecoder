#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath('.')))
import youtubedlapi_server_infusiblecoder
import youtubedlapi_server_infusiblecoder.app

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinxcontrib.httpdomain',
]

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'youtubedlapi-server-infusiblecoder'
copyright = '2020-{now:%Y}, Syed Usama Ahmad'.format(now=datetime.datetime.now())

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = youtubedlapi_server_infusiblecoder.__version__
# The short X.Y version.
version = '.'.join(release.split('.')[:2])

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

ALLOWED_EXTRA_PARAMS = youtubedlapi_server_infusiblecoder.app.ALLOWED_EXTRA_PARAMS
extra_params = ', '.join('``{}``'.format(param) for param in ALLOWED_EXTRA_PARAMS.keys())
# the string will be included at the end of every source file that is read
rst_epilog = """
.. |info-extra-params| replace:: {extra_params}
""".format(extra_params=extra_params)
