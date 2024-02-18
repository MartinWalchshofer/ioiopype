#Copyright © 2024 Martin Walchshofer

from .output_stream import OutputStream
from .input_stream import InputStream
class OutputNode:
    def __init__(self):
        self.OutputStreams : list[OutputStream] = []

    def add_stream(self, outputStream : OutputStream):
        #TODO CHECK IF ID IS UNIQE
        if isinstance(outputStream, OutputStream):
            self.OutputStreams.append(outputStream)
        else:
            raise TypeError("'outputStream' must be type of 'OutputStream'")
        
    def connect(self, id : int, inputStream : InputStream):
        if id < len(self.OutputStreams):
            self.OutputStreams[id].connect(inputStream)
        else:
            raise IndexError("Index out of range")

    def write(self, id : int, data):
        if id < len(self.OutputStreams):
            self.OutputStreams[id].write(data)
        else:
            raise IndexError("Index out of range")
