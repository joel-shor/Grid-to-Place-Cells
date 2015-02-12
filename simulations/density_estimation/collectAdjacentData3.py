'''
Created on Jun 19, 2014

@author: jshor
'''

from simulations.params import Param
import logging
import numpy as np


def run():
    logging.basicConfig(level=logging.INFO)
    pm = Param # Makes warnings go away by making pm local
    pm.modules = 0
    pm.min_plcfld_size = .005
    pm.min_grid_size = .0004 # m**2
    pm.C = 0.33
    pm.thresh = 0.01
    pm.f_I = 7
    pm.f_p = 15
    pm.wt_type = 'Monaco'
    pm.plc_cells = 500
    pm.grd_cells = 1000
    pm.W = pm.H = pm.W = 1

    def get_relevant_activity(act):
        act_l = np.array( [acts[0,i,i] for i in range(50)])
        return act_l

    for _ in range(2):
        collect_data(pm, get_relevant_activity, cycles=1000,
                     subfolder="Adjacent3")


#final_acts, inhibs = asymptotic_inhib(acts, pm.f_I, pm.f_p, pm.thresh)