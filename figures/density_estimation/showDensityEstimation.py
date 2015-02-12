'''
Created on Jun 20, 2014

@author: jshor
'''

import figures.graphLib
from matplotlib import pyplot as plt
import numpy as np
from data.simulations.density_estimation.load_density_data import load_one_cell_large_room, load_one_cell_small_room, load_adj3
from analysis.density_estimation import gaussian
from scipy.stats import norm


def show_full():

    results = load_same_loc()

    # Results is an array of lists of activities at a given place
    acts = [x[0] for x in results]
    plt.hist(acts,bins=70,normed=Normed)
    plt.show()

def show_conditional_probabilities():
    ''' Shows two rows of distributions. The top row gives
        the distribution of the input activity to place cells
        at various spatial locations. The second row shows
        the same distributions conditioned on the value of
        the (0,0) activity taking a certain value.

        Each file contains a list of 400 activity grids. Each grid is a 21x21 numpy
        matrix indicating the activity of cell 0 in a 21x21 grid centered around
        the middle of the room.
        '''

    GRID_SIZE = 21
    NORMED = True

    # Load data.
    results = load_one_cell_large_room()
    for grid in results:
        assert grid.shape == (GRID_SIZE, GRID_SIZE)

    # Computations.
    activities = {}; gaussians = {}
    for diagonal_distance_from_origin in range(10):
        dist = diagonal_distance_from_origin # for ease of reading
        activities[dist] = [grid_of_activity[dist,dist] for grid_of_activity in results]
        mn, std = gaussian(activities[dist])
        gaussians[dist] = {'mean': mn,
                           'std dev': std}

    x_bounds = (np.min(acts), np.max(acts))
    xs = np.linspace(np.min(acts), np.max(acts), 1000)
    mn, std = gaussian(acts)

    # Plot.
    plt.figure('Original distribution')
    count, bins, _ = plt.hist(acts, bins=40, normed=NORMED)
    plt.plot(xs, norm.pdf(xs, mn, std))
    plt.title('Original dist. Pts: %i'%(len(acts),))
    mx_i = np.argmax(count)
    iss = get_iss(mx_i, bins, acts)

    plt.figure('Conditional distributions')
    width = 10
    plt.subplot(2, width**2,1)

    for delt in range(width):
        plt.subplot(2,width,1+delt)
        cur_acts = [x[delt*2,delt*2] for x in results]

        plt.hist(cur_acts, bins=bins, normed=NORMED)

        mn, std = gaussian(cur_acts)
        plt.plot(xs,norm.pdf(xs,mn,std))
        plt.title('(%i,%i) O'%(delt*2,delt*2))
        plt.xlim(xlm)

    for delt in range(width):
        plt.subplot(2,width,width+1+delt)
        cur_acts = [x[delt,delt] for x in results[iss]]

        plt.hist(cur_acts, bins=bins, normed=NORMED)

        mn, std = gaussian(cur_acts)
        plt.plot(xs,norm.pdf(xs,mn,std))
        plt.title('(%i,%i) C'%(delt,delt))
        plt.xlim(xlm)

    plt.axis(tight=True)
    plt.show()

def show_adj3():
    ''' Shows two rows of distributions. The top row gives
        the distribution of the input activity to place cells
        at various spatial locations. The second row shows
        the same distributions conditioned on the value of
        the (0,0) activity taking a certain value. '''

    results = load_adj3()


    acts = [x[0] for x in results]
    plt.subplot(2,1,1)
    count, bins, _ = plt.hist(acts,bins=40,normed=Normed)
    plt.title('Original dist. Pts: %i'%(len(acts),))
    xlm = plt.xlim()
    xs = np.linspace(xlm[0],xlm[1],1000)
    mn, std = gaussian(acts)
    plt.plot(xs,norm.pdf(xs,mn,std))
    mx_i = np.argmax(count)
    iss = get_iss(mx_i, bins, acts)

    plt.figure()
    width = 5
    scale = 1
    plt.subplot(2,width,1)

    for delt in range(width):
        plt.subplot(2,width,1+delt)
        cur_acts = [x[delt*scale] for x in results]

        plt.hist(cur_acts,bins=bins,normed=Normed)

        mn, std = gaussian(cur_acts)
        plt.plot(xs,norm.pdf(xs,mn,std))
        plt.title('(%i,%i) O'%(delt*scale,delt*scale))
        plt.xlim(xlm)


    for delt in range(width):
        plt.subplot(2,width,width+1+delt)
        cur_acts = [x[delt*scale] for x in results[iss]]

        plt.hist(cur_acts,bins=bins,normed=Normed)

        mn, std = gaussian(cur_acts)
        plt.plot(xs,norm.pdf(xs,mn,std))
        plt.title('(%i,%i) C'%(delt*scale,delt*scale))
        plt.xlim(xlm)

    plt.axis(tight=True)
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
