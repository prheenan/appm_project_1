# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
# need to add the utilities class. Want 'home' to be platform independent
# import the patrick-specific utilities
import GenUtilities  as pGenUtil
import PlotUtilities as pPlotUtil
from scipy.stats import chi2
# where to save

def run():
    outputFolder = "./output_p1/"
    pGenUtil.ensureDirExists(outputFolder)
    # specify which degrees of freedom to get
    dof = np.round(np.arange(0,15))
    points = np.linspace(0,20,1000)
    numPoints = len(points)
    numDof = len(dof)
    chiSq = np.zeros((numDof,numPoints))
    # fill in all the chi^2 distributions we want
    for i,df in enumerate(dof):
        chiSq[i,:] = 1-chi2.cdf(points,df)
    # plot all the chi^2 tests
    colors = pPlotUtil.colorCyc(numDof)
    fig = pPlotUtil.pFigure()
    # plot all the chi^2, label them
    for i,df in enumerate(dof):
        plt.plot(points,chiSq[i,:],color=colors[i],label="DOF: {:d}"
                 .format(int(df)))
    # get that legend / x axis!
    plt.legend(loc='best')
    plt.xlabel("T test value (T0) ")
    plt.ylabel("1-CDF(Chi^2(x)), Prob(T >= T0)")
    plt.title("Probability of Chi^2 >= T0 approaches 0 as T0 grows large")
    pPlotUtil.saveFigure(fig,outputFolder + 'chi^2')

if __name__=="main":
    run()

