''' The driver module for the experiments. Contains
    functions for parameter initialization and shell
    function for running repeated trials. '''

import time
import cPickle
import logging

from Simulation.simulation import run_simulation
from Simulation.params import Param

def combine(main, new):
    ''' Adds fields in dictionary 'new' to dictionary 'main'. '''
    if new is None: return
    for key in main.keys():
        main[key].extend(new[key])
        
def run_experiment2(trials,pm):
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
        map_dat, unit_dat, fld_dat = run_simulation(pm)
        combine(maps,map_dat)
        combine(units,unit_dat)
        combine(fields,fld_dat)

    # Store data in file
    tot = {'maps':maps,
           'units':units,
           'fields':fields}
    fn = 'exp results size%s,modes%s,plccells%d,grdcells%d,runs%d'%(pm.L,
                                                       str(pm.modules),
                                                       pm.plc_cells,
                                                       pm.grd_cells,
                                                       trials)
    cPickle.dump(tot,open(fn,'w'))
    logging.info('Finished an experiment: %.3f', time.time()-s)

def run_experiment(pm, trials):
    ''' The shell function to cycle through repeated trials.'''
    
    pm.validate()
    
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
        maps, units, fields = run_simulation(pm)
        
        # Store data in file
        tot = {'maps':maps,
               'units':units,
               'fields':fields}
        fn = 'exp results size%s,modes%s,plccells%d,grdcells%d,runs%d'%(pm.L,
                                                           str(pm.modules),
                                                           pm.plc_cells,
                                                           pm.grd_cells,
                                                           rnd+10)
        cPickle.dump(tot,open(fn,'w'))
        logging.info('Total experiment time so far: %.3f', time.time()-s)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    pm = Param # Makes warnings go away by making pm local
    
    pm.modules = None
    #pm.min_plcfld_size = .005
    pm.min_plcfld_size = 0.0
    pm.min_grid_size = .0004 # m**2
    
    pm.C = 0.30
    pm.thresh = 0.0075
    pm.f_I = 5.31
    pm.f_p = 15
    pm.wt_type = 'Monaco'
    pm.use_cutoff = False
    
    
    pm.plc_cells = 500
    pm.grd_cells = 1000

    # Profile
    '''
    import cProfile
    pm.L=pm.W=pm.H=1
    cProfile.run('run_experiment(trials=1)',sort='cumulative')
    import sys; sys.exit()'''

    # Actually run an experiment
    for x in [3]:
        pm.L=pm.W=pm.H=x
        run_experiment(pm,trials=15)
        
        # Sends email updates if expiriments are running on a server.
        '''
        msg= 'Finished simulation size %f'%(x,)
        #from customLogging import logger
        #logger.debug(msg)
        #print msg'''

        