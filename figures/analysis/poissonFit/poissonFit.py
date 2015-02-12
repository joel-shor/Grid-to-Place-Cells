'''
Reads in data and generates a graph comparing
the the graph of (number of place fields vs proportion of place cells with
that number of place fields)
against the graph of (x vs _poisson_distribution(x)).
'''

import figures.graphLib
from matplotlib import pyplot as plt
from analysis.poissonFit import best_poisson_fit
from data.simulations.experiment.load_experiment_data import load_number_of_fields_histogram as load

subfolder = 'Group 3 no cutoff'
modes = None
place_cells = 500
grid_cells= 1000
side_lens = [1, 2, 3]

def plot_poisson_curves(real_curves, theoretical_curves):
    plt.figure('poisson curve')

    # Print in sorted order
    iter = sorted(real_curves.items(),key = lambda x:x[0])
    for side_len, curve in iter:
        x, y = curve['Number of fields'], curve['Count']
        if side_len == 1:
            plt.plot(x, y, label='Area (m$^2$)= '+str(side_len**2))
        else:
            plt.plot(x, y, label=str(side_len**2))

    for side_len, curve in theoretical_curves.items():
        x, y = curve['Number of fields'], curve['Count']
        plt.plot(x, y,'--k')
    plt.legend()
    plt.show()

def graph_poisson_fit(calc_overall_best_fit):
    real_curves = load(subfolder, place_cells, grid_cells, modes, side_lens)
    theoretical_curves = best_poisson_fit(real_curves, calc_overall_best_fit)
    plot_poisson_curves(real_curves, theoretical_curves)