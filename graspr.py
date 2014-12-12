# -*- coding: utf-8 -*-
"""
Draws Graspr Output
"""
from pyqtgraph.flowchart import Flowchart
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import pyqtgraph.metaarray as metaarray
import graspr_client as gc
from pyqtgraph.ptime import time
# QtGui.QApplication.setGraphicsSystem('opengl')
app = QtGui.QApplication([])


######################################
## INIT
## Create main window with grid layout
win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: Flowchart')
cw = QtGui.QWidget()
win.setCentralWidget(cw)
layout = QtGui.QGridLayout()
cw.setLayout(layout)
controlsWidget = QtGui.QWidget()
controlsLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
controlsWidget.setLayout(controlsLayout)
layout.addWidget(controlsWidget, 1,0)
######################################


####################################
#CONSTANTS
spins = [
    ("Red - Probe 14", None),
    ("Green - Probe 15", None),
    ("Blue - Probe 16", None),
    ("Finger", pg.SpinBox(value=5.0, bounds=[0, 5], step=1, minStep=1))
]

labels = []
FPSLabel = QtGui.QLabel("FPS:");
DATA_LENGTH = 120
X_DATA = range(0,DATA_LENGTH)
X_DATA = metaarray.MetaArray(X_DATA, info=[{'name': 'Time', 'values': np.linspace(0, 1.0, len(X_DATA))}, {}])
PROBE_IDX_1 = 14
PROBE_IDX_2 = 15
PROBE_IDX_3 = 16
####################################


## Create flowchart, define input/output terminals
fc = Flowchart(terminals={
    'output1': {'io': 'in'},
    'output2': {'io': 'in'},
    'output3': {'io': 'in'},
    'x': {'io': 'in'},       
    'dataOut': {'io': 'out'}    
})
w = fc.widget()

## Add flowchart control panel to the main window
# layout.addWidget(fc.widget(), 0, 0, 1, 1)

## Add two plot widgets
pw1 = pg.PlotWidget()
pw2 = pg.PlotWidget()



layout.addWidget(pw1, 0, 1)
layout.addWidget(pw2, 1, 1)

## Add Options
label = QtGui.QLabel(spins[0][0])
labels.append(label)
label = QtGui.QLabel(spins[1][0])
labels.append(label)
label = QtGui.QLabel(spins[2][0])
labels.append(label)
text = spins[3][0]
spin = spins[3][1]
label = QtGui.QLabel(text)
labels.append(label)

controlsLayout.addWidget(label)
controlsLayout.addWidget(spin)

controlsLayout.addWidget(FPSLabel)

#Set Input
fc.setInput(x=X_DATA)

########################################
#Set up flowchart nodes
pw1Node = fc.createNode('PlotWidget', pos=(150, 150))
pw1Node.setPlot(pw1)
pw2Node = fc.createNode('PlotWidget', pos=(300, -150))
pw2Node.setPlot(pw2)

curveNode1 = fc.createNode('PlotCurve', pos=(0, 0))
curveNode2 = fc.createNode('PlotCurve', pos=(0, 150))
curveNode3 = fc.createNode('PlotCurve', pos=(0, 300))
curveNode4 = fc.createNode('PlotCurve', pos=(-450, 0))
curveNode5 = fc.createNode('PlotCurve', pos=(-300, 150))
curveNode6 = fc.createNode('PlotCurve', pos=(-150, 300))
curveNode1.ctrls['color'].setColor((255,0,0))
curveNode2.ctrls['color'].setColor((0,255,0))
curveNode3.ctrls['color'].setColor((0,0,255))
curveNode4.ctrls['color'].setColor((255,0,0))
curveNode5.ctrls['color'].setColor((0,255,0))
curveNode6.ctrls['color'].setColor((0,0,255))

gauss1 = fc.createNode('GaussianFilter', pos=(150, -450))
gauss2 = fc.createNode('GaussianFilter', pos=(150, -300))
gauss3 = fc.createNode('GaussianFilter', pos=(150, -150))
gauss1.ctrls['sigma'].setValue(5)
gauss2.ctrls['sigma'].setValue(5)
gauss3.ctrls['sigma'].setValue(5)

fc.connectTerminals(fc['x'], curveNode1['x'])
fc.connectTerminals(fc['x'], curveNode2['x'])
fc.connectTerminals(fc['x'], curveNode3['x'])
fc.connectTerminals(fc['output1'], curveNode1['y'])
fc.connectTerminals(fc['output2'], curveNode2['y'])
fc.connectTerminals(fc['output3'], curveNode3['y'])
fc.connectTerminals(curveNode1['plot'], pw1Node['In'])
fc.connectTerminals(curveNode2['plot'], pw1Node['In'])
fc.connectTerminals(curveNode3['plot'], pw1Node['In'])

fc.connectTerminals(fc['output1'], gauss1['In'])
fc.connectTerminals(fc['output2'], gauss2['In'])
fc.connectTerminals(fc['output3'], gauss3['In'])
fc.connectTerminals(fc['x'], curveNode4['x'])
fc.connectTerminals(fc['x'], curveNode5['x'])
fc.connectTerminals(fc['x'], curveNode6['x'])
fc.connectTerminals(gauss1['Out'], curveNode4['y'])
fc.connectTerminals(gauss2['Out'], curveNode5['y'])
fc.connectTerminals(gauss3['Out'], curveNode6['y'])
fc.connectTerminals(curveNode4['plot'], pw2Node['In'])
fc.connectTerminals(curveNode5['plot'], pw2Node['In'])
fc.connectTerminals(curveNode6['plot'], pw2Node['In'])
###############################

win.show()


def fingerChanged(changed):
    global PROBE_IDX_1, PROBE_IDX_2, PROBE_IDX_3
    val = int(changed.value() * 3) #3 probes per finger
    PROBE_IDX_1 = val - 1
    PROBE_IDX_2 = val
    PROBE_IDX_3 = val + 1
    print 'FINGER CHAAANGED, now using probes: %s, %s, %s' % (PROBE_IDX_1, PROBE_IDX_2, PROBE_IDX_3)


spin.sigValueChanging.connect(fingerChanged)


lastTime = time()
fps = None
def _fps():
    global lastTime, fps, FPSLabel
    now = time()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    FPSLabel.setText('%0.2f FPS' % fps)

def update():
    global data, fc, PROBE_IDX_1, PROBE_IDX_2, PROBE_IDX_3
    ## generate signal data to pass through the flowchart
    data1 = gc.get_buffer(PROBE_IDX_1)
    data2 = gc.get_buffer(PROBE_IDX_2)
    data3 = gc.get_buffer(PROBE_IDX_3)
    # data += np.sin(np.linspace(0, 100, 1000))
    data1 = metaarray.MetaArray(data1, info=[{'name': 'Time', 'values': np.linspace(0, 1.0, len(data1))}, {}])
    data2 = metaarray.MetaArray(data2, info=[{'name': 'Time', 'values': np.linspace(0, 1.0, len(data2))}, {}])
    data3 = metaarray.MetaArray(data3, info=[{'name': 'Time', 'values': np.linspace(0, 1.0, len(data3))}, {}])
    ## Feed data into the input terminal of the flowchart
    fc.setInput(output1=data1)
    fc.setInput(output2=data2)
    fc.setInput(output3=data3)
    _fps()
    

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    gc.setup_socket()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
