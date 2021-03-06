'''
Created on Jun 19, 2014

@author: jshor
'''

from simulations.density_estimation.collectDensityLib import collect_data
from simulation.params import Param
import logging

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
        midx = int(acts.shape[1]/2)
        midy = int(acts.shape[2]/2)
        act_l = acts[0,midx-10:midx+10+1,midy-10:midy+10+1]
        return act_l

    for _ in range(2):
        collect_data(pm, get_relevant_activity, cycles=1000,
                     subfolder="Adjacent")