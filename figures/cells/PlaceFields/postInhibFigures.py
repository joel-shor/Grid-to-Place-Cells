from matplotlib import pyplot as plt
from cells.PlaceCells import PlaceNetwork
from cells.GridCells import GridNetwork
from cells.Inhibition import asymptotic_inhib
from figures.graphLib import _plot

def example():
    ''' Create images of place cell output for the paper.

        Called as python MakeFig.py inhib'''
    thresh = .1
    f_I = 7
    f_p = 15
    W = 1
    C=.33

    min_grid_size = .0004
    grid_net = GridNetwork(1000,min_grid_size,W,W)
    plc_net = PlaceNetwork(500,grid_net,wt_type='Monaco updated',C=C)
    act = plc_net.activity()
    final_acts, _ = asymptotic_inhib(act,f_I,f_p,thresh)

    for i in range(5):
        _plot(grid_net.X[0],grid_net.Y[0],final_acts[i],None)
    plt.show()