from matplotlib import pyplot as plt
from Cells.PlaceCells import PlaceNetwork
from Cells.GridCells import GridNetwork
from Cells.Inhibition import asymptotic_inhib
from Figures.graphFuncs import _plot
import logging

def example():
    ''' Create images of place cell input for the paper. '''
    logging.basicConfig(level=logging.INFO)
    thresh = 1
    f_I = 0.04/thresh
    f_p = thresh/0.005
    W = 1
    min_grid_size = .0001
    grid_net = GridNetwork(1000,min_grid_size,W,W)
    plc_net = PlaceNetwork(500,grid_net,wt_type='Monaco updated',C=.4)
    act = plc_net.activity()
    final_acts, _ = asymptotic_inhib(act,f_I,f_p,thresh)

    for i in range(15):
        _plot(grid_net.X[0],grid_net.Y[0],final_acts[i],None)
    plt.show()