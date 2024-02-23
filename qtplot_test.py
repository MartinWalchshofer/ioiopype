#TODO DELETE THIS SCRIPT

import numpy as np
import pyqtgraph as pg
import numpy as np



# Generate some data
#xVals = np.linspace(0, 10, 100)
numberOfSamples = 100
x = np.linspace(1, numberOfSamples, numberOfSamples)
plotWidget = pg.plot(title="multichannel plot")

pdi1 = pg.PlotDataItem( np.zeros(1),np.zeros(1))
#pdi2 = pg.PlotDataItem( x,np.random.random(numberOfSamples))
plotWidget.addItem(pdi1)
#plotWidget.addItem(pdi2)
plotWidget.plotItem.curves[0].curve.xData = x
plotWidget.plotItem.curves[0].xChanged.emit()
plotWidget.plotItem.curves[0].curve.yData = np.random.random(numberOfSamples)
plotWidget.plotItem.curves[0].yChanged.emit()

                      
"""
timer = pg.QtCore.QTimer()
def update():
    y = np.random.random((numberOfSamples,10))
    for i in range(y.shape[1]):
        if i <= 1:
             plotWidget.plot(x, y[:,i], pen=(i,y.shape[1]), clear=True)
        else:
            plotWidget.plot(x, y[:,i], pen=(i,y.shape[1]))
timer.timeout.connect(update)
timer.start(0)
"""
print('Press ENTER to terminate the script')
input()
