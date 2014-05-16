'''
Created on Jun 26, 2013

Creates the basic properties of the grid cell, which produces a sum
of sinusoids, and the grid network, which keeps track of a collection
of grid cells and sums their outputs when necessary.
'''

import numpy as np
from numpy.random import uniform
import logging

LEN_RANGE = [.28, .73]

class GridCell:
    '''
    This is a single Grid Cell. It generates activity at x and y locations.
    '''
    def __init__(self, length, rot, offsetx,offsety):
        ''' Length is the length between peaks. 
        Rot is the rotation from the origin. 
        Offset is a number between 0 and 1, representing where the peak lies
        with respect to the origin'''
        self.length=length
        self.rot=rot
        self.offsetx=offsetx
        self.offsety=offsety

    def _arg(self, X, Y, th):
        return (4*np.pi/(np.sqrt(3)*self.length)*
                    (np.cos(th-self.rot)*(X-self.offsetx*self.length) +
                     np.sin(th-self.rot)*(Y-self.offsety*self.length)))
    
    def activity(self, X, Y):
        ''' Activity is between -.5 and 1 (pf??) '''
        sm = sum([np.cos(self._arg(X,Y,th)) for th in [0, np.pi/3,-1*np.pi/3]])/3.0
        return sm
    

class GridNetwork:
    ''' A collection of grid cells. Simply keeps track of the cells
        and sums the activity when necessary. '''
    def __init__(self, N, min_grid_size,W,H, modules=None):
        ''' Time to generate network is negligible. '''
        
        self.X, self.Y = self._calc_grid(min_grid_size,W,H)

        if modules is None:
            grds = zip(uniform(*LEN_RANGE,size=N),
                       uniform(0,2.0*np.pi/3,N),
                       uniform(0,1,N),
                       uniform(0,1,N))
            self.net = np.array([GridCell(leng,rot,off_x,off_y) for (leng,rot,off_x,off_y) in grds])
        else:
            raise Exception('Modules not implemented.')

    def _calc_grid(self, min_grid_size, W, H):
        '''A convenient way to compute the spatial grid.'''
        size_len = np.sqrt(min_grid_size)
        mesh_pts = int(W/size_len)
        logging.info('Mesh points: %i', mesh_pts)
        
        x = np.linspace(-1.0*W/2, 1.0*W/2, mesh_pts)
        y = np.linspace(-1.0*H/2, 1.0*H/2, mesh_pts)
        return np.meshgrid(x, y)
    
    def activity(self):
        ''' Each grid cell output lies within [-.5, 1].'''
        return np.array([cell.activity(self.X,self.Y) for cell in self.net])


def generate_example_images():
    ''' Create images of grid cell activity for the paper. '''
    
    from graph_funcs import _plot
    from matplotlib import pyplot as plt
    
    W = 4
    for min_grid_size in [.01,.007,.005,.003,.001,.0001]:
        grid_net = GridNetwork(1,min_grid_size,W,W)
        _plot(grid_net.X,grid_net.Y,grid_net.activity()[0],None)
        
        cell = grid_net.net[0]
        logging.info('len=%f, rot=%f, offx=%f, offy=%f',cell.length,cell.rot, 
                                                           cell.offsetx, cell.offsety)
    plt.show()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    generate_example_images()
    