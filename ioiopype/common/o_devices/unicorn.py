from ...pattern.o_stream import OStream
from ...pattern.o_node import ONode
from ...pattern.stream_info import StreamInfo
from ...pattern.o_device import ODevice
from ...utilities.system import is_mobile, get_system, System
import serial as ps
import serial.tools.list_ports as p

class Unicorn(ODevice):
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
        elif not ismobile and system is System.Mac:
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

    def __init__(self, serial):
        super().__init__()
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
        
        CMD_START_ACQUISITION = b'\x61\x7C\x87'
        CMD_STOP_ACQUISITION = b'\x63\x5C\xC5'
        RES_OK = b'\x00\x00\x00'

        self.__serialPort.write(CMD_START_ACQUISITION)


        #TODO NOT FINISHED YET

    def __del__(self):
        if self.__serialPort.is_open:
            self.__serialPort.close()
        self.__serialPort = None