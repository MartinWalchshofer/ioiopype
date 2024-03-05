#Copyright © 2024 Martin Walchshofer

from .i_stream import IStream
from .stream_info  import StreamInfo

class OStream:
    def __init__(self, streamInfo : StreamInfo):
        self.__inputStreams : list [IStream] = []
        self.StreamInfo = streamInfo
        self.IsConnected = False
    
    def connect(self, inputStream : IStream):
        if isinstance(inputStream, IStream):
            inputStream.IsConnected = True
            self.__inputStreams.append(inputStream)
            self.IsConnected = True
        else:
            raise TypeError("'inputStream' must be type of 'InputStream'")
        
    def disconnect(self, inputStream : IStream):
        if len(self.__inputStreams) > 0:
            inputStream.IsConnected = False
            self.__inputStreams.remove(inputStream)
            self.IsConnected = False
            self.__inputStream = None

    def write(self, data):
        if len(self.__inputStreams) > 0:
            for inputstream in self.__inputStreams:
                inputstream.write(data)