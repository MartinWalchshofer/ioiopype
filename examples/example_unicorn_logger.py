'''This example shows how to connect to a 'Unicorn - The Brain Interface' device, calculate and visualize a pwelch spectrum '''

import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

import ioiopype as ioio

use_device_simulator = True #Use device simulator (True) or real device (False)
if use_device_simulator:
    device = ioio.UnicornSimulator('UN-0000.00.00')
else:
    device = ioio.Unicorn('UN-2023.02.15') #Enter your device serial here

csv = ioio.CSVLogger(len(device.OutputStreams))
csv.open(dir + '/test.csv', header='EEG1,EEG2,EEG3,EEG4,EEG5,EEG6,EEG7,EEG8,ACCX,ACCY,ACCZ,GYRX,GYRY,GYRZ,CNT,BAT,VALID')
for i in range(0, len(device.OutputStreams)):
    device.connect(i, csv.InputStreams[i])

input('Press ENTER to terminate the application\n')

csv.close()
for i in range(0, len(device.OutputStreams)):
    device.disconnect(i, csv.InputStreams[i])

del device