import sys
import numpy as np

from vispy import scene, app
from time import time

from vispy.io import read_png, load_data_file
import vispy.mpl_plot as plt
import graspr_client as gc

DATA_LENGTH = 120
X_DATA = range(0,DATA_LENGTH)

PROBE_IDX_1 = 14
PROBE_IDX_2 = 15
PROBE_IDX_3 = 16

canvas = scene.SceneCanvas(keys='interactive')
canvas.size = 600, 600
canvas.show()

# This is the top-level widget that will hold three ViewBoxes, which will
# be automatically resized whenever the grid is resized.
grid = canvas.central_widget.add_grid()


# Add 3 ViewBoxes to the grid
b1 = grid.add_view(row=0, col=0, col_span=2)
b1.border_color = (1, 0, 0, 1)
b1.camera.rect = (-10, -10), (DATA_LENGTH + 15, 65535)
b1.border = (1, 0, 0, 1)

b2 = grid.add_view(row=1, col=0, col_span=2)
b2.border_color = (0, 1, 0, 1)
b2.camera.rect = (-10, -10), (DATA_LENGTH + 15, 65535)
b2.border = (1, 0, 0, 1)

# Generate some random vertex data and a color gradient
N = DATA_LENGTH
pos = np.empty((N, 2), dtype=np.float32)
pos[:, 0] = np.linspace(0, DATA_LENGTH, N)
pos[:, 1] = np.random.normal(size=N, scale=100)
# pos[5000, 1] += 50

color = np.ones((N, 4), dtype=np.float32)
color[:, 0] = np.linspace(0, 1, N)
color[:, 1] = color[::-1, 0]

# Top grid cell shows plot data in a rectangular coordinate system.
l1 = scene.visuals.Line(pos=pos, color=color, antialias=False, mode='gl')
b1.add(l1)
grid1 = scene.visuals.GridLines(parent=b1.scene)

l2 = scene.visuals.Line(pos=pos, color=color, antialias=False, mode='gl')
b2.add(l2)
grid2 = scene.visuals.GridLines(parent=b2.scene)

def on_timer(event):
    global l1, l2, l3, canvas, PROBE_IDX_1, PROBE_IDX_2, PROBE_IDX_3
    data1 = gc.get_buffer(PROBE_IDX_1)
    data2 = gc.get_buffer(PROBE_IDX_2)
    data3 = gc.get_buffer(PROBE_IDX_3)
    pos = np.empty((N, 2), dtype=np.float32)
    # pos[:, 0] = np.linspace(0, 1000, N)
    pos[:, 0] = np.linspace(0, DATA_LENGTH, DATA_LENGTH)
    # pos[:, 1] = np.random.normal(size=N, scale=100)
    pos[:, 1] = data1
    # pos[5000, 1] += 50
    l1.set_data(pos=pos)

    pos2 = np.empty((N, 2), dtype=np.float32)
    pos2[:, 0] = np.linspace(0, DATA_LENGTH, DATA_LENGTH)
    pos2[:, 1] = data2
    l2.set_data(pos=pos2)
    canvas.measure_fps(window=1, callback='%1.1f FPS')

timer = app.Timer(0, connect=on_timer, start=True)

gc.setup_socket()

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()