''' Provides a common format for plotting figures that will
be used in the write-up. '''

import matplotlib as mpl
mpl.rcParams['font.size'] = 25
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['axes.titlesize'] = 25
font = {'weight' : 'bold',
        'size'   : 25}
mpl.rc('font', **font)

from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap


def _plot(Xs,Ys, Zs,title,cmapping=get_cmap('Reds')):
    plt.figure()
    cntr = plt.contourf(Xs,Ys,Zs,cmap=cmapping)
    plt.colorbar(cntr, extend='both')
    if title: plt.title(title)
    plt.axis('off')
    plt.tight_layout(pad=.1, h_pad=.1, w_pad=.1)