''' 
Reads in data and generates a graph comparing
the the graph of (number of place fields vs proportion of place cells with
that number of place fields)
against the graph of (x vs Poisson(x)).
'''

from scipy.misc import factorial
import logging
import numpy as np
from Results.load import load_old as load
#from Results.load import load_new as load

import matplotlib as mpl
mpl.rcParams['font.size'] = 22
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.titlesize'] = 25

from matplotlib import pyplot as plt
plt.rc('text', usetex=True)

SHOW = True

from scipy.optimize import fmin
def calc_best_avg_A(runs, modes, plc_cells,side_lens, first_guess, grd_cells):
    '''
    Uses optimization to fmin the L2 error of the Poisson fitting
    '''
    
    # Read in all the data
    num_flds_all = {}
    for side_len in side_lens:
        num_flds = np.array(load(modes, plc_cells, side_len, grd_cells,runs))
        x = []; y = []
        for num_fld in range(np.max(num_flds)+1):
            x.append(num_fld)
            y.append(1.0*np.count_nonzero(num_flds == num_fld)/len(num_flds))
        num_flds_all[side_len] = [x,y]
    
    def error(lambduh):
        err = 0
        for side_len in num_flds_all.keys():
            cur_lambduh = side_len**2*lambduh
            x = range( np.max(num_flds_all[side_len][0])+1 )
            y_estimates = Poisson(x,cur_lambduh)
            for i in range(len(x)): 
                y_target = num_flds_all[side_len][1][i]
                y_estimate = y_estimates[i]
                err += (y_target - y_estimate)**2
        return err
    
    result = fmin(error, first_guess)
    return result[0]
    
        
def Poisson(x,lambduh):
    return np.exp(-1*lambduh)*lambduh**x/factorial(x)


def generate_graphs_for_total_poisson_comparison(runs, modes, plc_cells,side_lens,grd_cells=None):    
    ''' Generates a comparison graph between the data and a 
        theoretical Poisson distribution.
        
        Based on which code is commented out, the theoretical distribution can
        either be the best-fitted Poisson distribution or one with Poisson
        parameter that scales with area. '''
    
    # Read in a list of the number of fields
    #  for each place cell
    
    plt.figure()
    max_num_flds = 0
    As= {}
    
    for side_len in side_lens:
        num_flds = np.array(load(modes, plc_cells, side_len,grd_cells, runs))
        
        # Generate data curve that we hope looks Poisson
        x = []; y = []

        for num_fld in range(np.max(num_flds)+1):
            x.append(num_fld)
            y.append(1.0*np.count_nonzero(num_flds == num_fld)/len(num_flds))
        lambduh = np.average(num_flds)
        logging.info('Best lambduh for %.1f is %.5f', side_len, lambduh)
        if side_len == 1:
            plt.plot(x,y,label='Area (m$^2$)= '+str(side_len**2))
        else:
            plt.plot(x,y,label=str(side_len**2))
            
        A = 1.0*lambduh/(side_len**2)
        As[side_len] = A
        if np.max(num_flds) > max_num_flds:
            max_num_flds = np.max(num_flds)
    
    
    '''
    # Finally, do the average best fit poisson curves
    A_avg = np.average(As.values())
    A_best = calc_best_avg_A(runs, modes, plc_cells,side_lens, A_avg, grd_cells)
    #A_best = A_avg
    
    logging.debug('Best Average A: %f',A_best)
    x = range(max_num_flds+1)
    for side_len in As.keys():
        lambduh = A_best * side_len**2
        logging.info('Best overall lambduh: %.5f',A_best)
        y = Poisson(x,lambduh)
        if side_len == As.keys()[0]:
            #plt.plot(x,y,'-.',label='\lambda = %.3f'%(lambduh,))
            plt.plot(x,y,'--k')
        else:
            #plt.plot(x,y,'-.k',label=round(lambduh,3))
            plt.plot(x,y,'--k')
    #plt.legend()
    plt.xlabel('Number of Place Fields')
    #plt.ylabel('Proportion of Cell Population')
    plt.title('Best Overall Poisson Fit')
    #plt.xlim([0,18])
    if not SHOW:
        plt.savefig('Figures/Poisson_average_fit_curves_plccells_%d_runs_%d.png'%(plc_cells,runs))
    '''
    
    
    # Now do the theoretical best fit poisson curves
    ''''''
    x = range(max_num_flds+1)
    for side_len, A in As.items():
        lambduh = A * side_len**2
        y = Poisson(x,lambduh)
        if side_len == As.keys()[0]:
            #plt.plot(x,y,'--',label='\lambda = %.3f'%(lambduh,))
            plt.plot(x,y,'--k')
        else:
            plt.plot(x,y,'--k')
    plt.legend()
    plt.xlabel('Number of Place Fields')
    plt.ylabel('Proportion of Cell Population')
    plt.title('Best Poisson Fit')
    #plt.xlim([0,18])
    if not SHOW:
        plt.savefig('Figures/Poisson_best_fit_curves_plccells_%d_runs_%d.png'%(plc_cells,runs)) 
    
def poisson_fit():
    logging.basicConfig(level=logging.INFO)   
    #generate_graphs_for_total_poisson_comparison(runs=10,modes=None,plc_cells=25,grd_cells=500,side_lens=[1,2,3,4,5])
    generate_graphs_for_total_poisson_comparison(runs=32,modes=None,plc_cells=500,grd_cells=1000,side_lens=[1,2,3,4,5])
    #generate_graphs_for_total_poisson_comparison(runs=32,modes=None,plc_cells=500,side_lens=[1,2,3,4,5])
    #generate_graphs_for_total_poisson_comparison(runs=32,modes=None,plc_cells=1500,side_lens=[1,2,3])
    if SHOW: plt.show()
    