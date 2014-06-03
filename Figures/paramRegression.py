'''
Generates two graphs:
1) A linear regression of the Poisson parameters
2) A close up of the Poisson parameteres with error bounds

Called as:

python MakeFig.py regr
'''

import cPickle
import numpy as np
import logging

from matplotlib import pyplot as plt

import matplotlib as mpl
mpl.rcParams['font.size'] = 22
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.titlesize'] = 25
plt.rc('text', usetex=True)

from Results.load import load_old

SHOW = True # Show the graph or save it to file


def load(runs, modes, plc_cells, size):
    filename = 'Results/old/exp results size%s,modes%s,plccells%d,runs%d'%(str(size),
                                                        str(modes),
                                                        plc_cells,
                                                        runs)
    try:
        with open(filename,'r') as f:
            txt = f.read()
    finally:
        import pdb; pdb.set_trace()
    
    dat = cPickle.loads(txt)
    
    num_flds = dat['units']['Number of fields']
    
    if len(num_flds) != runs*plc_cells: raise Exception
    
    return num_flds

from scipy.stats import chi2
ALPHA = .05
def get_As(runs, modes,plc_cells,side_lens):
    area = []
    As = []
    As_bound = []
    for side_len in side_lens:
        num_flds = load(runs,modes, plc_cells, side_len)
        lambduh = np.average(num_flds)
        
        lower_bound = .5*chi2.ppf(ALPHA/2.0,2*sum(num_flds))/len(num_flds)
        upper_bound = .5*chi2.ppf(1-ALPHA/2.0,2*sum(num_flds)+2)/len(num_flds)
        
        A = 1.0*lambduh/(side_len**2)
        A_bound = [lower_bound/side_len**2, upper_bound/side_len**2]
        area.append(side_len**2)
        As.append(A)
        As_bound.append(A_bound)
    return area,As, As_bound

clrs = []
def graph_poisson_parameters_w_bounds(As1,As2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    xs = As1[0]+As2[0]
    xlim = [np.min(xs)-1,np.max(xs)+1]
        
    
    for As,clr,ylim,ax,lbl in zip([As1,As2],['b','g'],[(.25,.32),(.33,.65)],[ax1,ax2],
                            ['Network 1','Network 2']):
        y_lower = [A - bounds[0] for A, bounds in zip(As[1],As[2])]
        y_upper = [bounds[1] - A for A, bounds in zip(As[1],As[2])]
        ax.errorbar(As[0],As[1],yerr = [y_lower,y_upper],c=clr)
        
        for tl in ax.get_yticklabels():
            tl.set_color(clr)
        ax.set_ylim(ylim)

    #ax1.set_ylabel('Poisson parameter')
    #ax1.set_xlabel('Environment Area (m$^2$)')
    
    #plt.legend(loc='upper right')
    plt.xlim(xlim)
    plt.title('')
    plt.tight_layout(pad=1.2)
    
    if not SHOW:
        plt.savefig('Figures/poisson_parameter_summary_bounds.png')

from scipy.stats import linregress
def graph_poisson_parameter_regression(As1,As2):

    a, b, r,_,_ = linregress(As1[0],As1[1])
    a2, b2, r2,_, _ = linregress(As2[0],As2[1])
    
    xs = np.linspace(0,36,1000)
    linreg = plt.plot(xs,[x*a+b for x in xs],color='b')#,label='y=%.3fx+%.3f, r=%.5f'%(round(a,3),round(b,3),round(r,5)))
    linreg = plt.plot(xs,[x*a2+b2 for x in xs],color='g')#,label='y=%.3fx+%.3f, r=%.5f'%(round(a2,3),round(b2,3), round(r,5)))
    logging.info('y=%.3fx+%.3f, r=%.5f',a,b,r)
    logging.info('y=%.3fx+%.3f, r=%.5f',a2,b2,r2)
    
    pts = plt.scatter(As1[0],As1[1],s=100,c='b',marker='o',label='Network 1')
    pts = plt.scatter(As2[0],As2[1],s=100,c='g',marker='o',label='Network 2')
    
    plt.legend(loc='upper right')
    plt.title('Best Fit Poisson Parameter')
    plt.tight_layout(pad=1.2)
    
    plt.xlabel('Environment Area (m$^2$)')
    plt.xlim([min(xs),max(xs)])

    plt.ylabel(r'Poisson parameter ($\bar{\lambda}_{A_i}$)')
    plt.ylim([0,.7])
    
    
    if not SHOW:
        plt.savefig('Figures/poisson_parameter_summary.png')

def regr_bounds():
    logging.basicConfig(level=logging.DEBUG)
    
    As500 = get_As(runs=32,modes=None,plc_cells=500,side_lens=[1,2,3,4,5])
    As1500 = get_As(runs=32,modes=None,plc_cells=1500,side_lens=[1,2,3])
    
    graph_poisson_parameters_w_bounds(As500, As1500)
    #graph_poisson_parameter_regression(As500, As1500)
    if SHOW:
        plt.show()
  
def regr():
    logging.basicConfig(level=logging.DEBUG)
    
    As500 = get_As(runs=32,modes=None,plc_cells=500,side_lens=[1,2,3,4,5])
    As1500 = get_As(runs=32,modes=None,plc_cells=1500,side_lens=[1,2,3])
    
    #graph_poisson_parameters_w_bounds(As500, As1500)
    graph_poisson_parameter_regression(As500, As1500)
    if SHOW:
        plt.show()
    
                

if __name__ == '__main__':
    regr()