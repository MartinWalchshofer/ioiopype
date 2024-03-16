from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
from ...utilities.system import is_mobile, get_system, System
import serial as ps
import serial.tools.list_ports as p
import threading
import time
import numpy as np

class Unicorn(ODevice):
    NumberOfAcquiredChannels = 17
    SamplingRateInHz = 250
    NumberOfEEGChannels = 8
    NumberOfAccChannels = 3
    NumberOfGyrChannels = 3
    NumberOfCntChannels = 1
    NumberOfBatChannels = 1
    NumberOfValidChannels = 1

    __CmdStartAcquisition = b'\x61\x7C\x87'
    __CmdStopAcquisition = b'\x63\x5C\xC5'
    __ResOk = b'\x00\x00\x00'
    __RawPayloadLengthBytes = 45
    __HeaderStartSequence = b'\xC0\x00'
    __FooterStopSequence = b'\x0D\x0A'
    
    __EegScale = 4500000.0 / 50331642.0
    __BatteryScale = 1.2 / 16.0
    __BatteryOffset = 3.0
    __BatteryPercentageFactor = 100.0 / 4.2
    __BatteryBitMask = 0x0F
    __AccelerometerScale = 1.0 / 4096.0
    __GyroscopeScale = 1.0 / 32.8
    __HeaderLength = 2
    __HeaderOffset = 0
    __BytesPerBatteryLevelChannel = 1
    __BatteryLevelLength = NumberOfBatChannels * __BytesPerBatteryLevelChannel
    __BatteryLevelOffset = __HeaderLength
    __BytesPerEegChannel = 3
    __EegLength = NumberOfEEGChannels * __BytesPerEegChannel
    __EegOffset = __HeaderLength + __BatteryLevelLength
    __BytesPerAccChannel = 2
    __AccLength = NumberOfAccChannels * __BytesPerAccChannel
    __AccOffset = __HeaderLength + __BatteryLevelLength + __EegLength
    __BytesPerGyrChannel = 2
    __GyrLength = NumberOfGyrChannels * __BytesPerGyrChannel
    __GyrOffset = __HeaderLength + __BatteryLevelLength + __EegLength + __AccLength
    __BytesPerCntChannel = 4
    __CntLength = NumberOfCntChannels * __BytesPerCntChannel
    __CntOffset = __HeaderLength + __BatteryLevelLength + __EegLength + __AccLength + __GyrLength
    __NumberOfFooterChannels = 1
    __BytesPerFooterChannel = 2
    __FooterLength = __NumberOfFooterChannels * __BytesPerFooterChannel
    __FooterOffset = __HeaderLength + __BatteryLevelLength + __EegLength + __AccLength + __GyrLength + __CntLength
    
    __EegOffsetConverted = 0
    __AccOffsetConverted = NumberOfEEGChannels
    __GyrOffsetConverted = NumberOfEEGChannels + NumberOfAccChannels
    __BatOffsetConverted = NumberOfEEGChannels + NumberOfAccChannels + NumberOfBatChannels
    __CntOffsetConverted = NumberOfEEGChannels + NumberOfAccChannels + NumberOfBatChannels + NumberOfBatChannels
    __ValidOffsetConverted = NumberOfEEGChannels + NumberOfAccChannels + NumberOfBatChannels + NumberOfBatChannels + NumberOfCntChannels

    __deviceDiscoveredEventHandler = None
    __discoveryThread = None
    __discoveryThreadRunning = False

    class Device:
        def __init__(self, serial, port):
            self.Serial = serial
            self.Port = port

    @staticmethod
    def __get_available_devices():
        unicornPrefix = 'UN-'
        devices = []
        system = get_system()
        ismobile = is_mobile()
        if not ismobile and system is System.Windows:
            import wmi
            wmic = wmi.WMI()
            btDevices = "SELECT * FROM Win32_PnPEntity WHERE ClassGuid='{e0cbf06c-cd8b-4647-bb8a-263b43f0f974}' AND Description='Bluetooth Device'"
            rfcommDevices = "SELECT * FROM Win32_PnPEntity WHERE ClassGuid='{4d36e978-e325-11ce-bfc1-08002be10318}'"
            btDeviceQuery = wmic.query(btDevices)
            rfcommDeviceQuery = wmic.query(rfcommDevices)
            for btDevice in btDeviceQuery:
                if unicornPrefix in btDevice.Name:
                    serial = btDevice.Name
                    hardwareId = btDevice.HardwareId[0].replace('BTHENUM\\Dev_', '')
                    for rfcommDevice in rfcommDeviceQuery:
                        if hardwareId in rfcommDevice.PNPDeviceID:
                            start = rfcommDevice.Name.index( '(' )
                            end = rfcommDevice.Name.index( ')' )
                            port = rfcommDevice.Name[start+1:end]
                            devices.append(Unicorn.Device(serial, port))
        elif not ismobile and (system is System.Mac or system is System.Linux):
            ports = p.comports()
            for port in ports:
                portName = port.name
                if unicornPrefix in portName:
                    start = portName.index(unicornPrefix)
                    serial = portName[start:]
                    serial =  serial[:7] + '.' + serial[7:]
                    serial =  serial[:10] + '.' + serial[10:]
                    portTemp = port.device
                    if 'cu.' in portTemp:
                        portTemp = portTemp.replace('cu.', 'tty.')
                    devices.append(Unicorn.Device(serial, portTemp))
        else:
            raise NotImplementedError()

        return devices
    
    @staticmethod
    def get_available_devices():
        devices = Unicorn.__get_available_devices()
        serials = []
        for device in devices:
            serials.append(device.Serial)
        return serials

    @staticmethod
    def __discoveryThread_DoWork():
        while Unicorn.__discoveryThreadRunning:
            serials = Unicorn.get_available_devices()
            if len(serials) > 0 and Unicorn.__deviceDiscoveredEventHandler is not None:
                Unicorn.__deviceDiscoveredEventHandler(serials)
            time.sleep(1)

    @staticmethod
    def start_scanning():
        if not Unicorn.__discoveryThreadRunning:
            Unicorn.__discoveryThreadRunning = True
            Unicorn.__discoveryThread = threading.Thread(target=Unicorn.__discoveryThread_DoWork, daemon=True)
            Unicorn.__discoveryThread.start()

    @staticmethod
    def stop_scanning():
        if Unicorn.__discoveryThreadRunning:
            Unicorn.__discoveryThreadRunning = False
            Unicorn.__discoveryThread .join()
            Unicorn.__discoveryThread  = None

    @staticmethod
    def add_devices_discovered_eventhandler(handler):
        Unicorn.__deviceDiscoveredEventHandler = handler

    @staticmethod
    def remove_devices_discovered_eventhandler():
        Unicorn.__deviceDiscoveredEventHandler = None

    def __init__(self, serial):
        super().__init__()
        self.add_o_stream(OStream(StreamInfo(0, 'EEG', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(1, 'ACC', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(2, 'GYR', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(3, 'CNT', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(4, 'BAT', StreamInfo.Datatype.Sample)))
        self.add_o_stream(OStream(StreamInfo(5, 'VALID', StreamInfo.Datatype.Sample)))

        self.__devices = Unicorn.__get_available_devices()
        self.__device = None
        for device in self.__devices:
            if serial in device.Serial:
                self.__device = device     
        if self.__device is None:
             raise ValueError("Could find device with the specified serial number '" + serial + "'.")
        self.__serialPort = ps.Serial()
        self.__serialPort.port = self.__device.Port
        self.__serialPort.open()
        if not self.__serialPort.is_open:
            raise ValueError("Could not open device")
        self.__connected = True

        self.__acquisitionRunning = False
        self._acquisitionThread = None
        self.__serialPort.write(Unicorn.__CmdStartAcquisition)
        res = self.__serialPort.read(3)
        if res != Unicorn.__ResOk:
            raise ValueError("Could not start acquisition")
        
        self.__payloadConverted = [0] * Unicorn.NumberOfAcquiredChannels
        self.__prevPayloadConverted = [0] * Unicorn.NumberOfAcquiredChannels
        self.__start_acquisition()

    def __start_acquisition(self):
        if not self.__acquisitionRunning:
            self.__acquisitionRunning = True
            self._acquisitionThread = threading.Thread(target=self.__acquisitionThread_DoWork, daemon=True)
            self._acquisitionThread.start()

    def __stop_acquisition(self):
        if self.__acquisitionRunning:
            self.__serialPort.write(Unicorn.__CmdStopAcquisition)
            self.__acquisitionRunning = False
            self._acquisitionThread .join()
            self._acquisitionThread  = None

    def __del__(self):
        self.__stop_acquisition()
        if self.__connected :
            self.__serialPort.close()
        self.__serialPort = None

    def __convert_raw_data_payload(self, payloadRaw):
        for i in range(0, Unicorn.NumberOfEEGChannels):
            eegTemp = int((((payloadRaw[Unicorn.__EegOffset + i * Unicorn.__BytesPerEegChannel] & 0xFF) << 16) |
                ((payloadRaw[Unicorn.__EegOffset + i * Unicorn.__BytesPerEegChannel + 1] & 0xFF) << 8) |
                (payloadRaw[Unicorn.__EegOffset + i * Unicorn.__BytesPerEegChannel + 2] & 0xFF)))

            if (eegTemp & 0x00800000) == 0x00800000:
                eegTemp = (eegTemp | 0xFF000000)

            self.__payloadConverted[i + Unicorn.__EegOffsetConverted]= eegTemp * Unicorn.__EegScale
        
        for i in range (0, Unicorn.NumberOfAccChannels):
            accTemp = int(((payloadRaw[Unicorn.__AccOffset + i * Unicorn.__BytesPerAccChannel] & 0xFF) |
                    ((payloadRaw[Unicorn.__AccOffset + i * Unicorn.__BytesPerAccChannel + 1] & 0xFF) << 8)))

            self.__payloadConverted[i + Unicorn.__AccOffsetConverted] = accTemp * Unicorn.__AccelerometerScale

        for i in range(0, Unicorn.NumberOfGyrChannels):
            gyrTemp = int(((payloadRaw[Unicorn.__GyrOffset + i * Unicorn.__BytesPerGyrChannel] & 0xFF) |
                    ((payloadRaw[Unicorn.__GyrOffset + i * Unicorn.__BytesPerGyrChannel + 1] & 0xFF) << 8)))
            self.__payloadConverted[i + Unicorn.__GyrOffsetConverted] = gyrTemp * Unicorn.__GyroscopeScale;
        
        self.__payloadConverted[Unicorn.__BatOffsetConverted] = int(((payloadRaw[Unicorn.__BatteryLevelOffset] & Unicorn.__BatteryBitMask)) * Unicorn.__BatteryScale + Unicorn.__BatteryOffset) * Unicorn.__BatteryPercentageFactor
        self.__payloadConverted[Unicorn.__CntOffsetConverted] = int(((payloadRaw[Unicorn.__CntOffset] & 0xFF) | (payloadRaw[Unicorn.__CntOffset + 1] & 0xFF) << 8 | (payloadRaw[Unicorn.__CntOffset + 2] & 0xFF) << 16 | (payloadRaw[Unicorn.__CntOffset + 3] & 0xFF) << 24))
        self.__payloadConverted[Unicorn.__ValidOffsetConverted] = 1

    def __send_data(self, payload):
        self.write(0, np.array([payload[Unicorn.__EegOffsetConverted:Unicorn.NumberOfEEGChannels]])) 
        self.write(1, np.array([payload[Unicorn.__AccOffsetConverted:Unicorn.NumberOfAccChannels]])) 
        self.write(2, np.array([payload[Unicorn.__GyrOffsetConverted:Unicorn.NumberOfGyrChannels]])) 
        self.write(3, np.array([payload[Unicorn.__BatOffsetConverted:Unicorn.NumberOfBatChannels]])) 
        self.write(4, np.array([payload[Unicorn.__CntOffsetConverted:Unicorn.NumberOfCntChannels]])) 
        self.write(5, np.array([payload[Unicorn.__ValidOffsetConverted:Unicorn.NumberOfValidChannels]])) 

    def __acquisitionThread_DoWork(self):
        while self.__acquisitionRunning:
            payloadRaw = self.__serialPort.read(Unicorn.__RawPayloadLengthBytes)
            payloadValid = False
            try:
                headerIndex = payloadRaw.index(Unicorn.__HeaderStartSequence)
                footerIndex = payloadRaw.index(Unicorn.__FooterStopSequence)
                if footerIndex - headerIndex == Unicorn.__RawPayloadLengthBytes - 2 and headerIndex == Unicorn.__HeaderOffset:
                    payloadValid = True
            except:
                payloadValid = False
            
            if payloadValid:
                self.__convert_raw_data_payload(payloadRaw)
                
                samplesLost = self.__payloadConverted[Unicorn.__CntOffsetConverted] - self.__prevPayloadConverted[Unicorn.__CntOffsetConverted] - 1
                if samplesLost > 0:
                    cntVal = self.__payloadConverted[Unicorn.__CntOffsetConverted]
                    for i in range(0, samplesLost):
                        self.__prevPayloadConverted[Unicorn.__CntOffsetConverted] = cntVal + i + 1
                        self.__prevPayloadConverted[Unicorn.__ValidOffsetConverted] = 0
                        self.__send_data(self.__prevPayloadConverted)
                self.__send_data(self.__payloadConverted)
                self.__prevPayloadConverted = self.__payloadConverted.copy()