''' 
THIS MODULE IS DEFUNCT! SEE 'generate poisson parameter comparison.py'
FOR RECENT GRAPHS

This function takes a list of simulation data files.
Each data file contains the results from 32
runs of the simulation - the length of the
'Number of fields' values is 32*# of Place Fields.
Average over trials, poisson fit the results, and throw
down error bars to see if it matches
'''

import cPickle

from matplotlib import pyplot as plt

import matplotlib as mpl
mpl.rcParams['font.size'] = 22
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.titlesize'] = 25

SHOW = True


'''
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
MASS = importr('MASS')'''

def gen_count(dat):
    plc_flds = {}
    for x in dat:
        if x in plc_flds:
            plc_flds[x] += 1
        else:
            plc_flds[x] = 1
    return plc_flds

from scipy.stats import poisson
import numpy as np
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.1f'%round(height,1),
                ha='center', va='bottom')
def autolabel_diff(observed, predicted):
    for x in observed.keys():
        diff = np.abs(observed[x]-predicted[x])
        maxim = np.max([observed[x],predicted[x]])
        plt.text(x,1.05*maxim, '|$\Delta$|=%.1f'%(diff,),
                 ha='center',va='bottom')

def graph_actual_vs_predict3(freqs,good_lam, bad_lam, data_for_graph_text):
    expected = generate_theoretical(freqs,good_lam)
    maybe_expec = generate_theoretical(freqs,bad_lam)

    plt.figure()
    observed = plt.bar([x-.3 for x in freqs.keys()],freqs.values(),width=.2,color='blue')
                       #yerr=se.values(),ecolor='red',)
    observed.set_label('Observed values')
    #autolabel(observed)
    
    predicted = plt.bar([x-.1 for x in expected.keys()],expected.values(),width=.2,color='green')
    predicted.set_label('Best Fit')
    #autolabel(predicted)
    #
    maybe_pred = plt.bar([x+.1 for x in maybe_expec.keys()],maybe_expec.values(),width=.2,color='red')
    maybe_pred.set_label('Average Fit')
    #autolabel(predicted)
    
    #plt.title('Average Empirical Distribution vs Poisson')
    #plt.xlabel('Number of place fields')
    #plt.ylabel('Number of place cells')
    #plt.legend(loc='upper right')
    txt='\n'.join([str(key)+str(val) for key, val in data_for_graph_text.items()])
    #plt.text(max(freqs.keys())*.65,max(freqs.values())*0.4,txt)
    plt.xlim([-.4,max(freqs.keys())+.5])
    plt.tight_layout(pad=.5)


def graph_actual_vs_predict2(freqs,lambduh, data_for_graph_text):
    expected = generate_theoretical(freqs,lambduh)

    plt.figure()
    observed = plt.bar([x-.25 for x in freqs.keys()],freqs.values(),width=.25)
                       #yerr=se.values(),ecolor='red',)
    observed.set_label('Observed values')
    #autolabel(observed)
    
    predicted = plt.bar([x for x in expected.keys()],expected.values(),width=.25,color='green')
    predicted.set_label('Predicted values')
    #autolabel(predicted)
    #autolabel_diff(freqs, expected)
    
    #plt.title('Actual vs Predicted Poisson distribution for Average Empirical Distribution')
    plt.xlabel('Number of place fields')
    plt.ylabel('Number of place cells')
    plt.legend(loc='upper right')
    txt='\n'.join([str(key)+str(val) for key, val in data_for_graph_text.items()])
    plt.text(max(freqs.keys())*.65,max(freqs.values())*0.4,txt)

def generate_theoretical(freqs,lambduh):
    N = sum(freqs.values())
    end = max(freqs.keys())
    
    expected = {}
    
    for i in range(end):
        if i not in freqs: freqs[i] = 0
        expected[i] = N*poisson.pmf(i,lambduh)
        
    expected[end] = N - sum(expected.values())
    
    if np.sum(freqs.values()) != np.sum(expected.values()) or np.sum(expected.values())!=N:
        print np.sum(flds.values())
        print np.sum(expected.values())
        raise Exception()

    return expected

'''
from scipy.stats import poisson
from scipy.stats import chisquare
def calc_chi_sq(freqs, lambduh):
    tots = int(sum(freqs.values()))
    xs = range(max(freqs.keys())+1)
    theoretical = {x:tots*poisson.pmf(x,lambduh) for x in xs}
    theoretical[freqs.keys()[-1]] += tots - sum(theoretical.values())
    
    for x in xs:
        if freqs[x] < 5 or theoretical[x] < 5:
            freqs[x+1] += freqs[x]; theoretical[x+1] += theoretical[x]
            del freqs[x]; del theoretical[x]
            print 'deleted off the front', x
        else:
            break
    for x in xs[-1:0:-1]:
        if freqs[x] < 5 or theoretical[x] < 5:
            try:
                freqs[x-1] += freqs[x]
            except:
                freqs[x-1] = freqs[x]
            theoretical[x-1] += theoretical[x]
            del freqs[x]; del theoretical[x]
            print 'deleted off the back', x
        else:
            break
    
    if freqs.keys() != theoretical.keys(): raise Excpetion()
    if sum(freqs.values()) != sum(theoretical.values()) or sum(freqs.values()) != tots:
        import pdb; pdb.set_trace()
    for x in freqs.values(): 
        if x < 5: raise Exception()
    for x in theoretical.values():
        if x < 5: raise Exception()

    return chisquare(np.array(freqs.values()), 
                     np.array(theoretical.values()),
                     ddof=0)
'''
def regress(flds):
    # This is stupid!! It just calculates the average
    '''
    returns:
    1) lambda    
    2) standard error    
    '''
    xs = robjects.IntVector(flds)
    params = MASS.fitdistr(x=xs,densfun='Poisson')
    return [params[0][0],params[1][0]]#+calc_chi_sq(xs,params[0][0])

