''' The function to run a single simulation. This also contains
some functions for plotting pretty pictures during the 
simulation, if necessary. '''

import time
import numpy as np
import logging

from Cells.GridCells import GridNetwork
from Cells.PlaceFields import PlaceField
from Cells.PlaceCells import PlaceCellNetwork
from Inhibition import calc_inhib
#from InhibitionC import calc_inhib

def run_simulation(params):
    ''' Completes a single run of the simulation for the given parameters.
        Returns the resulting map, units, and fields spatial statistics. '''
    s=time.time()
    p = params
    maps = {'Sparsity':[],
            'Coverage':[],
            'Representation':[]}
    units = {'Number of fields':[],
             'Coverage':[]}
    fields = {'Area':[]}

    grid_net = GridNetwork(p.grd_cells,p.min_grid_size,p.W,p.H,p.modules)
    plc_net = PlaceCellNetwork(p.plc_cells,grid_net,wt_type='Monaco',C=p.C)
    acts = plc_net.activity()
    final_acts, inhibs = _calculate_asymptotic_activity(acts,p.f_I,p.f_p,p.thresh)
    
    # Plot the post inhibition activities
    '''
    plot_final_acts(grid_net.X, grid_net.Y,final_acts)
    return None, None, None'''
    
    mesh_pts = acts[0].shape[0]
    plc_fld_dat = []
    for i in range(p.plc_cells):
        flds = PlaceField.above_cutoff(final_acts[i])
        num_flds, layout, fld_areas = PlaceField.check_size(flds,p.W,p.H,
                                                            p.min_plcfld_size,mesh_pts)
        #Finds pictures where size check matters
        '''
        test, _, _ = PlaceField.check_size(flds,p.W,p.H,0,mesh_pts)
        if test != num_flds:
            _plot_size_check_matters(grid_net.X,grid_net.Y, flds,layout)'''
        
        fields['Area'].extend(fld_areas)
        units['Number of fields'].append(num_flds)
        units['Coverage'].append(1.0*np.sum(layout)/np.prod(layout.shape))
        plc_fld_dat.append((num_flds,layout))
    
    maps['Sparsity'].append(PlaceField.sparsity(plc_fld_dat))
    maps['Coverage'].append(PlaceField.coverage(plc_fld_dat))
    maps['Representation'].append(PlaceField.representation(plc_fld_dat))
    
    logging.info('Finished a simulation in time: %.3f', time.time()-s)
    return maps, units, fields

def _calculate_asymptotic_activity(acts, f_I, f_p, thresh):
    ''' Runs the fast asymptotic activity algorithm for each
        spatial point in acts. '''
    s = time.time()
    mesh_pts = acts[0].shape[0]
    final_acts = [np.zeros([mesh_pts,mesh_pts]) for _ in range(len(acts))]
    inhibs = np.zeros([mesh_pts,mesh_pts])
    for i in range(mesh_pts):
        for j in range(mesh_pts):
            yf, inhib = calc_inhib([act[i,j] for act in acts], 
                                   f_I, f_p, thresh)
            for k in range(len(acts)):
                final_acts[k][i,j] = yf[k]
            inhibs[i,j] = inhib
    logging.info('Time to calculate asymptotic: %.3f', time.time()-s)
    return final_acts, inhibs

def _plot_final_acts(X,Y,final_acts):
    '''Plots figures of activity after global inhibition'''
    from GenerateFigures.simulation_graph_funcs import _plot
    from matplotlib import pyplot as plt
    for i in range(5):
        _plot(X,Y,final_acts[i],'Activity after inhibition')
    plt.show()

def _plot_size_check_matters(X,Y,flds,layout):
    '''Plots figures where size check matters.'''
    from GenerateFigures.simulation_graph_funcs import _plot
    from matplotlib import pyplot as plt
    _plot(X,Y,flds,None)
    _plot(X,Y,layout,None)
    plt.show()
    