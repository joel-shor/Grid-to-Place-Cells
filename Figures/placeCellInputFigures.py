from matplotlib import pyplot as plt
from Cells.PlaceCells import PlaceNetwork
from Cells.GridCells import GridNetwork
from Figures.graphFuncs import _plot
import logging

def example():
    ''' Create images of place cell input for the paper. '''
    logging.basicConfig(level=logging.INFO)
    W = 3
    min_grid_size = .0001
    grid_net = GridNetwork(1000,min_grid_size,W,W,modules=5)
    plc_net = PlaceNetwork(500,grid_net,wt_type='Monaco updated',C=.4)

    act = plc_net.activity()

    for i in range(5):
        _plot(grid_net.X[0],grid_net.Y[0],act[i],None)
    plt.show()