'''
Created on Jun 2, 2014

@author: jshor
'''

from Simulation.optimize import prev_results
import numpy as np

def view():
    dat = prev_results()
    rdat = [(x,np.mean(fits)) for x,fits in dat.items()]
    rdat.sort(key=lambda x: x[1])
    str1 = '%s    :    %.6f'
    for x,fit in rdat:
        print str1%(x,fit)