#Copyright © 2024 Martin Walchshofer

from .input_stream import InputStream

class OutputStream:
    def __init__(self, id : int, name : str):
        self.__inputStreams : list [InputStream] = []
        self.Id : int = id
        self.Name  : str = name
        self.IsConnected = False
    
    def connect(self, inputStream : InputStream):
        if isinstance(inputStream, InputStream):
            inputStream.IsConnected = True
            self.__inputStreams.append(inputStream)
            self.IsConnected = True
        else:
            raise TypeError("'inputStream' must be type of 'InputStream'")
        
    def disconnect(self, inputStream : InputStream):
        if len(self.__inputStreams) > 0:
            inputStream.IsConnected = False
            self.__inputStreams.remove(inputStream)
            self.IsConnected = False
            self.__inputStream = None

    def write(self, data):
        if len(self.__inputStreams) > 0:
            for inputstream in self.__inputStreams:
                inputstream.write(data)