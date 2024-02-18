#Copyright © 2024 Martin Walchshofer

from ..pattern.input_stream import InputStream
from ..pattern.output_stream import OutputStream
from ..pattern.input_node import InputNode
from ..pattern.output_node import OutputNode
import threading
import time
import random

#todo change data and counter to numpy arrays
class DataGenerator(OutputNode):
    def __init__(self, sampling_rate, channel_count):
        super().__init__()
        self.add_stream(OutputStream(0,'data')) #todo extend type, range, etc.
        self.add_stream(OutputStream(1,'cnt'))

        self.sampling_rate = sampling_rate
        self.channel_count = channel_count
        self.__acquisitionRunning = False
        self.__acquisitionThread = None
        self.__cnt = 0

    def start(self):
        if not self.__acquisitionRunning:
            self.__acquisitionRunning = True
            self.__acquisitionThread = threading.Thread(target=self.__acquisitionThread_dowork)
            self.__acquisitionThread.start()
           
    def stop(self):
        if self.__acquisitionRunning:
            self.__acquisitionRunning = False
            self.__acquisitionThread.join(500)

    def __acquisitionThread_dowork(self):
        while self.__acquisitionRunning:
            time.sleep(1/self.sampling_rate)
            data = [0]*self.channel_count
            self.__cnt += 1
            for i in range(self.channel_count):
                data[i] = random.uniform(-10, 10)

            self.write(0, data)
            self.write(1, self.__cnt)