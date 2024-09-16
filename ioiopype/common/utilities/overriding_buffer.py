import numpy as np
from enum import Enum

class OverridingBuffer:
    class OutputMode(Enum):
        Aligned = 1
        NotAligned = 2

    __frame = None
    __cnt = 0
    def __init__(self, samples_count, channel_count, outputMode = OutputMode.Aligned):
        self.__frame = np.zeros((int(samples_count), int(channel_count)))
        self.outputMode = outputMode
        self.__cnt = 0

    def setData(self, data):
        if isinstance(data, list):
            data = np.array([data])

        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                data = data[np.newaxis,:]
            if data.ndim != 2:
                raise ValueError("Dimensions do not match.")
            if data.shape[1] is not self.__frame.shape[1]:
                raise ValueError("Number of channels do not match.")
            
            #fill buffer with initial value
            if  self.__cnt == 0:
                self.__frame[:] = data[0]

            samplesCnt = data.shape[0]
            if self.__cnt + samplesCnt < self.__frame.shape[0]:
                self.__frame[self.__cnt : self.__cnt + samplesCnt, :] = data
            else:
                self.__frame[self.__cnt:] = data[0:self.__frame.shape[0]-self.__cnt,:]
                self.__frame[0:samplesCnt-(self.__frame.shape[0]-self.__cnt),:] = data[self.__frame.shape[0]-self.__cnt:]
            self.__cnt = (self.__cnt + samplesCnt) % self.__frame.shape[0]
        else:
            raise TypeError("Type not supported.")
        
    def getFrame(self):
        if self.outputMode is self.OutputMode.Aligned:
            return np.concatenate((self.__frame[self.__cnt :], self.__frame[:self.__cnt ]), axis=0)
        else:
            return self.__frame