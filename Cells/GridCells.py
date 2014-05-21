'''
Created on Jun 26, 2013

Creates the basic properties of the grid cell, which produces a sum
of sinusoids, and the grid network, which keeps track of a collection
of grid cells and sums their outputs when necessary.
'''

import numpy as np
from numpy.random import uniform
import logging

# Try using the cache
from Cache.cache import try_cache, store_in_cache

from time import time as tm

len_range = [.3, .9]

class GridNetwork:
    '''
    A better grid network
    '''
    def __init__(self, N, min_grid_size,W,H, modules=None):
        
        self.X, self.Y = self._calc_grid(min_grid_size,W,H,N)
        
        
        self.cache_key = (N,min_grid_size,W,H,modules,len_range)
        self.cache=None
        
        #s = tm()
        #self.cache = try_cache(self.cache_key)

        if self.cache is not None: 
            logging.info('Skipping init for cache.')
            return
        
        self.N = N
        [_, xx, yy] = self.X.shape
        
        if modules is None:
            
            self.l = np.zeros([N,xx,yy])    # The grid length matrix
            self.rot = np.zeros([N,xx,yy])  # The rotation matrix
            self.xoff = np.zeros([N,xx,yy]) # x offset matrix
            self.yoff = np.zeros([N,xx,yy]) # y offset matrix
            
            for i in range(N): 
                cur_l = uniform(*len_range)
                self.l[i,:,:] = cur_l
                
                self.rot[i,:,:] = uniform(0,2.0*np.pi/3)
                
                cur_xoff = uniform(-cur_l, cur_l)
                self.xoff[i,:,:] = cur_xoff
                
                y_range = np.sqrt(cur_l**2-cur_xoff**2)
                self.yoff[i,:,:] = uniform(-y_range, y_range)
        else:
            raise Exception('Modules not implemented.')
    
    def activity(self):
        '''
        Eq:
        1/3 * cos[ 4*pi/(sqrt(3)*l) {cos(t-rot), sin(t-rot)} DOT (x-offset)  ] for t = -pi/3, 0, pi/3
        '''
        if self.cache is not None: 
            logging.info('Got grid cell activity from cache.')
            return self.cache
        
        out = np.zeros(self.l.shape)
        
        for tt in [-np.pi/3.0, 0.0, np.pi/3.0]:
            pt1 = 4*np.pi/(np.sqrt(3)*self.l)
            pt2 = np.cos(tt-self.rot)
            pt3 = np.sin(tt-self.rot)
            pt4 = self.X - self.xoff
            pt5 = self.Y - self.yoff

            #import pdb; pdb.set_trace()
            out += 1/3.0 * np.cos(pt1*(pt2*pt4+pt3*pt5))
        
        #store_in_cache(self.cache_key, out)
        
        return out
     
    def _calc_grid(self, min_grid_size, W, H, N):
        '''A convenient way to compute the spatial grid.'''
        
        size_len = np.sqrt(min_grid_size)
        mesh_pts = int(W/size_len)
        
        
        x = np.linspace(-1.0*W/2, 1.0*W/2, mesh_pts)
        y = np.linspace(-1.0*H/2, 1.0*H/2, mesh_pts)
        X_tmp,Y_tmp = np.meshgrid(x, y)

        X = np.zeros([N, mesh_pts,mesh_pts])
        Y = np.zeros([N, mesh_pts,mesh_pts])
        
        for i in range(N):
            X[i,:,:] = X_tmp
            Y[i,:,:] = Y_tmp
        
    
        return X, Y

if __name__ == '__main__':
    
    # Check speed of GridCells
    import logging
    logging.basicConfig(level=logging.INFO)
    from time import time as tm
    N = 1000
    min_grid_size = .0001
    W=H=1
    
    s = tm()
    for i in range(5):
        k = GridNetwork(N, min_grid_size,W,H)
        k.activity()
        logging.info('Done with %i',i)
    logging.info('Time for 1: %.3f',tm()-s)
    