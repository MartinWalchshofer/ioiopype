# -*- coding: utf-8 -*-
"""
ioiopype
-------

A realtime processing framework for python

:copyright: (c) 2024 by Martin Walchshofer

"""

# compatibility
from __future__ import absolute_import, division, print_function

# get version
from .__version__ import __version__

# allow lazy loading
#common nodes
#ondevices
from .common.o_devices.unicorn import Unicorn
from .common.o_devices.unicorn_simulator import UnicornSimulator

#inodes
from .common.i_nodes.csv_logger import CSVLogger
from .common.i_nodes.console_log import ConsoleLog
from .common.i_nodes.to_workspace import ToWorkspace

#onodes
from .common.o_nodes.data_generator import DataGenerator
from .common.o_nodes.frame import Frame

#ionodes
from .common.io_nodes.buffer import Buffer
from .common.io_nodes.pwelch import PWelch
from .common.io_nodes.downsample import Downsample
from .common.io_nodes.offset_correction import OffsetCorrection
from .common.io_nodes.butterworth_filter import ButterworthFilter
from .common.io_nodes.to_sample import ToSample

#pattern
from .pattern.i_node import INode
from .pattern.o_node import ONode
from .pattern.io_node import IONode
from .pattern.i_stream import IStream
from .pattern.o_stream import OStream
from .pattern.stream_info import StreamInfo

#functions
from .common.utilities.filter_types import FilterType

#desktop nodes
from .utilities.system import is_mobile, get_system
system = get_system()
ismobile = is_mobile()
if ismobile is False:
    from .desktop.i_nodes.frame_plot import FramePlot
    from .desktop.i_nodes.sample_plot import SamplePlot