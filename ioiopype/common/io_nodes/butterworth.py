from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
import numpy as np
from scipy.signal import butter, lfilter
from enum import Enum

class Butterworth(IONode):
    class FilterType(Enum):
        Lowpass = 1
        Highpass = 2
        Bandpass = 3
        Notch = 4

    def __init__(self, type, order, cutoffFrequencies):
        super().__init__()
        self.add_i_stream(IStream(0, 'sample'))
        self.add_o_stream(OStream(0,'sample'))
        if type is self.FilterType.Lowpass or type is self.FilterType.Highpass:
            if len(cutoffFrequencies) != 1:
                raise ValueError("Number of cutoff frequencies must be 1 for high and lowpass filters.")
        if type is self.FilterType.Bandpass or type is self.FilterType.Notch:
            if len(cutoffFrequencies) != 2:
                raise ValueError("Number of cutoff frequencies must be 2 for bandpass and notch filters.")
        if type is self.FilterType.Lowpass:
            self.b, self.a = butter(order, cutoffFrequencies,'lowpass', analog=False)
        elif type is self.FilterType.Highpass:
            self.b, self.a = butter(order, cutoffFrequencies,'highpass', analog=False)
        if type is self.FilterType.Lowpass:
            self.b, self.a = butter(order, cutoffFrequencies,'bandpass', analog=False)
        elif type is self.FilterType.Highpass:
            self.b, self.a = butter(order, cutoffFrequencies,'bandstop', analog=False)

    def __del__(self):
        super().__del__()

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             for row in data:
                raise NotImplementedError("TBD")