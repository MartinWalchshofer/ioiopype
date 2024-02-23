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
#common nodes
#inodes
from .common.i_nodes.console_log import ConsoleLog

#onodes
from .common.o_nodes.data_generator import DataGenerator

#ionodes
from .common.io_nodes.buffer import Buffer
from .common.io_nodes.framer import Framer

#desktop nodes
from .utilities.system import is_mobile, get_system
system = get_system()
ismobile = is_mobile()
if ismobile is False:
    from .desktop.i_nodes.frame_plot import FramePlot
    from .desktop.i_nodes.sample_plot import SamplePlot