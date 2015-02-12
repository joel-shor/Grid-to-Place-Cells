"""
A script for generating graphs.
Called as follows:
python MakeFigureScript.py xxxxxxx
where "xxxxx" is one of the choices below.
"""

import argparse
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Choose which figure to graph.')
    parser.add_argument('graph_name',help='name of the graph to make',
                        choices=[# Cell figures.
                                 'grid',
                                 'pre_inhibition',
                                 'post_inhibition',
                                 'size_cutoff',

                                 # Analysis figures.
                                 'poisson_param_regr',
                                 'poisson_param_regr_bounds',
                                 'spatial',
                                 'fit_poisson_per_room_size',
                                 'fit_poisson_overall',

                                 # Densities
                                 'conditional_probability'
                                 ])

    nn = parser.parse_args().graph_name

    # Cell figures.
    # Shows the output of grid cells
    if nn == 'grid':
        from figures.cells.GridCells.gridCellFigures import example
        example()
    # Plots the input to the place cell inhibition using different modules.
    # This is the summation of grid cell outputs.
    elif nn == 'pre_inhibition':
        from figures.cells.PlaceCells.inputToPlaceCellInhibitionFigures import display_with_modules
        display_with_modules()
    elif nn == 'post_inhibition':
        from figures.cells.PlaceFields.postInhibFigures import example as ex3
        ex3()
    elif nn == 'size_cutoff':
        from figures.cells.PlaceFields.sizeCheck import example as ex4
        ex4()

    # Analysis figures.
    elif nn == 'poisson_param_regr':
        from figures.analysis.areaIndependentPoisson.paramRegression import regr
        regr(with_bounds=False)
    elif nn == 'poisson_param_regr_bounds':
        from figures.analysis.areaIndependentPoisson.paramRegression import regr
        regr(with_bounds=True)
    elif nn == 'spatial':
        raise Exception("Not currently working.")
        from figures.analysis.spatialStatistics.spatialStatistics import spatial_statistics
        spatial_statistics()
    elif nn == 'fit_poisson_per_room_size':
        from figures.analysis.poissonFit.poissonFit import graph_poisson_fit
        graph_poisson_fit(calc_overall_best_fit = False)
    elif nn == 'fit_poisson_overall':
        from figures.analysis.poissonFit.poissonFit import graph_poisson_fit
        graph_poisson_fit(calc_overall_best_fit = True)

    # Density estimation figures.
    elif nn == 'conditional_probability':
        from figures.density_estimation.showDensityEstimation import show_conditional_probabilities
        show_conditional_probabilities()



