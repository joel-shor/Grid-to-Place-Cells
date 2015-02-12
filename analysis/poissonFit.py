'''
Reads in data and generates a graph comparing
the the graph of (number of place fields vs proportion of place cells with
that number of place fields)
against the graph of (x vs _poisson_distribution(x)).
'''

from scipy.misc import factorial
import logging
import numpy as np

def _poisson_distribution(x,lambduh):
    return np.exp(-1*lambduh)*lambduh**x/factorial(x)

def calculate_lambda(number_of_fields, counts):
    iter = zip(number_of_fields, counts)
    fields = np.sum([place_fields * count for (place_fields, count) in iter])
    cells = np.sum([count for (_, count) in iter])
    return 1.0*fields/cells

def best_poisson_fit(real_curves, calc_overall_best_fit = False):

    Ls = {}
    for side_len, place_field_counts in real_curves.items():
        Ls[side_len] = calculate_lambda(place_field_counts['Number of fields'],
                                        place_field_counts['Count']) / side_len**2

    if calc_overall_best_fit:
        mean_lambduh = np.mean(Ls.values())
        Ls = {key: mean_lambduh for key, _ in Ls.items()}

    assert Ls.keys() == real_curves.keys()

    theoretical_curves = {}
    for side_len in Ls.keys():
        xs = real_curves[side_len]['Number of fields']
        theoretical_curves[side_len] = {'Number of fields': xs,
                                        'Count': _poisson_distribution(xs, Ls[side_len]*side_len**2)}

    return theoretical_curves