'''
Created on Jun 2, 2014

@author: jshor
'''
from Simulation.optimize import grid_search
from Simulation.viewFitness import view
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    grid_search()
    #view()