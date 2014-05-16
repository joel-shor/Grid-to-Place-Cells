'''
Used to find the best parameters for the experiment using
the fitness function as a metric.

NEEDS TO BE UPDATED

Created on Sep 21, 2013

@author: jshor
'''
import numpy as np
import time

from scipy.optimize import fmin_l_bfgs_b, fmin, anneal,brute
best = []
best_mean = 10*2
def fitness(a):
        [C,f_I,f_p, t] = a
        if C < 0:
            return 10**10*(-1*C) 
        if C>1:
            return 10**10*(-1*C)
        if f_I < 0:
            return 10**10*(-1*f_I) 
        if f_p < 0:
            return 10**10*(-1*f_p) 
        if t < 0:
            return 10**10*(-1*t)

        tot = []
        rpt_trls = 2
        for _ in range(rpt_trls):
            spars,cov = run(L=1,C=C, f_I=f_I,f_peak=f_p,thresh=t,MESH_PTS = 25)
            tot.append(10*(spars-.8)**2 + 100*(cov-1)**2)
        #tot.remove(np.max(tot))
        #tot.remove(np.min(tot))
        mean = 1.0*sum(tot)/rpt_trls
        std = np.sqrt(sum([(x-mean)**2 for x in tot]))
        global best_mean
        if mean < best_mean:
            print 'NEW BEST:', (C, f_I,f_p,t)
            
            best_mean = mean
        #\print a,':',mean,':',std
        return mean

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