def load(runs, modes, plc_cells, size):
    filename = 'Data/exp results size%s,modes%s,plccells%d,runs%d'%(str(size),
                                                        str(modes),
                                                        plc_cells,
                                                        runs)
    with open(filename,'r') as f:
        txt = f.read()
    
    dat = cPickle.loads(txt)
    
    num_flds = dat['units']['Number of fields']
    if len(num_flds) != runs*plc_cells: raise Exception
    
    return num_flds

def get_average_dist(num_flds, plc_cells):
    if len(num_flds) % plc_cells != 0: raise Exception()
    runs = len(num_flds) / plc_cells
    # Get the average frequency distribution
    tot_cnt = {}
    for exp_num in range(runs):
        flds = num_flds[exp_num*plc_cells:(exp_num+1)*plc_cells]
        cnt = gen_count(flds)
        for fld_num, count in cnt.items():
            if fld_num in tot_cnt: tot_cnt[fld_num].append(count) 
            else: tot_cnt[fld_num] = [count]
    
    # Add the zeros
    for key, val in tot_cnt.items():
        tot_cnt[key].extend([0]*(runs-len(val)))
    #Check
    for val in tot_cnt.values():
        if len(val) != runs:
            print val
            import pdb; pdb.set_trace()
            raise Exception()
    avg_cnt = {key:np.mean(val) for key,val in tot_cnt.items()}
    se = {key:1.0*np.std(val)/np.sqrt(runs) for key, val in tot_cnt.items()}
    return avg_cnt, se

def do_stuff(runs, modes, plc_cells,size):
    
    num_flds = load(runs,modes, plc_cells, size)
    lambduh, lambduh_se, = regress(num_flds)
    A = 1.0*lambduh/(size**2)
    A_se = 1.0*lambduh_se/size**2

    freqs, se = get_average_dist(num_flds, plc_cells)
    #t, p = calc_chi_sq({x:y for x,y in freqs.items()},avg_A*size**2)
    
    data_for_graph_text = {'Size:':size,
                           'Modules:':modes,
                           'A:':round(A,5),
                           'Place Cells:':plc_cells}
    graph_actual_vs_predict2(freqs,A*size**2, data_for_graph_text)
    
    if SHOW:
        plt.show()
    else:
        if runs == 32:
            plt.savefig('Figures/L_%d_plccells_%d.png'%(size,plc_cells))
        else:
            plt.savefig('Figures/L_%d_plccells_%d_runs_%d.png'%(size,plc_cells,runs))
        plt.close()
    return A, A_se

