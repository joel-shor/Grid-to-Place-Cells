#!/usr/local/bin/python2.7
# encoding: utf-8
'''
EstimateDensity -- shortdesc

EstimateDensity is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

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

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2014 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))


    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('act', choices=['estInp','showfull','showcond', 'adj',
                                        'showadj'])
    
    # Process arguments
    args = parser.parse_args()

    act = args.act
    if act == 'estInp':
        from DensityEstimation.collectSameLocData import run
        run()
    elif act == 'showfull':
        from DensityEstimation.Show import show_full
        show_full()
    elif act == 'showcond':
        from DensityEstimation.Show import show_cond
        show_cond()
    elif act == 'adj':
        from DensityEstimation.collectAdjacentData import run as rn
        rn()
    elif act == 'showadj':
        from DensityEstimation.Show import show_adj
        show_adj()

if __name__ == "__main__":
    sys.exit(main())