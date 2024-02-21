from ..pattern.output_node import OutputNode
from ..pattern.output_stream import OutputStream
from ..pattern.input_node import InputNode
from ..pattern.input_stream import InputStream
from ..utilities.overriding_buffer import OverridingBuffer

class Buffer(InputNode, OutputNode):
    def __init__(self, numberOfChannels, bufferSizeInSamples, bufferOverlapInSamples):
        super().__init__()
        super(InputNode, self).__init__()
        self.add_input_stream(InputStream(0, 'sample'))
        self.add_output_stream(OutputStream(0,'frame'))
        self.buffer = OverridingBuffer(bufferOverlapInSamples, numberOfChannels)
        self.sampleCnt = 0
        self.threshold = bufferSizeInSamples - bufferOverlapInSamples
        if self.threshold < 0:
            raise ValueError("Overlap must be smaller than buffersize")

    def __del__(self):
        super().__del__()
        super(InputNode, self).__del__()

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