import time
import threading
from abc import ABC, abstractmethod

class RealtimeClock(ABC):
    def __init__(self, frequencyHz):
        self.__realtimeClockRunning = False
        self.__realtimeClockThread = None
        self.__targetDt = 1000/frequencyHz
        self.__timestampStart = None
        self.__timestamp = 0
        self.__samplesSent = 0

    def __del__(self):
        self.stop()

    def start(self):
        if not self.__realtimeClockRunning:
            self.__realtimeClockRunning = True
            self.__realtimeClockThread = threading.Thread(target=self.__updateThread_DoWork, daemon=True)
            self.__realtimeClockThread.start()
           
    def stop(self):
        if self.__realtimeClockRunning:
            self.__realtimeClockRunning = False
            self.__realtimeClockThread.join(500)

    def __updateThread_DoWork(self):
        if self.__timestampStart is None:
            self.__timestampStart = time.time()*1000
        while self.__realtimeClockRunning:
            self.__timestamp = time.time()*1000 - self.__timestampStart

            if self.__samplesSent >= round(self.__timestamp / self.__targetDt):
                time.sleep(self.__targetDt /1000)
            else:
                samplesToSend = round(self.__timestamp / self.__targetDt) - self.__samplesSent
                for i in range(0, samplesToSend):
                    self.update()
                    self.__samplesSent += 1

    @abstractmethod
    def update(self):
        pass