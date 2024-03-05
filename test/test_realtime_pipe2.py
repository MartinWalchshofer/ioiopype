import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import ioiopype as ioio

ioioPype = ioio.IOIOPypeBuilder(SCRIPT_DIR + "/test_realtime_pipe2.json")

'''TODO NOT FINISHED YET'''