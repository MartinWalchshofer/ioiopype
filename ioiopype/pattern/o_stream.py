#Copyright © 2024 Martin Walchshofer

from .i_stream import IStream

class OStream:
    def __init__(self, id : int, name : str):
        self.__inputStreams : list [IStream] = []
        self.Id : int = id
        self.Name  : str = name
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