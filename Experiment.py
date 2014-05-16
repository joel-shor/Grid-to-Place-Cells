''' The driver module for the experiments. Contains
    functions for parameter initialization and shell
    function for running repeated trials. '''

import time
import cPickle
import logging

from simulation import run_simulation


class Param:
    '''A class that conveniently holds the parameters.'''
    modules = None
    #min_plcfld_size = .05
    min_plcfld_size = .005
    #min_grid_size = .0001
    min_grid_size = .0004 # m**2
    #min_grid_size = .01 # m**2
    C = 0.4
    thresh = 1
    f_I = 0.04/thresh
    f_p = thresh/0.005
    cell_factor = 2
    plc_cells = 100
    grd_cells = 500

def combine(main, new):
    ''' Adds fields in dictionary 'new' to dictionary 'main'. '''
    if new is None: return
    for key in main.keys():
        main[key].extend(new[key])
        
def run_experiment(trials):
    ''' The shell function to cycle through repeated trials.'''
    
    s = time.time()
    # Data structure that will contain the data and will be pickled
    # to a file.
    maps = {'Sparsity':[],
            'Coverage':[],
            'Representation':[]}
    units = {'Number of fields':[],
             'Coverage':[]}
    fields = {'Area':[]}
    
    for rnd in range(trials):
        logging.info('Trial number %i:',rnd+1)
        map_dat, unit_dat, fld_dat = run_simulation(Param)
        combine(maps,map_dat)
        combine(units,unit_dat)
        combine(fields,fld_dat)

    # Store data in file
    tot = {'maps':maps,
           'units':units,
           'fields':fields}
    fn = 'exp results size%s,modes%s,plccells%d,grdcells%d,runs%d'%(Param.L,
                                                       str(Param.modules),
                                                       Param.plc_cells,
                                                       Param.grd_cells,
                                                       trials)
    cPickle.dump(tot,open(fn,'w'))
    logging.info('Finished an experiment: %.3f', time.time()-s)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Profile
    '''
    import cProfile
    Param.L=Param.W=Param.H=1
    cProfile.run('run_experiment(trials=1)',sort='cumulative')
    import sys; sys.exit()'''

    # Actually run an experiment
    for x in [1,2,3,4,5]:
        Param.L=Param.W=Param.H=x
        run_experiment(trials=10)
        
        # Sends email updates if expiriments are running on a server.
        '''
        msg= 'Finished simulation size %f'%(x,)
        #from customLogging import logger
        #logger.debug(msg)
        #print msg'''

        