from matplotlib import pyplot as plt
from Cells.PlaceCells import PlaceNetwork
from Cells.GridCells import GridNetwork
from Cells.Inhibition import asymptotic_inhib
from Cells.PlaceFields import PlaceField
from Figures.graphFuncs import _plot
import logging

def example():
    ''' Create images of a situation where the size of the place cell matters. '''
    logging.basicConfig(level=logging.INFO)
    PlaceN = 500
    GridN = 1000
    C=.3
    thresh = .0075
    f_I = 5.31
    f_p = 15
    W = 1
    min_grid_size = .0004
    min_plcfld_size = .005

    
    grid_net = GridNetwork(GridN, min_grid_size, W,W, None)
    plc_net = PlaceNetwork(PlaceN, grid_net, wt_type='Monaco', C=C)
    acts = plc_net.activity()
    final_acts, _ = asymptotic_inhib(acts, f_I, f_p, thresh)
    
    mesh_pts = acts[0].shape[0]
    for i in range(PlaceN):
        logging.info('Starting cycle %i',i)
        flds = PlaceField.above_cutoff(final_acts[i], use_cutoff=False)
        num_flds, layout, _ = PlaceField.check_size(flds,W,W,min_plcfld_size,mesh_pts)
        no_min, _, _ = PlaceField.check_size(flds,W,W,0,mesh_pts)
        if no_min != num_flds:
            _plot(grid_net.X[0],grid_net.Y[0],flds,'Before size check')
            _plot(grid_net.X[0],grid_net.Y[0],layout,'After size check')
            plt.show()