from scipy.stats import linregress, chi2
alpha = .05
def generate_graphs_for_poisson_regression_fit():
    ''' This function takes a list of simulation data files.
        Each data file contains the results from 32
        runs of the simulation - the length of the
        'Number of fields' values is 32*# of Place Fields.
        Poisson regress each simulation, determine
        the coefficient and fit, and display the graphs
    '''

    runs = 32
    modes = None
    plc_cells=500
    As= {}
    As_bound = {}
    for size in [1,2,3,4,5]:
        num_flds = load(runs,modes, plc_cells, size)
        lambduh = np.average(num_flds)
        
        lower_bound = .5*chi2.ppf(alpha/2.0,2*sum(num_flds))/len(num_flds)
        upper_bound = .5*chi2.ppf(1-alpha/2.0,2*sum(num_flds)+2)/len(num_flds)
        
        A = 1.0*lambduh/(size**2)
        A_bound = [lower_bound/size**2, upper_bound/size**2]
        As[size] = A
        As_bound[size] = A_bound
    
    avg_A = np.average(As.values())
    for size, A in As.items():
        num_flds = load(runs,modes, plc_cells, size)
        freqs, se = get_average_dist(num_flds, plc_cells)
        #t, p = calc_chi_sq({x:y for x,y in freqs.items()},avg_A*size**2)
        
        data_for_graph_text = {'Size:':size,
                               'Modules:':modes,
                               'A:':round(A,5),
                               'Average A:':round(avg_A,5),
                               'Place Cells:':plc_cells}
        graph_actual_vs_predict3(freqs,A*size**2, avg_A*size**2, 
                                 data_for_graph_text)
        
        if SHOW:
            plt.show()
        else:
            if runs == 32:
                plt.savefig('Figures/L_%d_plccells_%d.png'%(size,plc_cells))
            else:
                plt.savefig('Figures/L_%d_plccells_%d_runs_%d.png'%(size,plc_cells,runs))
            plt.close()
    
    runs = 32
    modes = None
    plc_cells=1500
    As2= {}
    As2_bound = {}
    for size in [1,2,3]:
        num_flds = load(runs,modes, plc_cells, size)
        lambduh = np.average(num_flds)
        
        lower_bound = .5*chi2.ppf(alpha/2.0,2*sum(num_flds))/len(num_flds)
        upper_bound = .5*chi2.ppf(1-alpha/2.0,2*sum(num_flds)+2)/len(num_flds)
        
        A = 1.0*lambduh/(size**2)
        A_bound = [lower_bound/size**2, upper_bound/size**2]
        As2[size] = A
        As2_bound[size] = A_bound
        
    avg_A = np.average(As2.values())
    for size, A in As2.items():
        num_flds = load(runs,modes, plc_cells, size)
        freqs, se = get_average_dist(num_flds, plc_cells)
        data_for_graph_text = {'Size:':size,
                               'Modules:':modes,
                               'A:':round(A,5),
                               'Average A:':round(avg_A,5),
                               'Place Cells:':plc_cells}
        graph_actual_vs_predict3(freqs,A*size**2, avg_A*size**2, 
                                 data_for_graph_text)
        if SHOW:
            plt.show()
        else:
            if runs == 32:
                plt.savefig('Figures/L_%d_plccells_%d.png'%(size,plc_cells))
            else:
                plt.savefig('Figures/L_%d_plccells_%d_runs_%d.png'%(size,plc_cells,runs))
            plt.close()

    a, b, r,_,_ = linregress(As.keys(),As.values())
    a2, b2, r2,_, _ = linregress(As2.keys(),As2.values())
    
    #_, sub = plt.subplots(3,sharex=True)
    xs = np.linspace(0,7,1000)
    linreg = plt.plot(xs,[x*a+b for x in xs],color='b')#,label='y=%.3fx+%.3f, r=%.5f'%(round(a,3),round(b,3),round(r,5)))
    linreg = plt.plot(xs,[x*a2+b2 for x in xs],color='g')#,label='y=%.3fx+%.3f, r=%.5f'%(round(a2,3),round(b2,3), round(r,5)))
    print 'y=%.3fx+%.3f, r=%.5f'%(round(a,3),round(b,3),round(r,5))
    print 'y=%.3fx+%.3f, r=%.5f'%(round(a2,3),round(b2,3), round(r2,5))
    
    #linreg = sub[0].plot(xs,[x*a+b for x in xs],color='b',label='y=%.3fx+%.3f'%(round(a,3),round(b,3)))
    pts = plt.scatter(As.keys(),As.values(),s=100,c='b',marker='o',label='500 place cells')
    pts = plt.scatter(As2.keys(),As2.values(),s=100,c='g',marker='o',label='1500 place cells')
    plt.legend(loc='upper right')
    plt.tight_layout(pad=1.2)
    plt.ylabel('Poisson parameter')
    plt.xlim([0,6])
    plt.xlabel('Side Length (m)')
    
    plt.figure()
    y_lower = [As[size] - As_bound[size][0] for size in As.keys()]
    y_upper = [As_bound[size][1] - As[size] for size in As.keys()]
    pts = plt.errorbar(As.keys(),As.values(),yerr = [y_lower,y_upper],
                       c='b',label='500 place cells')
    plt.legend(loc='upper right')
    plt.tight_layout(pad=1.2)
    plt.ylabel('Poisson parameter')
    plt.xlim([0,6])
    #pts = sub[0].scatter(As2.keys(),As2.values(),s=20,c='r',marker='o',label='Place Cells = 1500')
    #sub.xlim([0,10])
    #sub.ylim([0,1.1*max(As2.values())])
    
    #linreg = plt.plot(xs,[x*a2+b2 for x in xs],color='r',label='y=%.3fx+%.3f, r=%.5f'%(round(a2,3),round(b2,3),round(r2,5)))
    
    plt.figure()
    y_lower = [As2[size] - As2_bound[size][0] for size in As2.keys()]
    y_upper = [As2_bound[size][1] - As2[size] for size in As2.keys()]
    pts = plt.errorbar(As2.keys(),As2.values(),yerr = [y_lower,y_upper],
                       c='g',label='1500 place cells')
    plt.legend()
    plt.tight_layout(pad=1.2)
    plt.ylabel('Poisson parameter')
    plt.xlim([0,6])

    #sub[0].set_title('A Constant')

    
    
    plt.show()

if __name__ == '__main__':
    
    #do_stuff(2,None,plc_cells=2500,size=1)
    #do_stuff(2,None,plc_cells=5000,size=1)

    generate_graphs_for_poisson_regression_fit()
    
                