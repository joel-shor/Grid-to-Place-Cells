'''
Created on Jun 1, 2014

@author: jshor
'''
from util.autoassign import autoassign

class Param:
    '''A class that conveniently holds the parameters.'''
    @autoassign
    def __init__(self, W=None, **args):
        self.L = self.H = W

    def validate(self):
        assert hasattr(self,'modules') # Assert that it exists, but it could be None
        assert self.min_plcfld_size is not None
        assert self.min_grid_size is not None
        assert self.C is not None
        assert self.thresh is not None
        assert self.plc_cells is not None
        assert self.grd_cells is not None
        assert self.f_I is not None
        assert self.thresh is not None
        assert self.L
        assert self.W
        assert self.H