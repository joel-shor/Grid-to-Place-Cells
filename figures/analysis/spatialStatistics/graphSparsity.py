

def generate_graphs_for_spatial_statistics(main, sub, y_unit):


    runs = 32
    modes = None
    # Load data from network1 network
    network1 = []
    for room_len in [1,2,3,4,5]:
        network1.append(load(runs,modes,500,room_len,main,sub))

    # Load data from network2 network
    network2 = []
    for room_len in [1,2,3]:
        network2.append(load(runs,modes,1500,room_len,main,sub))

    graph_shit(network1, network2, main.capitalize()+': '+sub, y_unit)

    # If looking at sparsity, plot expected exponential curve
    if sub == 'Sparsity':
        graph_expected_sparsity()
        plt.legend(loc='upper right')
    if main == 'units' and sub == 'Coverage':
        linereggsion(network1,network2, main,sub)
    if sub == 'Number of fields':
        linereggsion(network1,network2, main,sub)
    if sub == 'Area':
        linereggsion(network1,network2, main,sub)

def exponential(x,lambduh):
            return np.exp(-1*lambduh*x)

def graph_sparsity(xs, ):
    ''' Graph the curve expected by a Poisson distribution. '''

    # These values are calculated from the best Poisson fit in
    #  generate graph of poissonparameter regression and errors.py
    y1 = exponential(x, 0.272347)
    y2 = exponential(x, 0.524838)
    plt.plot(x,y1,'--k')
    plt.plot(x,y2,'--k')

                            ('maps', 'Sparsity', 'Proportion'),
                            ('maps', 'Coverage', 'Proportion'),
                            ('maps', 'Representation', 'Fields'),
                            ('fields','Area','Field Area (m$^2$)')]:
        generate_graphs_for_spatial_statistics(main, sub, y_unit)


