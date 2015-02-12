'''
Created on Jun 19, 2014

@author: jshor
'''

from cells.GridCells import GridNetwork
from cells.PlaceCells import PlaceNetwork
from os.path import join
from os import listdir

base = "data/simulations/density_estimation"

def _collect_one_round(params, get_relevant_activity):
    grid_net = GridNetwork(pm.grd_cells, pm.min_grid_size, pm.W,pm.H, pm.modules)
    plc_net = PlaceNetwork(pm.plc_cells, grid_net, wt_type=pm.wt_type, C=pm.C)
    acts = plc_net.activity()
    return get_relevant_activity(acts)

def collect_data(params, get_relevant_activity, cycles, subfolder):
    folder =join(base, subfolder)
    file_num = len(listdir(folder))

    results = []
    for rnd in range(cycles):
        logging.info('Round %i/%i',rnd+1,cycles)
        results.append(_collect_one_round(pm, get_relevant_activity))

    fn = join(folder, subfolder+str(file_num+rnd+1))
    with open(fn,'w') as f:
        cPickle.dump(results,f)