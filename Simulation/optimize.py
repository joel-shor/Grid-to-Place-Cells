'''
Used to find the best parameters for the experiment using
the fitness function as a metric.

Created on Sep 21, 2013

@author: jshor
'''
from itertools import product
import time
import logging
import re

from Simulation.params import Param as pm
from Simulation.simulation import run_simulation
from Cells.PlaceFields import PlaceField as pf

max_fit_runs = 1

#from scipy.optimize import fmin_l_bfgs_b, fmin, anneal,brute
best = []
best_mean = 10*2

def _validate_params(thresh,f_I):
    return True

def fitness(a):
    ''' Fitness function for optimization
    a  = (thresh,f_I) '''
    [f_I, thresh] = a
    try:
        assert _validate_params(thresh,f_I)
    except:
        return 10**8

    pm.f_I = f_I
    pm.thresh=thresh
    maps, _, _ = run_simulation(pm)
    
    assert len(maps['Sparsity']) == 1
    sparsity = maps['Sparsity'][0]
    
    assert len(maps['Coverage']) == 1
    coverage = maps['Coverage'][0]
    
    return sparsity, coverage
    
fn = 'Simulation/optimize_results.txt'
def prev_results():
    ''' Read in previous optimization results.
        Grid cells:    Place cells: 
        C    thresh    f_I    f_p    :    [(spars1,cov1), (spars2,cov2),... ]'''
    dat = {}
    
    try:
        with open(fn,'r') as f:
            tmp = f.readlines()
    except:
        return dat
    
    for ln in tmp[2:]:
        C,thresh,f_I,f_p,_,fits = ln.split('    ')
        key = (float(C), float(thresh), float(f_I), float(f_p))
        
        assert key not in dat

        fit_l = [(float(a),float(b)) for a,b in re.findall('\((.*?),(.*?)\)',fits)]
        dat[key] = fit_l
    
    return dat

def grid_search():
    dat = prev_results()
    tot_time = 0
    
    # Init pm
    pm.modules = None
    #min_plcfld_size = .05
    pm.min_plcfld_size = .005
    #min_grid_size = .0001
    pm.min_grid_size = .0004 # m**2
    #pm.min_grid_size = .01 # m**2
    pm.plc_cells = 500
    pm.grd_cells = 1000
    pm.L=pm.W=pm.H=1

    pm.C = .33
    pm.f_p = 15
    
    #f_Is = np.arange(4,7,1)
    f_Is = [1]
    
    #threshs = [.005,.006,.007,.008,.009,.01,.1,1]
    threshs = [.05]
    
    
    repeats = range(3)
    
    arr = [x for x in product(f_Is,threshs,repeats)]
    
    for i in range(len(arr)):
        logging.warning('Round %i/%i',i+1,len(arr))
        f_I, thresh, _ = arr[i]
        key = (pm.C,thresh,f_I,pm.f_p)
        if key in dat and len(dat[key]) >= max_fit_runs: continue
        
        logging.warning('Starting f_I:%.3f, thresh:%.3f',f_I,thresh)
        s = time.time()
        spars,cov = fitness([f_I, thresh])
        f = time.time()
        tot_time += f-s
        logging.warning('Took time %.3f',f-s)
        
        if key not in dat:
            dat[key] = [(spars,cov)]
        else:
            dat[key].append((spars,cov))
    
        write_to_file(dat)

def write_to_file(dat):
    ''' Write data structure to file.
        key = (C,thresh,f_I,f_p) '''
    
    with open(fn,'w') as f:
        f.write('Place cells: 500    Grid cells: 1000\n')
        f.write('C    thresh    f_I    f_p    :    (spars1,cov1), (spars2,cov2),... \n')
        tstr = '%f    %f    %f    %f    :    %s\n'
        for key,fits in dat.items():
            cur = tstr%(key[0],key[1],key[2],key[3],fits)
            f.write(cur)

'''
import cPickle
def optimize():
    G2 = 6
    G3 = 3
    G4 = 6
    dat = np.zeros([G2,G3,G4])
    stds = np.zeros([G2,G3,G4])
    min_mean = min_std = params = 10**2
    for C in [1]:
        for f_I in range(G2):
            for f_peak in range(G3):
                for thresh in range(G4):
                    
                    c1 = .31
                    fi1 = np.linspace(700,5000,G2)[f_I]
                    fp1 = np.linspace(750,850,G3)[f_peak]
                    t = np.linspace(8,50,G4)[thresh]
                    s=time.time()
                    mean,std = fitness([c1,fi1,fp1,t])
                    f=time.time()
                    print 'One trial:', round(f-s,3)
                    dat[C,f_I,f_peak,thresh] = mean
                    stds[C,f_I,f_peak,thresh] = std
                    if mean < min_mean:
                        min_mean=mean
                        min_std = std
                        min_params = (C,f_I,f_peak,thresh)
                        print 'NEW MIN:', mean, ':',std,':',(c1,fi1,fp1,t)
                    
    with open('course trials2','w') as f:
        f.write(cPickle.dumps(dat))
    import pdb; pdb.set_trace()
'''
