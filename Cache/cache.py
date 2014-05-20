'''
Created on Apr 20, 2014

@author: jshor
'''
from os import listdir
from os.path import join, dirname, abspath
import hashlib
import cPickle

cache_loc = abspath(join(dirname(__file__),'cache'))

def _hash_args(args):
    h = hashlib.sha224()
    for arg in args:
        h.update(cPickle.dumps(arg))
    return h.hexdigest()

def try_cache(*args):

    fn = _hash_args(args)

    cached_items = [f for f in listdir(cache_loc)]

    try:
        if fn in cached_items:
            with open(join(cache_loc,fn),'r') as f:
                return cPickle.load(f)
        else:
            return None
    except: # If the file is there but corrupted
        return None

def store_in_cache(*args):
    ''' Last arg is what to store. '''
    fn = _hash_args(args[:-1])
    with open(join(cache_loc,fn),'w') as f:
        cPickle.dump(args[-1],f)

def add(adat, CLname, animal, session, cl_name, bin_size, label, K, correct_dp):
    '''
    all_dat{CLname: 
                animal: 
                    session: 
                        cl_prof_name: 
                            bin_size: 
                                label: 
                                    K:
                                        correct_dp}
                                        '''
    if CLname not in adat: adat[CLname] = {}
    if animal not in adat[CLname]: adat[CLname][animal]={}
    if session not in adat[CLname][animal]: adat[CLname][animal][session] = {}
    if cl_name not in adat[CLname][animal][session]: adat[CLname][animal][session][cl_name]={}
    if bin_size not in adat[CLname][animal][session][cl_name]: adat[CLname][animal][session][cl_name][bin_size] = {}
    if label not in adat[CLname][animal][session][cl_name][bin_size]: adat[CLname][animal][session][cl_name][bin_size][label] = {}
    adat[CLname][animal][session][cl_name][bin_size][label][K] = correct_dp 
    
    
def get(adat, CLname, animal, session, cl_name, bin_size, label, K):
    try:
        return adat[CLname][animal][session][cl_name][bin_size][label][K]
    except:
        return None

def clean_cache():
    okay = [_hash_args('Good trials'),
            _hash_args((5, [[-60,60],[-60,60]], 'Inside mask')),
            _hash_args((5, [[-55,55],[-55,55]], 'Inside mask')),
            _hash_args('One big data structure for 6 folds'),
            _hash_args()]
    
    
    
