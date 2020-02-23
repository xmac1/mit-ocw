import random
import statistics

def throwNeedles(numNeedles):
    inCircle = 0
    for needles in range(1, numNeedles+1):
        x = random.random()
        y = random.random()
        if (x**2 + y **2) ** 0.5 <= 1.0:
            inCircle += 1
    return 4*(inCircle/float(numNeedles))

def getEst(numNeedles, numTrials):
    estimate = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles)
        estimate.append(piGuess)
    sDev = statistics.stdev(estimate)
    curEst = sum(estimate) / len(estimate)
    print 'Est. = ' + str(curEst) \
        + ' Std. dev. = ' + str(round(sDev, 6)) \
        + ', Needles = '+ str(numNeedles)
    return (curEst, sDev)

def estPi(precison, numTrials):
    numNeedles = 1000
    sDev = precison
    while sDev  >= precison / 2.0:
        curEst, sDev = getEst(numNeedles, numTrials)
        numNeedles *= 2
    return curEst

estPi(0.001, 100)