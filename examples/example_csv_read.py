import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from PySide6.QtWidgets import QApplication
import ioiopype as ioio

app = QApplication(sys.argv)

#replay file with 250Hz and loop
cr = ioio.CSVReader(250, True)
sp1 = ioio.SamplePlot(17, 250, 10, 100, displayMode=ioio.SamplePlot.DisplayMode.Overriding)

#connect file output to plot
cr.connect(0, sp1.InputStreams[0])

#open file
cr.open(dir + '/test.csv')

app.exec()

#close file
cr.close()

#disconnect
cr.disconnect(0, sp1.InputStreams[0])

#delete csv readed
del cr