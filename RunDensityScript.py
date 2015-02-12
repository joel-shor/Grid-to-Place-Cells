import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-06-20'
__updated__ = '2014-06-20'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)


    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('act', choices=['same_location',
                                        'adjacent_data',
                                        'adjacent_data3',
                                        'final_activity'])

    # Process arguments
    args = parser.parse_args()

    act = args.act
    if act == 'same_location':
        from simulations.density_estimation.collectSameLocData import collectSameLocationData
        collectSameLocationData()
    elif act == 'adjacent_data':
        from simulations.density_estimation.DensityEstimation.collectAdjacentData import run as rn
        rn()
    elif act == 'adjacent_data3':
        from simulations.density_estimation.DensityEstimation.collectAdjacentData3 import run as rn3
        rn3()
    elif act == 'final_activity':
        from simulations.density_estimation.DensityEstimation.collectActivityProbData import run as rn4
        rn4()

if __name__ == "__main__":
    sys.exit(main())