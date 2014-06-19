'''
maps = {'Sparsity':[],
            'Coverage':[],
            'Representation':[]}
units = {'Number of fields':[],
         'Coverage':[]}
fields = {'Area':[]}

'''

import cPickle
from os import listdir
from os.path import join


def load_new(modes, plc_cells, size, grd_cells, *args):
    folder = 'Results/New'
    filename = 'exp results size%s,modes%s,plccells%d,grdcells%i'%(str(size),
                                                        str(modes),
                                                        plc_cells,
                                                        grd_cells)
    num_flds = []
    for fn in [x for x in listdir(folder) if x.find(filename) > -1]:
        with open(join(folder,fn),'r') as f:
            txt = f.read()
        
        dat = cPickle.loads(txt)
        cur_num_flds = dat['units']['Number of fields']
        assert len(cur_num_flds) == plc_cells
        num_flds.extend(cur_num_flds)
    
    return num_flds

def load_old(modes, plc_cells, size, grd_cells, runs):
    filename = 'Results/Old/exp results size%s,modes%s,plccells%d,runs%d'%(str(size),
                                                            str(modes),
                                                            plc_cells,
                                                            runs)
    with open(filename,'r') as f:
        txt = f.read()
    
    dat = cPickle.loads(txt)
    
    num_flds = dat['units']['Number of fields']
    
    assert len(num_flds) == runs*plc_cells
    
    return num_flds
