from matplotlib import pyplot as plt
from Cells.PlaceCells import PlaceNetwork
from Cells.GridCells import GridNetwork
from Figures.graphFuncs import _plot_sub
import logging

def example():
    ''' Create images of typical place cell input. '''
    logging.basicConfig(level=logging.INFO)
    W = 3
    min_grid_size = .0004
    G = 100
    Ms = [0,1,5]
    
    for j in range(len(Ms)):
        M = Ms[j]
    
        grid_net = GridNetwork(G,min_grid_size,W,W,modules=M)
        plc_net = PlaceNetwork(4,grid_net,wt_type='Monaco',C=.4)
    
        logging.info('Calculating activity...')
        act = plc_net.activity()
    
        for i in range(1,5):
            plt.subplot(len(Ms),4,i+4*j)
            _plot_sub(grid_net.X[0],grid_net.Y[0],act[i-1],None)
    plt.suptitle('W=%i,G=%i,Ms=%s'%(W,G,str(Ms)))
    plt.show()