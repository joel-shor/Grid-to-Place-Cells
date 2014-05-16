''' Runs some sample simulations to show that
    the almost closed form solution gives the same
    output as the actual ode integrator. '''

from scipy.integrate import odeint
from matplotlib import pyplot as plt
import numpy as np
import time
import logging

from GridCells import GridNetwork
from PlaceCells import PlaceCellNetwork
from GenerateFigures.simulation_graph_funcs import _plot
from Inhibition import calc_inhib

def _calculate_asymptotic_activity(acts, f_I, f_p, thresh, calc_inhib):
    ''' Runs the fast asymptotic activity algorithm for each
        spatial point in acts. '''
    s = time.time()
    mesh_pts = acts[0].shape[0]
    final_acts = [np.zeros([mesh_pts,mesh_pts]) for _ in range(len(acts))]
    inhibs = np.zeros([mesh_pts,mesh_pts])
    for i in range(mesh_pts):
        for j in range(mesh_pts):
            yf, inhib = calc_inhib([act[i,j] for act in acts], 
                                   f_I, f_p, thresh)
            for k in range(len(acts)):
                final_acts[k][i,j] = yf[k]
            inhibs[i,j] = inhib
    logging.info('Time to calculate asymptotic: %.3f', time.time()-s)
    return final_acts, inhibs

class Param:
    '''A class that conveniently holds the parameters.'''
    modules = None
    #min_plcfld_size = .05
    min_plcfld_size = .005
    #min_grid_size = .0001
    #min_grid_size = .0004 # m**2
    min_grid_size = .001 # m**2
    C = 0.4
    thresh = 1
    f_I = 0.04/thresh
    f_p = thresh/0.005
    cell_factor = 2
    plc_cells = 15
    grd_cells = plc_cells*cell_factor

def deriv(u,t, I, f_I, f_peak, thresh):
    act = [max(0,u0) for u0 in u]
    inhib = f_I * max(f_peak*sum(act)-thresh,0)
    a = [-1*ui + Ii - inhib for ui,Ii in zip(u,I(t))]
    return a

def test_validity_of_inhib_calc():
    Param.L=Param.W=Param.H=1
    p=Param

    grid_net = GridNetwork(p.grd_cells,p.min_grid_size,p.W,p.H,p.modules)
    plc_net = PlaceCellNetwork(p.plc_cells,grid_net,wt_type='Monaco',C=p.C)
    acts = plc_net.activity()
    final_acts_calc1, _ = _calculate_asymptotic_activity(acts,p.f_I,p.f_p,p.thresh,calc_inhib)

    mesh_pts = acts[0].shape[0]
    final_acts_sim = [np.zeros([mesh_pts,mesh_pts]) for _ in range(p.plc_cells)]
    t = np.linspace(0,100,100)
    sim_time = 0
    for i in range(mesh_pts):
        for j in range(mesh_pts):
            I = lambda t: [act[i,j] for act in acts]

            der = lambda u,t: deriv(u,t,I, p.f_I,p.f_p,p.thresh)
            u0 = [0 for _ in range(p.plc_cells)]
            
            s = time.time()
            y = odeint(der, u0, t)
            sim_time += time.time()-s
            
            yf = y[-1,:]
            for k in range(p.plc_cells):
                final_acts_sim[k][i,j] = p.f_p*max(yf[k],0)
    
    logging.info('Time to run simulations: %.3f', sim_time)
    sm = np.sum([np.abs(final_acts_sim[i]-final_acts_calc1[i]) for i in range(p.plc_cells)])
    sm /= p.plc_cells*mesh_pts**2
    logging.info('Error per mesh point: %f', sm)
    X = grid_net.X; Y=grid_net.Y
    #_plot(X,Y,final_acts_sim[0],title='FINAL Activity of Plc Cell 1 from Diff Eq')
    #_plot(X,Y,final_acts_calc[0],title='FINAL Activity of Plc Cell 1 from Calculation')
    #_plot(X,Y,np.abs(final_acts_calc2[0]-final_acts_calc1[0]),title='Difference between the two')
    _plot(X,Y,np.abs(final_acts_sim[0]-final_acts_calc1[0]),title='Difference between the two')
    plt.show()

def graph(y,t):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X,Y = np.meshgrid(range(y.shape[1]), t)

    ax.plot_surface(X,Y,y)
    ax.set_xlabel('Cell Number')
    ax.set_ylabel('Time')
    ax.set_zlabel('Cell State')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_validity_of_inhib_calc()
    #run()