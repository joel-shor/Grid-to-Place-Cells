''' The function to run a single simulation. This also contains
some functions for plotting pretty pictures during the 
simulation, if necessary. '''

import time
import numpy as np
import logging

from Cells.GridCells import GridNetwork
from Cells.PlaceFields import PlaceField
from Cells.PlaceCells import PlaceNetwork
from Cells.Inhibition import asymptotic_inhib
#from InhibitionC import inhib

def run_simulation(params):
    ''' Completes a single run of the simulation for the given parameters.
        Returns the resulting map, units, and fields spatial statistics. '''
    
    s=time.time()
    pm = params
    maps = {'Sparsity':[],
            'Coverage':[],
            'Representation':[]}
    units = {'Number of fields':[],
             'Coverage':[]}
    fields = {'Area':[]}

    grid_net = GridNetwork(pm.grd_cells, pm.min_grid_size, pm.W,pm.H, pm.modules)
    plc_net = PlaceNetwork(pm.plc_cells, grid_net, wt_type=pm.wt_type, C=pm.C)
    acts = plc_net.activity()
    final_acts, inhibs = asymptotic_inhib(acts, pm.f_I, pm.f_p, pm.thresh)
    
    mesh_pts = acts[0].shape[0]
    plc_fld_dat = []
    for i in range(pm.plc_cells):
        flds = PlaceField.above_cutoff(final_acts[i])
        num_flds, layout, fld_areas = PlaceField.check_size(flds,pm.W,pm.H,
                                                            pm.min_plcfld_size,mesh_pts)
        fields['Area'].extend(fld_areas)
        units['Number of fields'].append(num_flds)
        units['Coverage'].append(1.0*np.sum(layout)/np.prod(layout.shape))
        plc_fld_dat.append((num_flds,layout))
    
    maps['Sparsity'].append(PlaceField.sparsity(plc_fld_dat))
    maps['Coverage'].append(PlaceField.coverage(plc_fld_dat))
    maps['Representation'].append(PlaceField.representation(plc_fld_dat))
    
    logging.info('Finished a simulation in time: %.3f', time.time()-s)
    return maps, units, fields


    