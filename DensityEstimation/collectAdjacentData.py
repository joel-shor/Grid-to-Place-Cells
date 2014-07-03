'''
Created on Jun 19, 2014

@author: jshor
'''

from Cells.GridCells import GridNetwork
from Cells.PlaceCells import PlaceNetwork
from Simulation.params import Param
import logging
import cPickle


def run():
    logging.basicConfig(level=logging.INFO)
    pm = Param # Makes warnings go away by making pm local
    pm.modules = 0
    #min_plcfld_size = .05
    pm.min_plcfld_size = .005
    #min_grid_size = .0001
    pm.min_grid_size = .0004 # m**2
    #min_grid_size = .01 # m**2
    
    pm.C = 0.33
    pm.thresh = 0.01
    pm.f_I = 7
    pm.f_p = 15
    
    pm.wt_type = 'Monaco'
    
    
    pm.plc_cells = 500
    pm.grd_cells = 1000
    
    pm.W = pm.H=pm.W = 1
    
    
    tot=400
    for big_rnd in range(1,50):
        results = []
        for rnd in range(tot):
            logging.info('Round %i/%i',rnd+1,tot)
            grid_net = GridNetwork(pm.grd_cells, pm.min_grid_size, pm.W,pm.H, pm.modules)
            plc_net = PlaceNetwork(pm.plc_cells, grid_net, wt_type=pm.wt_type, C=pm.C)
            acts = plc_net.activity()
            
            midx = int(acts.shape[1]/2)
            midy = int(acts.shape[2]/2)
            act_l = acts[0,midx-10:midx+10+1,midy-10:midy+10+1]
            results.append(act_l)
        
        with open('adjacent_data'+str(big_rnd),'w') as f:
            cPickle.dump(results,f)
    
    
    
    
#final_acts, inhibs = asymptotic_inhib(acts, pm.f_I, pm.f_p, pm.thresh)