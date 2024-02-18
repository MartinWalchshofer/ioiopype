#Copyright © 2024 Martin Walchshofer

from .input_stream import InputStream

class OutputStream:
    def __init__(self, id : int, name : str):
        self.__inputStream : InputStream = None
        self.Id : int = id
        self.Name  : str = name
        self.IsConnected = False
    
    def connect(self, inputStream : InputStream):
        if isinstance(inputStream, InputStream):
            self.__inputStream = inputStream
            self.IsConnected = True
            inputStream.IsConnected = True
        else:
            raise TypeError("'inputStream' must be type of 'InputStream'")
        
    def disconnect(self):
        if self.__inputStream is not None:
            self.IsConnected = True
            self.__inputStream .IsConnected = True
            self.__inputStream = None

    def write(self, data):
        if self.__inputStream is not None:
             self.__inputStream.write(data)