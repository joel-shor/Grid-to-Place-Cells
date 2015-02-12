'''
Used in MakeFigureScript.py to generate a regression plot of the
area independent Poisson parameters.
'''

from numpy import linspace
from matplotlib import pyplot as plt
import figures.graphLib
from analysis.areaIndependentPoisson import calc_lambduhs
from data.simulations.experiment.load_experiment_data import load_multiple_numbers_of_fields as load
import logging
from scipy.stats import linregress

xs = linspace(0,35)
def _graph_init():
    plt.legend(loc='upper right')
    plt.title('Best Fit Poisson Parameter')
    plt.tight_layout(pad=1.2)

    plt.xlabel('Environment Area (m$^2$)')
    plt.xlim([min(xs),max(xs)])

    plt.ylabel(r'Poisson parameter ($\bar{\lambda}_{A_i}$)')

def _graph_poisson_parameter_regression(label, lambduhs, areas, bounds, clr):
    ''' Either plot linegraph+scatterplot or linegraph+error bars for lambda
        values. '''
    if not areas or not lambduhs: return
    a, b, r, _, _ = linregress(areas, lambduhs)

    linreg = plt.plot(xs, [x*a+b for x in xs], color=clr)
    logging.info('y=%.3fx+%.3f, r=%.5f',a,b,r)

    plt.scatter(areas, lambduhs, s=100, c=clr, marker='o',
                    label=label)
    if plot_bounds:
        plt.errorbar(areas, lambduhs, yerr=bounds, c=clr)


def regr(with_bounds):
    """ 'load' returns data of the form {side_len1: [num_flds,...],
                                         side_len2: [num_flds,...],
                                         ...
                                         }
    Note that lambduh_bounds are the errors relative to lambduh. For example,
    if lambduh_bounds = [[1,...], [2,...]] and lambduhs[0] = 7, then the real value
    lies in (7-1, 7+2).
    """
    global plot_bounds
    plot_bounds = with_bounds

    # Bring in the data in a nice form.
    num_flds_1 = load(side_lens=[1, 2, 2.5], subfolder='Group 1', plc_cells=500,
                     grd_cells=1000, modules=None)
    num_flds_2 = load(side_lens=[1, 2, 2.5, 3], subfolder='Group 2', plc_cells=500,
                     grd_cells=1000, modules=None)
    num_flds_3 = load(side_lens=[1, 2, 2.5], subfolder='Group 3', plc_cells=500,
                     grd_cells=1000, modules=None)
    num_flds_31 = load(side_lens=[1, 2, 3], subfolder='Group 3 no cutoff', plc_cells=500,
                     grd_cells=1000, modules=None)
    num_flds_4 = load(side_lens=[1, 2, 2.5], subfolder='Group 4', plc_cells=500,
                     grd_cells=1000, modules=0)
    num_flds_5 = load(side_lens=[1, 2, 2.5, 3], subfolder='Group 5', plc_cells=500,
                     grd_cells=1000, modules=None)

    # Calculate the lambdas from the place field data.
    lambdus_1, bounds_1, areas_1 = calc_lambduhs(num_flds_1)
    lambdus_2, bounds_2, areas_2 = calc_lambduhs(num_flds_2)
    lambdus_3, bounds_3, areas_3 = calc_lambduhs(num_flds_3)
    lambdus_31, bounds_31, areas_31 = calc_lambduhs(num_flds_31)
    lambdus_4, bounds_4, areas_4 = calc_lambduhs(num_flds_4)
    lambdus_5, bounds_5, areas_5 = calc_lambduhs(num_flds_5)

    # Graph the junks
    plt.figure('Poisson Parameter Regression')
    _graph_poisson_parameter_regression('Group 1', lambdus_1, areas_1, bounds_1, 'b')
    _graph_poisson_parameter_regression('Group 2', lambdus_2, areas_2, bounds_2, 'g')
    _graph_poisson_parameter_regression('Group 3', lambdus_3, areas_3, bounds_3, 'r')
    _graph_poisson_parameter_regression('Group 3 no cutoff', lambdus_31, areas_31, bounds_31, 'y')
    _graph_poisson_parameter_regression('Group 4', lambdus_4, areas_4, bounds_4, 'k')
    _graph_poisson_parameter_regression('Group 5', lambdus_5, areas_5, bounds_5, 'c')
    _graph_init()
    plt.show()
