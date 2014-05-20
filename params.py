'''
Created on May 19, 2014

@author: jshor
'''

class Param:
    '''A class that conveniently holds the parameters.'''
    
    @classmethod
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