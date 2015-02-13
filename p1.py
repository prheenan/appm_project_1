# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
# need to add the utilities class. Want 'home' to be platform independent
# import the patrick-specific utilities
import GenUtilities  as pGenUtil
import PlotUtilities as pPlotUtil
from scipy.stats import chi2
# where to save

def plotChi(outputFolder,label="chi^2"):
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
    pPlotUtil.saveFigure(fig,outputFolder + label)

def run():
    outputFolder = "./output_p1/"
    pGenUtil.ensureDirExists(outputFolder)
    # plot chi^2 for reference
    #plotChi(outputFolder)
    '''
    create an array for Mendel's data
    pp 15, under:
    THE OFFSPRING OF HYBRIDS IN WHICH SEVERAL DIFFERENTIATING CHARACTERS 
    ARE ASSOCIATED.
    '''
    data = np.array( [[315.,101.],[108.,32.]] )
    totalN = float(np.sum(data.flatten()))
    thetaI = np.sum(data,axis=0)/totalN
    thetaJ = np.sum(data,axis=1)/totalN
    # post: have everything we need to calculate the theta i and j values
    # just do a simple for loop now, inefficient by 2x2 matrix, no point
    numRows = data.shape[0]
    numCols = data.shape[1]
    # initialize the T test 
    tTest = 0
    for i in range(numRows):
        for j in range(numCols):
            expected = totalN * thetaI[i] * thetaJ[j]
            tTest+= ((data[i][j] - expected)**2 )/expected
    dof = (numRows-1) * (numCols -1)
    # go 3* the value of our t test
    points = np.linspace(0,3*tTest,1000)
    # get 1-CDF(chi^2)[T] with our dof.
    # CDF(chi^2)[T] is P(chi^2 <=T)
    # so 1-CDF(chi^2)[T] is the probability for a chi^2 to exceed our T
    probExceed = 1-chi2.cdf(points,dof)
    pValue = 1-chi2.cdf(tTest,dof)
    fig = pPlotUtil.pFigure()
    labelStr = str("T0={:.3g}, Mendel's T Test (p-value={:.3g})") \
        .format(tTest,pValue)
    plt.plot(points,probExceed,'r-',label="P(Chi^2_[k-1] >= T)")
    plt.axvline(tTest,linestyle='--',color='k',
                label=labelStr)
    plt.axhline(pValue,linestyle='--',color='k')
    plt.xlabel("T Test value")
    plt.ylabel("Probability for chi^2 with dof specified to exceed T")
    plt.title("{:s} with {:d} degrees of freedom".format(labelStr,dof))
    plt.legend(loc='best')
    pPlotUtil.saveFigure(fig,outputFolder + "mendel")
    

if __name__=="__main__":
    run()

