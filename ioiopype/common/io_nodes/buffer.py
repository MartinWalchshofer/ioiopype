from ...pattern.io_node import IONode
from ...pattern.o_stream import OStream
from ...pattern.i_stream import IStream
from ..utilities.overriding_buffer import OverridingBuffer
from ...pattern.stream_info import StreamInfo
import json

class Buffer(IONode):
    def __init__(self, numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples):
        super().__init__()
        self.add_i_stream(IStream(StreamInfo(0, 'in', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(0, 'out', StreamInfo.Datatype.Frame)))
        self.numberOfChannels = numberOfChannels
        self.bufferSizeInSamples = bufferOverlapInSamples
        self.bufferOverlapInSamples = bufferOverlapInSamples
        self.buffer = OverridingBuffer(bufferSizeInSamples, numberOfChannels)
        self.sampleCnt = 0
        self.threshold = bufferSizeInSamples - bufferOverlapInSamples
        if self.threshold < 0:
            raise ValueError("Overlap must be smaller than buffersize")

    def __del__(self):
        super().__del__()

    def __dict__(self):
        return {
            "name": self.__class__.__name__,
            "numberOfChannels": self.numberOfChannels,
            "bufferSizeInSamples": self.bufferSizeInSamples,
            "bufferOverlapInSamples": self.bufferOverlapInSamples,
        }
    
    def __str__(self):
        return json.dumps(self.__dict__())

    @classmethod
    def initialize(cls, data):
        ds = json.loads(data)
        ds.pop('name', None)
        return cls(**ds)

    def update(self):
        data = None
        if self.InputStreams[0].DataCount > 0:
            data = self.InputStreams[0].read()
        if data is not None:
             for row in data:
                self.buffer.setData(data)
                self.sampleCnt += 1
                if self.sampleCnt % self.threshold == 0 and self.sampleCnt > 0:
                    self.write(0, self.buffer.getFrame())      