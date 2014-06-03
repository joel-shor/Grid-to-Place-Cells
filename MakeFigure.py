import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose which figure to graph.')
    parser.add_argument('graph_name',help='name of the graph to make',
                        choices=['grid',
                                 'regr',
                                 'regr_bounds',
                                 'spatial',
                                 'fit',
                                 'input',
                                 'inhib',
                                 'size',
                                 'typical'])

    nn = parser.parse_args().graph_name
    
    if nn == 'grid':    
        from Figures.gridCellFigures import example
        example()
    elif nn == 'regr':
        from Figures.paramRegression import regr
        regr()
    elif nn == 'regr_bounds':
        from Figures.paramRegression import regr_bounds
        regr_bounds()
    elif nn == 'spatial':
        from Figures.spatialStatistics import spatial
        spatial()
    elif nn == 'fit':
        from Figures.poissonFit import poisson_fit
        poisson_fit()
    elif nn == 'input':
        from Figures.placeCellInputFigures import example as ex2
        ex2()
    elif nn == 'inhib':
        from Figures.inhibFigures import example as ex3
        ex3()
    elif nn == 'size':
        from Figures.sizeCheck import example as ex4
        ex4()
    elif nn == 'typical':
        from Figures.typicalInput import example as ex5
        ex5()