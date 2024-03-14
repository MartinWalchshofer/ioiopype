from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
from ...utilities.system import is_mobile, get_system, System
import serial as ps
import serial.tools.list_ports as p
import threading
import time

class Unicorn(ODevice):
    NumberOfAcquiredChannels = 17
    SamplingRateInHz = 250
    NumberOfEEGChannels = 8
    NumberOfAccChannels = 3
    NumberOfGyrChannels = 3
    NumberOfCntChannels = 1
    NumberOfBatteryLevelChannels = 1
    NumberOfValidationIndicatorChannels = 1

    CmdStartAcquisition = b'\x61\x7C\x87'
    CmdStopAcquisition = b'\x63\x5C\xC5'
    ResOk = b'\x00\x00\x00'
    RawPayloadLengthBytes = 45
    HeaderStartSequence = b'\xC0\x00'
    FooterStopSequence = b'\x0D\x0A'
    
    EegScale = 4500000.0 / 50331642.0
    BatteryScale = 1.2 / 16.0
    BatteryOffset = 3.0
    BatteryPercentageFactor = 100.0 / 4.2
    BatteryBitMask = 0x0F
    AccelerometerScale = 1.0 / 4096.0
    GyroscopeScale = 1.0 / 32.8
    HeaderLength = 2
    HeaderOffset = 0
    BytesPerBatteryLevelChannel = 1
    BatteryLevelLength = NumberOfBatteryLevelChannels * BytesPerBatteryLevelChannel
    BatteryLevelOffset = HeaderLength
    BytesPerEegChannel = 3
    EegLength = NumberOfEEGChannels * BytesPerEegChannel
    EegOffset = HeaderLength + BatteryLevelLength
    BytesPerAccChannel = 2
    AccLength = NumberOfAccChannels * BytesPerAccChannel
    AccOffset = HeaderLength + BatteryLevelLength + EegLength
    BytesPerGyrChannel = 2
    GyrLength = NumberOfGyrChannels * BytesPerGyrChannel
    GyrOffset = HeaderLength + BatteryLevelLength + EegLength + AccLength
    BytesPerCntChannel = 4
    CntLength = NumberOfCntChannels * BytesPerCntChannel
    CntOffset = HeaderLength + BatteryLevelLength + EegLength + AccLength + GyrLength
    NumberOfFooterChannels = 1
    BytesPerFooterChannel = 2
    FooterLength = NumberOfFooterChannels * BytesPerFooterChannel
    FooterOffset = HeaderLength + BatteryLevelLength + EegLength + AccLength + GyrLength + CntLength
    
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
        self.__serialPort = ps.Serial()
        self.__serialPort.port = self.__device.Port
        self.__serialPort.open()
        if not self.__serialPort.is_open:
            raise ValueError("Could not open device")
        self.__connected = True

        self.__acquisitionRunning = False
        self._acquisitionThread = None
        self.__serialPort.write(Unicorn.CmdStartAcquisition)
        res = self.__serialPort.read(3)
        if res != Unicorn.ResOk:
            raise ValueError("Could not start acquisition")
        
        self.__payloadConverted = [None] * Unicorn.NumberOfAcquiredChannels
        self.__prevPayloadConverted = [None] * Unicorn.NumberOfAcquiredChannels
        self.__start_acquisition()

    def __start_acquisition(self):
        if not self.__acquisitionRunning:
            self.__acquisitionRunning = True
            self._acquisitionThread = threading.Thread(target=self.__acquisitionThread_DoWork, daemon=True)
            self._acquisitionThread.start()

    def __stop_acquisition(self):
        if self.__acquisitionRunning:
            self.__serialPort.write(Unicorn.CmdStopAcquisition)
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
            eegTemp = int((((payloadRaw[Unicorn.EegOffset + i * Unicorn.BytesPerEegChannel] & 0xFF) << 16) |
                ((payloadRaw[Unicorn.EegOffset + i * Unicorn.BytesPerEegChannel + 1] & 0xFF) << 8) |
                (payloadRaw[Unicorn.EegOffset + i * Unicorn.BytesPerEegChannel + 2] & 0xFF)))

            if (eegTemp & 0x00800000) == 0x00800000:
                eegTemp = (eegTemp | 0xFF000000)

            self.__payloadConverted[i]= eegTemp * Unicorn.EegScale
        
        for i in range (0, Unicorn.NumberOfAccChannels):
            accTemp = int(((payloadRaw[Unicorn.AccOffset + i * Unicorn.BytesPerAccChannel] & 0xFF) |
                    ((payloadRaw[Unicorn.AccOffset + i * Unicorn.BytesPerAccChannel + 1] & 0xFF) << 8)))

            self.__payloadConverted[i + Unicorn.NumberOfEEGChannels] = accTemp * Unicorn.AccelerometerScale

        for i in range(0, Unicorn.NumberOfGyrChannels):
            gyrTemp = int(((payloadRaw[Unicorn.GyrOffset + i * Unicorn.BytesPerGyrChannel] & 0xFF) |
                    ((payloadRaw[Unicorn.GyrOffset + i * Unicorn.BytesPerGyrChannel + 1] & 0xFF) << 8)))
            self.__payloadConverted[i + Unicorn.NumberOfEEGChannels + Unicorn.NumberOfAccChannels] = gyrTemp * Unicorn.GyroscopeScale;
        
        self.__payloadConverted[Unicorn.NumberOfEEGChannels + Unicorn.NumberOfAccChannels + Unicorn.NumberOfGyrChannels] = int(((payloadRaw[Unicorn.BatteryLevelOffset] & Unicorn.BatteryBitMask)) * Unicorn.BatteryScale + Unicorn.BatteryOffset) * Unicorn.BatteryPercentageFactor

        self.__payloadConverted[Unicorn.NumberOfEEGChannels + Unicorn.NumberOfAccChannels + Unicorn.NumberOfGyrChannels + Unicorn.NumberOfBatteryLevelChannels] = int(((payloadRaw[Unicorn.CntOffset] & 0xFF) | (payloadRaw[Unicorn.CntOffset + 1] & 0xFF) << 8 | (payloadRaw[Unicorn.CntOffset + 2] & 0xFF) << 16 | (payloadRaw[Unicorn.CntOffset + 3] & 0xFF) << 24))

    def __acquisitionThread_DoWork(self):
        while self.__acquisitionRunning:
            payloadRaw = self.__serialPort.read(Unicorn.RawPayloadLengthBytes)
            payloadValid = False
            try:
                headerIndex = payloadRaw.index(Unicorn.HeaderStartSequence)
                footerIndex = payloadRaw.index(Unicorn.FooterStopSequence)
                if footerIndex - headerIndex == Unicorn.RawPayloadLengthBytes - 2 and headerIndex == 0:
                    payloadValid = True
            except:
                payloadValid = False
            
            if payloadValid:
                self.__convert_raw_data_payload(payloadRaw)
                print(self.__payloadConverted)
                #CHECK FOR DATA LOSS
                #CONVERT TO NUMPY ARRAY
                #FORWARD TO PIPELINE
                self.__payloadConverted = self.__payloadConverted.copy()