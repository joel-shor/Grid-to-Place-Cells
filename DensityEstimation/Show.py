'''
Created on Jun 20, 2014

@author: jshor
'''
from matplotlib import pyplot as plt
import numpy as np
from DensityEstimation.load import load_same_loc, load_adj
from DensityEstimation.fitCurve import gaussian
from scipy.stats import norm

Normed = True

def show_full():
    
    results = load_same_loc()
    
    # Results is an array of lists of activities at a given place
    acts = [x[0] for x in results]
    plt.hist(acts,bins=70,normed=Normed)
    plt.show()

def show_adj():
    results = load_adj()

    import pdb; pdb.set_trace()
    acts = [x[0,0] for x in results]
    plt.subplot(2,1,1)
    count, bins, _ = plt.hist(acts,bins=40,normed=Normed)
    plt.title('Original dist. Pts: %i'%(len(acts),))
    xlm = plt.xlim()
    xs = np.linspace(xlm[0],xlm[1],1000)
    mn, std = gaussian(acts)
    plt.plot(xs,norm.pdf(xs,mn,std))
    mx_i = np.argmax(count)
    
    nb = [x[0,1] for x in results]
    plt.subplot(2,1,2)
    plt.hist(nb,bins=40,normed=Normed)
    plt.title('Original dist. Pts: %i'%(len(nb),))
    xs = np.linspace(xlm[0],xlm[1],1000)
    mn, std = gaussian(acts)
    plt.plot(xs,norm.pdf(xs,mn,std))
    
    plt.figure()
    plt.subplot(2,3,1)
    plt.hist(acts,bins=40,normed=Normed)
    plt.xlim(xlm)
    iss = get_iss(mx_i, bins, acts)
    
    cur_plot = 1
    for xdelt in range(2):
        for ydelt in range(2):
            if xdelt == 0 and ydelt == 0: continue
            plt.subplot(2,3,3+cur_plot)
            cur_plot += 1
            cur_acts = [x[xdelt,ydelt] for x in results[iss]]

            plt.hist(cur_acts,bins=bins,normed=Normed)
    
            mn, std = gaussian(cur_acts)
            plt.plot(xs,norm.pdf(xs,mn,std))
            plt.title('Pts: %i'%(len(cur_acts)))
            plt.xlim(xlm)
    plt.show()
    
    
def get_iss(i_target, bins, acts):
    mn = bins[i_target]; mx = bins[i_target+1]
    iss = np.intersect1d(np.nonzero(acts<=mx)[0], np.nonzero(acts>mn)[0])
    return iss
       
def show_cond():
    results = load_same_loc()
    tt = 8

    # Graph the histogram of activity at the center of
    #  of the room from cell 0
    acts = [x[0] for x in results]
    plt.subplot(2,1,1)
    count, bins, _ = plt.hist(acts,bins=40,normed=Normed)
    plt.title('Original dist. Pts: %i'%(len(acts),))
    xlm = plt.xlim()
    xs = np.linspace(xlm[0],xlm[1],1000)
    mn, std = gaussian(acts)
    plt.plot(xs,norm.pdf(xs,mn,std))
    
    # Graph the histogram of activity at the center of
    #  of the room from cell 1
    plt.subplot(2,1,2)
    nb = [x[1] for x in results]
    plt.hist(nb,bins=bins,normed=Normed)
    mn, std = gaussian(nb)
    plt.plot(xs,norm.pdf(xs,mn,std))
    plt.title('Side dist. Pts: %i'%(len(nb),))
    plt.xlim(xlm)
        
    mx_i = np.argmax(count)
    
    
    plt.figure()
    plt.subplot(2,1,1)
    nb = [x[1] for x in results]
    plt.hist(nb,bins=bins,normed=Normed)
    plt.title('Side dist. Pts: %i'%(len(nb),))
    mn, std = gaussian(nb)
    plt.plot(xs,norm.pdf(xs,mn,std))
    plt.xlim(xlm)
    
    plt.subplot(2,1,2)
    iss = get_iss(mx_i+1, bins, acts)
    acts_neighbor = [x[1] for x in results[iss]]
    plt.hist(acts_neighbor,bins=bins,normed=Normed)
    plt.title('Pts: %i'%(len(acts_neighbor)))
    nb = acts_neighbor
    mn, std = gaussian(nb)
    plt.plot(xs,norm.pdf(xs,mn,std))
    plt.xlim(xlm)
    
    plt.figure()
    for delt in range(-tt,tt):
        iss = get_iss(mx_i+delt, bins, acts)
    
        acts_neighbor = [x[1] for x in results[iss]]
        plt.subplot(2,tt,delt+tt+0)
        plt.hist(acts_neighbor,bins=bins,normed=Normed)
        nb = acts_neighbor
        mn, std = gaussian(nb)
        plt.plot(xs,norm.pdf(xs,mn,std))
        plt.title('Pts: %i'%(len(acts_neighbor)))
        plt.xlim(xlm)
    plt.show()
    