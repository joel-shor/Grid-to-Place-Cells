'''
Contains the function that calculates the steady-state inhibition
for the given parameters. It is called in place of running
an ode-solver.
'''
def calc_inhib(Is, f_I, f_p,thresh):
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


if __name__ == '__main__':
    print calc_inhib([2.0,2.0,3.0],2.0,3.0,1.0)