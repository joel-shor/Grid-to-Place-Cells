import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose which figure to graph.')
    parser.add_argument('graph_name',help='name of the graph to make',
                        choices=['grid',
                                 'regr',
                                 'regr_bounds'])

    nn = parser.parse_args().graph_name
    
    if nn == 'grid':    
        from Figures.gridCellFigures import example
        example()
    elif nn == 'regr':
        from Figures.paramRegression import regr
        regr()
    elif nn == 'regr_nounds':
        pass