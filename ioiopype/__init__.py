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
#TODO LOAD PLATFORM SPECIFIC NODES ACCORDING TO PLATFORM

#common nodes
#inodes
from .common.i_nodes.console_log import ConsoleLog

#onodes
from .common.o_nodes.data_generator import DataGenerator

#ionodes
from .common.io_nodes.buffer import Buffer
from .common.io_nodes.framer import Framer