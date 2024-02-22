#TODO DELETE THIS SCRIPT

import numpy as np
import pyqtgraph as pg

# Generate some data
xVals = np.linspace(0, 10, 100)
yVals = np.sin(xVals)
yVals2 = np.sin(xVals*2)

pw = pg.plot(xVals, yVals, pen='r')  # plot x vs y in red
pw.plot(yVals, yVals2, pen='b')

print('Press ENTER to terminate the script')
input()
