'''
Created on Jun 20, 2014

@author: jshor
'''
import cPickle
from matplotlib import pyplot as plt
import numpy as np

def _load():
    results = []
    for i in range(1,23):
        with open('DensityEstimation/Results/input_density_estimation'+str(i),'r') as f:
            results.extend(cPickle.load(f))
    print 'Tot points: '+str(len(results))
    return np.array(results)

def show_full():
    
    results = _load()
    
    # Results is an array of lists of activities at a given place
    acts = [x[0] for x in results]
    plt.hist(acts,bins=40,normed=False)
    plt.show()

def show_cond():
    results = _load()
    tt = 8

    acts = [x[0] for x in results]
    plt.subplot(2,1,1)
    count, bins, _ = plt.hist(acts,bins=20,normed=False)
    plt.title('Original dist. Pts: %i'%(len(acts),))
    xlm = plt.xlim()
    
    plt.subplot(2,1,2)
    nb = [x[1] for x in results]
    plt.hist(nb,bins=bins,normed=False)
    plt.title('Side dist. Pts: %i'%(len(nb),))
    plt.xlim(xlm)
        
    def get_iss(i_target):
        mn = bins[i_target]; mx = bins[i_target+1]
        iss = np.intersect1d(np.nonzero(acts<=mx)[0], np.nonzero(acts>mn)[0])
        return iss
    mx_i = np.argmax(count)
    
    
    plt.figure()
    plt.subplot(2,1,1)
    nb = [x[1] for x in results]
    plt.hist(nb,bins=bins,normed=False)
    plt.title('Side dist. Pts: %i'%(len(nb),))
    plt.xlim(xlm)
    
    plt.subplot(2,1,2)
    iss = get_iss(mx_i+1)
    acts_neighbor = [x[1] for x in results[iss]]
    plt.hist(acts_neighbor,bins=bins,normed=False)
    plt.title('Pts: %i'%(len(acts_neighbor)))
    plt.xlim(xlm)
    
    plt.figure()
    for delt in range(-tt,tt):
        iss = get_iss(mx_i+delt)
    
        acts_neighbor = [x[1] for x in results[iss]]
        plt.subplot(2,tt,delt+tt+0)
        plt.hist(acts_neighbor,bins=bins,normed=False)
        plt.title('Pts: %i'%(len(acts_neighbor)))
        plt.xlim(xlm)
    plt.show()
    