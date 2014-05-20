import logging
from matplotlib import pyplot as plt
from Cells.GridCells import GridNetwork
from Figures.graphFuncs import _plot

def example():
    ''' Create images of grid cell activity for the paper. '''
    
    W = 4
    for min_grid_size in [.01,.007,.005,.003,.001,.0001]:
        grid_net = GridNetwork(1,min_grid_size,W,W)
        _plot(grid_net.X,grid_net.Y,grid_net.activity()[0],None)
        
        cell = grid_net.net[0]
        logging.info('len=%f, rot=%f, offx=%f, offy=%f',cell.length,cell.rot, 
                                                           cell.offsetx, cell.offsety)
    plt.show()