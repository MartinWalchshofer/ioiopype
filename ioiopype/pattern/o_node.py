from .o_stream import OStream
from .i_stream import IStream
class ONode:
    def __init__(self):
        self.OutputStreams : list[OStream] = []
        self.__writeCnt = 0
        
    def __del__(self):
        for outputstream in self.OutputStreams:
            if(outputstream.IsConnected):
                outputstream.disconnect()

    def add_o_stream(self, outputStream : OStream):
        #TODO CHECK IF ID IS UNIQE
        if isinstance(outputStream, OStream):
            self.OutputStreams.append(outputStream)
        else:
            raise TypeError("'outputStream' must be type of 'OutputStream'")
        
    def connect(self, id : int, inputStream : IStream):
        if id < len(self.OutputStreams):
            if self.OutputStreams[id].StreamInfo.Datatype is not inputStream.StreamInfo.Datatype:
                raise ValueError("Data types do not match")
            self.OutputStreams[id].connect(inputStream)
        else:
            raise IndexError("Index out of range")
        
    def disconnect(self, id : int, inputStream : IStream):
        if id < len(self.OutputStreams):
            self.OutputStreams[id].disconnect(inputStream)
        else:
            raise IndexError("Index out of range")

    def write(self, id : int, data):
        if id < len(self.OutputStreams):
            self.__writeCnt += 1
            self.OutputStreams[id].write(data)
        else:
            raise IndexError("Index out of range")
