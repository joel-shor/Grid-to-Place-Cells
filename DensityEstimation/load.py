'''
Created on Jun 29, 2014

@author: joelshor
'''
import cPickle
import numpy as np

def _load(base):
    results = []
    for i in range(1,23):
        with open('DensityEstimation/Results/'+base+str(i),'r') as f:
            results.extend(cPickle.load(f))
    print 'Tot points: '+str(len(results))
    return np.array(results)

def load_same_loc():
    ''' An array of list elements containing the input to place cells
        at the center of a 1m x 1m room. '''
    return _load('Same Loc/input_density_estimation')
    

def load_adj():
    return _load('Adjacent/adjacent_data')
    