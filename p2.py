# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
# need to add the utilities class. Want 'home' to be platform independent
from os.path import expanduser
home = expanduser("~")
# get the utilties directory (assume it lives in ~/utilities/python)
# but simple to change
path= home +"/utilities/python"
import sys
sys.path.append(path)
# import the patrick-specific utilities
import GenUtilities  as pGenUtil
import PlotUtilities as pPlotUtil

def plotBoth(rVals,haldane,kosambi):
    plt.plot(rVals,haldane,'r-',label="Haldane's mapping function")
    plt.plot(rVals,kosambi,'b--',label="Kosambi's mapping function")
    plt.xlabel("R value")
    plt.ylabel("Mapping value")
    plt.legend(loc='best')

def run(outDir = "./outputp2/"):
    pGenUtil.ensureDirExists(outDir)
    # r can only be betwene 0 and 1/2 
    maxR = 0.5
    numPoints= 1000
    # cant go exactly from [0,0.5], since we would divide by zero.
    # use a small tolerance
    tol = maxR/numPoints
    rVals = np.linspace(tol,maxR-tol,numPoints)
    
    haldane = -np.log(1-2*rVals)/2.
    kosambi = np.log((1+2*rVals)/(1-2*rVals))/4
    # plot the first 10% for small r
    smallRNum = int(numPoints/10)
    
    fig= pPlotUtil.pFigure()
    plt.subplot(3,1,1)
    plt.title("Comparison of Haldane and Kosambi mapping function.")
    # plot for all r
    plotBoth(rVals,haldane,kosambi)
    plt.subplot(3,1,2)
    smallR = rVals[:smallRNum]
    smallHal = haldane[:smallRNum]
    smallKos = kosambi[:smallRNum]
    plotBoth(smallR,smallHal,smallKos)
    plt.xlabel("R value, for small R")
    plt.subplot(3,1,3)
    diff = (smallHal-smallKos)/np.minimum(smallHal,smallKos)
    plt.plot(smallR,diff,'k--',
             label="Relative difference [0,1]")
    plt.xlabel("R value, for small R")
    plt.ylabel("Relative difference \n between Haldane and Kosambi")
    plt.legend(loc='best')
    pPlotUtil.saveFigure(fig,outDir + "CompareMaps")


if __name__=="__main__":
    run()
