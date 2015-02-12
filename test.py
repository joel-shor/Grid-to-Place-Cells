from util.autoassign import autoassign
class A:
    @autoassign
    def __init__(self, x=None, **args):
        pass

x = A(y=2,z=3)
import pdb; pdb.set_trace()