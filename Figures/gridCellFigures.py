import logging
from matplotlib import pyplot as plt
from Cells.GridCells import GridNetwork
from Figures.graphFuncs import _plot

def example():
    ''' Create images of grid cell activity for the paper. 
    
        Called as python MakeFig.py grid
    '''
    
    W = 4
    for min_grid_size in [.01,.007,.005,.003,.001,.0001]:
        grid_net = GridNetwork(1,min_grid_size,W,W)
        xx = grid_net.X[0]
        yy = grid_net.Y[0]
        act = grid_net.activity()[0]
        _plot(xx,yy,act,None)

    plt.show()