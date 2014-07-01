'''
Created on Jun 29, 2014

@author: joelshor
'''

import numpy as np

def gaussian(data):
    data = np.array(data)
    mn = np.mean(data)
    std = np.std(data)*data.size/(data.size-1)
    return mn, std