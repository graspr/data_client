#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Update a simple plot as rapidly as possible to measure speed.
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import graspr_client as gc

BUFFER = np.zeros(120, 'f')
BUFFER_STEP = 1

BUFFER_TWO = np.zeros(120, 'f')

app = QtGui.QApplication([])

def changeTitle():
    print 'HELLO!'

cb = QtGui.QCheckBox('Show title', self)
cb.move(20, 20)
cb.toggle()
cb.stateChanged.connect(changeTitle)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p = win.addPlot(title="Graspr Probe1 Value") # Create a new window showing the data, returns PlotWindow (which has a PlotWidget inside)
# p.setWindowTitle('Graspr Probe Value')
p.setRange(QtCore.QRectF(0, 0, 120, 65536)) 
p.setLabel('bottom', 'Index', units='B')

p_two = win.addPlot(title='Graspr Probe2 Value')
# p_two.setWindowTitle('Graspr Probe2 Value')
p_two.setRange(QtCore.QRectF(0, 0, 120, 40)) 
p_two.setLabel('bottom', 'Index', units='B')
p_two.setTitle('Probe 2')

curve = p.plot()
curve_2 = p_two.plot()

curve.setPen('r', width=2, cosmetic=True)
curve_2.setPen('g')

# curve.setFillBrush((0, 0, 100, 100))
# curve.setFillLevel(0)
# lr = pg.LinearRegionItem([100, 4900])
# p.addItem(lr)

ptr = 0
lastTime = time()
fps = None
def update():
    global curve, ptr, p, lastTime, fps, BUFFER, BUFFER_TWO
    raw_data = gc.read()
    val = raw_data[0]
    val_2 = np.random.randint(0,40)
    BUFFER = np.roll(BUFFER, BUFFER_STEP)
    BUFFER_TWO = np.roll(BUFFER_TWO, BUFFER_STEP)
    BUFFER[0] = val
    BUFFER_TWO[0] = val_2
    curve.setData(BUFFER)
    curve_2.setData(BUFFER_TWO)

    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    p.setTitle('Probe 1 :: %0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
    


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    gc.setup_socket()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
