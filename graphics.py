import matplotlib.pyplot as plt
import membershipFunctions as membFuncts


def draw_graph():
    # Setting a domain field.
    xaxis = {'xmin': 2002, 'xmax': 2012}

    # Creating the values for the domain of all our membership functions.
    xrange = membFuncts.getAxisValues(xaxis, 0.1)

    # Functions information
    trianglePoints = {'a': 2002, 'b': 2002, 'c': 2007}

    """
    
    pendingPoints = {'a': 3, 'b': 11}
    linealPoints = {'a': -4, 'b': 3}
    
    trapezoidalPoints = {'a': -5, 'b': -2, 'c': 6, 'd': 8}
    generalizedBellData = {'width': 4, 'slope': 2, 'center': 0}
    gaussianData = {'mean': 2, 'sigma': 3}
    """
    # Obtaining the graph values of each membership function.

    triangleFunction = membFuncts.triangleFunction(trianglePoints, xrange)
    triangleFunction_2 = membFuncts.triangleFunction({'a': 2002, 'b': 2007, 'c': 2012}, xrange)

    """
    pendingFunction = membFuncts.linearFunction(pendingPoints, xrange)
    linealFunction = membFuncts.linearFunction(linealPoints, xrange)
    
    trapezoidalFunction = membFuncts.trapezoidalFunction(trapezoidalPoints, xrange)
    generalizedBellFunction = membFuncts.generalizedBellFunction(generalizedBellData, xrange)
    gaussianFunction = membFuncts.gaussianFunction(gaussianData, xrange)   
    """

    # Setting the graphs grid size.
    fig, axs = plt.subplots(1, figsize=(10, 6), sharey=True)

    axs.plot(xrange, triangleFunction, 'gold')
    axs.plot(xrange, triangleFunction_2, 'red')
    """
    axs[0, 0].plot(xrange, pendingFunction,         'red'       )
    axs[0, 1].plot(xrange, linealFunction,          'orange'    )
    
    axs[1, 1].plot(xrange, trapezoidalFunction,     'green'     )
    axs[0, 2].plot(xrange, generalizedBellFunction, 'blue'      )
    axs[1, 2].plot(xrange, gaussianFunction,        'indigo'    )
    """

    # Setting titles for each subplot.
    axs.title.set_text('Triangle')
    """
    axs[0, 0].title.set_text('Pending')
    axs[0, 1].title.set_text('Linear')
    
    axs[1, 1].title.set_text('Trapezoidal')
    axs[0, 2].title.set_text('Generalize Bell')
    axs[1, 2].title.set_text('Gauss')
    
    """

    # Setting the main title
    """   
    plt.suptitle('Membership functions')"""

    # Show us what you got!
    """"  
    plt.show()
    """
    return fig, plt


draw_graph()
