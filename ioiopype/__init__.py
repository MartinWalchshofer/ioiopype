# -*- coding: utf-8 -*-
"""
ioiopype
-------

A toolbox for realtime signalprocessing

:copyright: (c) 2024 by Martin Walchshofer

"""

# compatibility
from __future__ import absolute_import, division, print_function

# get version
from .__version__ import __version__

# allow lazy loading
from .pattern.input_stream import InputStream
from .pattern.output_stream import OutputStream
from .pattern.input_node import InputNode
from .pattern.output_node import OutputNode

from .filters.console_log import ConsoleLog
from .filters.data_generator import DataGenerator