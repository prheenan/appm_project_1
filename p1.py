# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
# need to add the utilities class. Want 'home' to be platform independent
# import the patrick-specific utilities
import GenUtilities  as pGenUtil
import PlotUtilities as pPlotUtil
from scipy.stats import chi2
# where to save

# dont want to plot the PDF at 0; will distort everything 
pdfMin = 0.005

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

def plotBetween(ax,x,y,cutoff,alpha):
    alphaRegion = np.where(x >= cutoff)[0]
    xRegion = x[alphaRegion]
    yRegion = y[alphaRegion]
    plt.fill_between(xRegion,yRegion,color='r')
    arrowIdxX = int(len(xRegion)/2)
    arrowTxt = ('T_alpha={:.3g} gives\n alpha (red region)= {:.3g}')\
        .format(cutoff,alpha)
    # plot the x and y location in the middle
    arrowLocY = yRegion[arrowIdxX]
    arrowLocX = xRegion[arrowIdxX]
    yRange = float(max(y)-min(y))
    ax.annotate(arrowTxt, xy=(arrowLocX,arrowLocY),
                xytext=(arrowLocX, arrowLocY+yRange/4),
                arrowprops=dict(facecolor='red', shrink=0.05),)

def plotAlpha(outputFolder):
    end = 3.
    dof=1
    points = np.linspace(pdfMin,end,1000)
    tAlpha = chi2.ppf(0.75,dof)
    chiPdf = chi2.pdf(points,dof)
    fig = pPlotUtil.pFigure()
    ax = plt.subplot(1,1,1)
    plt.plot(points,chiPdf,'g-',label='pdf',linewidth=2)

    alpha = 1-chi2.cdf(tAlpha,dof)
    plotBetween(ax,points,chiPdf,tAlpha,alpha)

    plt.axvline(tAlpha,color='k',linestyle='--',
                label='T_alpha={:.3f}'.format(tAlpha))
    plt.title("PDF Versus Chi^2 showing T_alpha corresponding to level alpha")
    plt.xlabel("T Test Value")
    plt.ylabel("PDF Of Chi^2 with 1 degree of freedom")
    plt.legend()
    pPlotUtil.saveFigure(fig,outputFolder + "alphaLevelExample")

def plotMendel(outputFolder):
    '''
    create an array for Mendel's data
    pp 15, under:
    THE OFFSPRING OF HYBRIDS IN WHICH SEVERAL DIFFERENTIATING CHARACTERS 
    ARE ASSOCIATED.
    '''
    data = np.array( [[315.,101.],[108.,32.]] )
    numRows = data.shape[0]
    numCols = data.shape[1]
    totalN = float(np.sum(data.flatten()))
    thetaI = np.sum(data,axis=0)/totalN
    thetaJ = np.sum(data,axis=1)/totalN
    expData = np.zeros( (numRows,numCols) )
    # post: have everything we need to calculate the theta i and j values
    # just do a simple for loop now, inefficient by 2x2 matrix, no point
    # initialize the T test 
    tTest = 0
    for i in range(numRows):
        for j in range(numCols):
            expected = totalN * thetaI[i] * thetaJ[j]
            expData[j][i] = expected
            # flip [i,j] because of sum. should get 0.733 by chi2_contingency
            # from scipy.stats
            tTest+= ((data[j][i] - expected)**2 )/expected
    dof = (numRows-1) * (numCols -1)
    # go 3* the value of our t test
    points = np.linspace(pdfMin,3*tTest,1000)
    # get 1-CDF(chi^2)[T] with our dof.
    # CDF(chi^2)[T] is P(chi^2 <=T)
    # so 1-CDF(chi^2)[T] is the probability for a chi^2 to exceed our T
    pdf = chi2.pdf(points,dof)
    pValue = 1-chi2.cdf(tTest,dof)
    fig = pPlotUtil.pFigure()
    labelStr = str("T0={:.3g}, Mendel's T Test (p-value={:.3g})") \
        .format(tTest,pValue)
    plt.plot(points,pdf,'g-',linewidth=2.0,label="PDF(Chi^2_1)")
    ax = plt.subplot(1,1,1)
    plt.axvline(tTest,linestyle='--',color='k',
                label=labelStr)
    plotBetween(ax,points,pdf,tTest,pValue)

    plt.xlabel("T Test value")
    plt.ylabel("Probability density function of chi^2_1 ")
    plt.title("{:s} with {:d} degrees of freedom".format(labelStr,dof))
    plt.legend(loc='best')
    pPlotUtil.saveFigure(fig,outputFolder + "mendel")


def run():
    outputFolder = "./output_p1/"
    pGenUtil.ensureDirExists(outputFolder)
    plotAlpha(outputFolder)
    plotMendel(outputFolder)
    # plot chi^2 for reference
    plotChi(outputFolder)

    

if __name__=="__main__":
    run()

