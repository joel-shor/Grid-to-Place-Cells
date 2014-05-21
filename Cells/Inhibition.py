'''
Contains the function that calculates the steady-state inhibition
for the given parameters. It is called in place of running
an ode-solver.
'''
import numpy as np

def inhib(Is, f_I, f_p,thresh):
    '''This is called a lot. Make it tight.
    
        Is is a list of inputs to place cells.
        f_I is the inhibition strength.
        f_p is the firing strength
        thresh is the threshold for inhibition to kick in.
    '''
    if f_p*sum([max(I,0) for I in Is]) < thresh:
        return [f_p*max(I,0) for I in Is], 0
    I_ordered = sorted(Is)  # Add 0 to cover the case when
                                # all Is end up greater than 0
    Iplussum = sum(I_ordered)
    for i in range(0,len(I_ordered)):
        Nplus = len(I_ordered)-i
        inhib = f_I * ((f_p*Iplussum-thresh)/(1+f_I*Nplus*f_p))
        if I_ordered[i]-inhib >= 0:
            break
        Iplussum -= I_ordered[i]
    return [f_p*max(I-inhib,0) for I in Is], inhib

def asymptotic_inhib(acts, f_I, f_p, thresh):
    ''' Runs the fast asymptotic activity algorithm for each
        spatial point in acts. '''
    mesh_pts = acts.shape[1]
    final_acts = np.zeros([acts.shape[0],mesh_pts,mesh_pts])
    #final_acts = [np.zeros([mesh_pts,mesh_pts]) for _ in range(len(acts))]
    inhibs = np.zeros([mesh_pts,mesh_pts])
    for i in range(mesh_pts):
        for j in range(mesh_pts):
            yf, inh = inhib(acts[:,i,j], f_I, f_p, thresh)
            final_acts[:,i,j] = yf
            inhibs[i,j] = inh
    return final_acts, inhibs

if __name__ == '__main__':
    # Check speed of Inhibition
    import logging
    from PlaceCells import PlaceNetwork
    from GridCells import GridNetwork
    logging.basicConfig(level=logging.INFO)
    from time import time as tm
    thresh = 1
    f_I = 0.04/thresh
    f_p = thresh/0.005
    
    
    GridN = 1000
    PlaceN = 500
    min_grid_size = .0001
    W=H=1
    k = GridNetwork(GridN, min_grid_size,W,H)
    j = PlaceNetwork(PlaceN,k,'Monaco updated',.4)
    acts = j.activity()
    s = tm()
    for _ in range(2):
        asymptotic_inhib(acts, f_I, f_p, thresh)
    logging.info('Time for inhibs:\t%.3f',tm()-s)