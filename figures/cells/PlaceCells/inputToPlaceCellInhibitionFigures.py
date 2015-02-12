from matplotlib import pyplot as plt
from cells.PlaceCells import PlaceNetwork
from cells.GridCells import GridNetwork
from figures.graphLib import _plot_sub
import logging

def display_with_modules():
    ''' Create images of typical place cell input. '''
    W = 3   # Size of room
    min_grid_size = .0004
    G = 100 # Number of grid cells
    P = 4 # Number of place cells
    Ms = [0, 1, 5]    # Number of modules
    C = .4  # Connectivity

    for j in range(len(Ms)):
        M = Ms[j]

        grid_net = GridNetwork(G,min_grid_size,W,W,modules=M)
        plc_net = PlaceNetwork(P,grid_net,wt_type='Monaco',C=C)

        logging.info('Calculating activity...')
        act = plc_net.activity()

        for i in range(1,5):
            plt.subplot(len(Ms),4,i+4*j)
            _plot_sub(grid_net.X[0],grid_net.Y[0],act[i-1],None)
    plt.suptitle('W=%i,G=%i,Ms=%s'%(W,G,str(Ms)))
    plt.show()