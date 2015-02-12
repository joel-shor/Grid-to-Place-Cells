'''
??
'''

import numpy as np
from scipy.stats import chi2

ALPHA = .05

def calc_lambduhs(num_flds):
    """ Calculate and return the statistics on area-independent Poisson parameter
    for a collection of repeated experiments with the same parameters but different
    room sizes.

    num_flds takes the form {side_len1: [num_flds,...],
                             side_len2: [num_flds,...],
                             ...
                            }

    Note that lambduh_bounds are the errors relative to lambduh. For example,
    if lambduh_bounds = [[1,...], [2,...]] and lambduhs[0] = 7, then the real value
    lies in (7-1, 7+2)."""

    lambduhs = []; lambduh_bounds = [[], []]; areas = []
    for side_len, flds in num_flds.items():
        lambduh, lambduh_bound, area = calc_lambduh(flds, side_len)
        lambduhs.append(lambduh); areas.append(area)
        for i in [0,1]:
            lambduh_bounds[i].append(lambduh_bound[i])
    return lambduhs, lambduh_bounds, areas

def calc_lambduh(num_flds, side_len):
    lower_bound = .5*chi2.ppf(ALPHA/2.0,2*sum(num_flds))/len(num_flds)
    upper_bound = .5*chi2.ppf(1-ALPHA/2.0,2*sum(num_flds)+2)/len(num_flds)

    lambduh = 1.0*np.average(num_flds)/(side_len**2)

    lambduh_bound = [lower_bound/side_len**2, upper_bound/side_len**2]
    area = side_len**2
    return lambduh, lambduh_bound, area