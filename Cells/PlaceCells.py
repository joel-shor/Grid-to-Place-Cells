'''
PlaceNetwork class takes a grid network, determines what connection
weights it wants, and calculates the activity of each place cell in the
network.
'''

import numpy as np
import time
import logging

class Weights:
    ''' Static methods to determine synatpic weights
        between grid cells and place cells. '''
    @staticmethod
    def Monaco(grd_num, plc_num, connectivity):
        ''' Creates a weight matrix based on the Monaco and Abbott paper. '''
        active = int(np.ceil(grd_num*connectivity))
        base = np.concatenate([np.random.rand(active),
                               np.zeros(grd_num-active)])
        mat_arr = [np.random.permutation(base) for _ in range(plc_num)]
        return np.array(mat_arr)
    @staticmethod
    def MonacoUpdated(grd_num, plc_num, connectivity):
        ''' Creates a weight matrix based on the Monaco and Abbott paper,
            then renormalizes so that the maximum grid cell output is
            actually achieved. '''
        wts = Weights.Monaco(grd_num, plc_num, connectivity)
        wts *= grd_num*connectivity/np.sum([wts.item(i) for i in range(grd_num)])
        return wts

class PlaceNetwork:
    '''
    Generates weights connecting grid cells to place cells and calculates
    the resulting place cell activity.
    '''
    def __init__(self, N, grid_net, wt_type=None, C=None):
        self.grid_net = grid_net
        self.type = type
        self.C=C
        if C is None:
            logging.warning('PlaceNetwork.C is None')
        if wt_type == 'Monaco':
            self.wts = Weights.Monaco(self.grid_net.N, N, C)
        elif wt_type == 'Monaco updated':
            self.wts = Weights.MonacoUpdated(self.grid_net.N, N, C)
        else:
            logging.warning('No weights generated.')
            self.wts = None
    
    def activity(self):
        ''' Each grid cell output lies within [-.5, 1]
            Each weight lies between 0 and 1
            Connectivity lies between 0 and 1
            To normalize the place cell output to between 0 
            and 1, we must have 
            (Weights)*(Grid Cells)*(2/3)*(# of Grd Cells*C) + (1/3)(# of Grid Cells*C)
            **This is where a majority of the time is spent**
        '''
        s = time.time()
        C = self.C if self.C is not None else 1
        fac = int(np.ceil(self.wts.shape[1]*C))
        grid_output = self.grid_net.activity()
        
        # **This line is where a majority of the program's time is spent
        tot_act = np.tensordot(self.wts, grid_output,
                               axes=[[1],[0]])*(2.0/3)/fac + (1.0/3)

        logging.info('Calculated network activity: \t%.4f',time.time()-s)

        if len(tot_act) == 1:
            tot_act = tot_act[0]
        return tot_act

    
if __name__ == '__main__':
    # Check speed of PlaceCells
    logging.basicConfig(level=logging.INFO)
    from time import time as tm
    from GridCells import GridNetwork
    N = 1000
    min_grid_size = 1
    W=H=10
    k = GridNetwork(N, min_grid_size,W,H)
    s = tm()
    for _ in range(10):
        j = PlaceNetwork(500,k,'Monaco updated',.4)
        j.activity()
    print 'Time for 1:%.3f'%(tm()-s,)
    