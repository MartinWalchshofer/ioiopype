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
#inodes
from .common.i_nodes.csv_logger import CSVLogger
from .common.i_nodes.console_log import ConsoleLog
from .common.i_nodes.to_workspace import ToWorkspace
from .common.i_nodes.udp_sender import UDPSender

#onodes
from .common.o_nodes.ble_heart_rate import BLEHeartRate
from .common.o_nodes.ble_heart_rate_simulator import BLEHeartRateSimulator
from .common.o_nodes.constant import Constant
from .common.o_nodes.noise_generator import NoiseGenerator
from .common.o_nodes.signal_generator import SignalGenerator
from .common.o_nodes.frame import Frame
from .common.o_nodes.udp_receiver import UDPReceiver
from .common.o_nodes.csv_reader import CSVReader

#ionodes
from .common.io_nodes.buffer import Buffer
from .common.io_nodes.butterworth_filter import ButterworthFilter
from .common.io_nodes.butterworth_filtfilt import ButterworthFiltFilt
from .common.io_nodes.complementary_filter import ComplementaryFilter
from .common.io_nodes.deserialize import Deserialize
from .common.io_nodes.downsample import Downsample
from .common.io_nodes.get_range import GetRange
from .common.io_nodes.operation import Operation
from .common.io_nodes.lfhf import LFHF
from .common.io_nodes.log import Log
from .common.io_nodes.mux import Mux
from .common.io_nodes.movement_detector import MovementDetector
from .common.io_nodes.offset_correction import OffsetCorrection
from .common.io_nodes.poincare import Poincare
from .common.io_nodes.pwelch import PWelch
from .common.io_nodes.sqrt import Sqrt
from .common.io_nodes.square import Square
from .common.io_nodes.serialize import Serialize
from .common.io_nodes.to_sample import ToSample
from .common.io_nodes.transpose import Transpose

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
    from .desktop.i_nodes.spectrum_plot import SpectrumPlot