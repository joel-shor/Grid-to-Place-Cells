''' Generate graphs for:
        units
            Number of fields
            Coverage
        maps
            Sparsity
            Coverage
            Representation
        fields
            Area
'''

import cPickle
import logging

from matplotlib import pyplot as plt
plt.rc('text', usetex=True)
import numpy as np

import matplotlib as mpl
mpl.rcParams['font.size'] = 22
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.titlesize'] = 25
#mpl.rcParams['axes.titlesize'] = 25

SHOW = True


def load(runs, modes, plc_cells,side_len, type_of_dat, dat):
    ''' Load data file and return environment area, average, and standard deviation '''
    
    filename = 'Results/exp results size%s,modes%s,plccells%d,runs%d'%(str(side_len),
                                                        str(modes),
                                                        plc_cells,
                                                        runs)
    with open(filename,'r') as f:
        txt = f.read()
    
    data = cPickle.loads(txt)
    
    x = data[type_of_dat][dat]
    avg = np.average(x)
    std = np.std(x)
    
    return side_len**2,avg, std

def graph_shit(network1,network2,title,yunit):
    ''' Graph the map statistics of the network1 and network2 networks
        on the same graph.
        
        network1 and network2 are data points [(x1,y1), (x2,y2), ...]
        yunit is the y axis label
        xaxis is the length of the x axis, obviously...
    '''
    plt.figure()
    

    
    grph1 =     plt.errorbar([x[0] for x in network1], 
                             [x[1] for x in network1], 
                             yerr=[x[2] for x in network1],
                             linewidth=5, label='Network 1')

    grph2 =     plt.errorbar([x[0] for x in network2], 
                             [x[1] for x in network2], 
                             yerr=[x[2] for x in network2],
                             linewidth=5, label='Network 2')

    # If the graph doesn't do a good job of centering the y axis
    #min_y = min([x[1] for x in network1] + [x[1] for x in network2])
    #max_y = max([x[1]-x[2] for x in network1] + [x[1]-x[2] for x in network2])
    #plt.ylim([min_y,1.01*max_y]
    
    plt.ylabel(yunit)
    plt.xlabel('Environment Area (m$^2$)')
    
    plt.xlim([0,1+np.max(np.array([x[0] for x in network2]+[x[0] for x in network1]))])
    #plt.locator_params(tight=True, nbins=7)
    plt.title(title)
    plt.tight_layout(.1,.5,.1)

def graph_expected_sparsity():
    ''' Graph the curve expected by a Poisson distribution. '''
    def exponential(x,lambduh):
            return np.exp(-1*lambduh*x)
    x = np.array(range(26))
    
    # These values are calculated from the best Poisson fit in
    #  generate graph of poissonparameter regression and errors.py
    y1 = exponential(x,0.272347)
    y2 = exponential(x,0.524838)
    plt.plot(x,y1,'--k')
    plt.plot(x,y2,'--k')

from scipy.stats import linregress
def linereggsion(network1,network2, main,sub):
    ''' Graph the curve expected by a Poisson distribution. '''
    
    xs = np.array(range(26))
    a, b, r,_,_ = linregress([x[0] for x in network1],[x[1] for x in network1])
    plt.plot(xs,xs*a+b,'--k')
    logging.info('r %s/%s, network1: %f + %f x, r=%f',main,sub,b,a,r)
    
    a, b, r,_,_ = linregress([x[0] for x in network2],[x[1] for x in network2])
    plt.plot(xs,xs*a+b,'--k')
    logging.info('r %s/%s, network2: %f + %f x, r=%f',main,sub,b,a,r)
    

def generate_graphs_for_spatial_statistics(main, sub, y_unit):
    ''' Takes the name of the main header of data and the subheader,
        as well as value that goes on the y-axis, and plots.
        
        main
            sub
        ---------------------
        units
            Number of fields
            Coverage
        maps
            Sparsity
            Coverage
            Representation
        fields
            Area
    '''

    
    #if sub != 'Representation': return
    runs = 32
    modes = None
    # Load data from network1 network
    network1 = []
    for room_len in [1,2,3,4,5]:
        network1.append(load(runs,modes,500,room_len,main,sub))
    
    # Load data from network2 network
    network2 = []
    for room_len in [1,2,3]:
        network2.append(load(runs,modes,1500,room_len,main,sub))

    graph_shit(network1, network2, main.capitalize()+': '+sub, y_unit)
    
    # If looking at sparsity, plot expected exponential curve
    if sub == 'Sparsity':
        graph_expected_sparsity()
        plt.legend(loc='upper right')
    if main == 'units' and sub == 'Coverage':
        linereggsion(network1,network2, main,sub)
    if sub == 'Number of fields':
        linereggsion(network1,network2, main,sub)
    if sub == 'Area':
        linereggsion(network1,network2, main,sub)
        
    if not SHOW:
        plt.savefig('Figures/'+main.capitalize().replace(' ','_')+'_'+sub+'.png')


def spatial():
    for (main, sub, y_unit) in [('units', 'Number of fields', 'Fields'),
                            ('units','Coverage', 'Proportion'),
                            ('maps', 'Sparsity', 'Proportion'),
                            ('maps', 'Coverage', 'Proportion'),
                            ('maps', 'Representation', 'Fields'),
                            ('fields','Area','Field Area (m$^2$)')]:
        generate_graphs_for_spatial_statistics(main, sub, y_unit)
    if SHOW:
        plt.show()
    
    
                