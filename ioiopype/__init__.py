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
from .i_nodes.console_log import ConsoleLog

#source nodes
from .o_nodes.data_generator import DataGenerator

#filter nodes
from .io_nodes.buffer import Buffer
from .io_nodes.framer import Framer