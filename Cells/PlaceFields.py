'''
Created on Jun 30, 2013

A collection of static methods useful in calculating and
measuring place fields. These methods are used to calculate
the 'spatial statistics' section of the paper.
'''

import numpy as np
from scipy.sparse import csgraph as cs
from scipy.sparse import lil_matrix as lil

class PlaceField:
    @staticmethod
    def above_cutoff(act):
        ''' Returns a 2d binary array with 1 indicating
        activity above a threshold, 0 indicating below.
        
        Activities above the threshold are
        in the top 80% of activity. '''
        flds = np.zeros(act.shape)
        max_act = np.amax(act)
        if max_act == 0:
            return flds
        min_act = np.max([np.amin(act),0])
        cutoff = (max_act-min_act)*.2 + min_act
        for i in range(act.shape[0]):
            for j in range(act.shape[1]):
                flds[i,j] = 1 if act[i,j] > cutoff else 0
        return flds
    
    @staticmethod
    def representation(dat):
        ''' The average number of place fields
            per block in the spatial grid.
        
            dat = [(num_flds,layout), ...] '''
        tot = np.sum([x[1] for x in dat])
        return tot/np.product(dat[0][1].shape)
    
    @staticmethod
    def coverage(dat):
        ''' The proportion of the environment with
            at least 1 place field.
        
            dat = [(num_flds,layout), ...] '''
        tot = sum([x[1] for x in dat])
        empty = np.sum(tot != 0)
        return 1.0*empty / np.product(dat[0][1].shape)
    
    @staticmethod
    def sparsity(dat):
        ''' The fraction of place cells without
            place fields.
        
            dat = [(num_flds,layout), ...] '''
        return 1.0*sum([cell[0]==0 for cell in dat])/len(dat)
    
    @staticmethod
    def check_size(flds, W,H,min_size,mesh_p=None,fields_dat=None):
        ''' Returns the number of fields that are above the minimum size
            as well as a layout indicating the positions and identities
            of the fields and the sizes of the fields. 
            
            Finds fields by generating a 'connections' matrix that
            indicates adjacencies for active cells. 
            We call a 'connected-components' algorithm on the matrix.'''
        
        side = flds.shape[0]
        nodes = flds.shape[0]*flds.shape[1]
        
        # Create connection matrix
        connections = lil((nodes,nodes))

        for i in range(len(flds)):
            for j in range(len(flds[i])):
                if flds[i,j] != 1: continue
                for xd in [0,1]:    # This also does -1, implicitly
                    for yd in [0,1]:# This also does -1, implicitly
                        if (i+xd < side and i+xd >= 0 and j+yd < side and j+yd >= 0):
                            if flds[i+xd,j+yd] == 1:
                                connections[i*side+j,(i+xd)*side+(j+yd)] = 1
                                connections[(i+xd)*side+(j+yd),i*side+j] = 1

        # Determine connected components
        _, labels = cs.cs_graph_components(connections)

        one_node = 1.0*W*H/(mesh_p**2) #area of one node (m)
        nodes_required_for_fld = min_size/one_node
        
        # Find labels with min size
        fld_areas = []
        large_enough_flds = []
        for node_num in range(np.amax(labels)+1):
            if node_num < 0: break
            if (labels==node_num).sum() >= nodes_required_for_fld:
                large_enough_flds.append(node_num)
                fld_areas.append((labels==node_num).sum()*one_node)
        
        # Remap labels back to graph
        labels = labels.reshape([side,side])
        
        if large_enough_flds == []:
            fld_layout = np.zeros([side,side])
        else:
            fld_layout = sum([labels==component for component in large_enough_flds])

        return len(large_enough_flds), fld_layout, fld_areas