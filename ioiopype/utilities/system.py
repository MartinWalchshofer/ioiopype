import platform
from enum import Enum

class System(Enum):
    Unknown = 1
    Windows = 2
    Linux = 3
    Mac = 4
    iOs = 5
    Android = 6

def get_system():
    sys = System.Unknown
    system = platform.system()
    if system == 'Darwin':
        sys = System.Mac
        try:
            with open('System/Library/CoreServices/SystemVersion.plist') as f:
                for line in f:
                    if '<key>ProductName</key>' in line:
                        if '<string>iOS' in next(f):
                            sys = System.iOs
        except:
            sys = System.Mac
    elif system == 'Linux':
        sys = System.Linux
        try:
            with open('/proc/version', 'r') as f:
                for line in f:
                    if 'Android' in line:
                        sys = System.Android
        except:
            sys = System.Linux
    elif system == 'Windows':
        sys = System.Windows

    return sys

def is_mobile():
    sys = get_system()
    if sys is System.iOs or sys is System.Android:
        return True
    else:
        return False
