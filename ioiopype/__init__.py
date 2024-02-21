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
#sink nodes
from .sink_nodes.console_log import ConsoleLog

#source nodes
from .source_nodes.data_generator import DataGenerator

#filter nodes
from .filter_nodes.buffer import Buffer