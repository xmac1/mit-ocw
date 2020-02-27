import matplotlib.pylab as pylab
import random

def minkowsikiDist(v1, v2, p):
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    return dist**(1.0/p)


class Example(object):
    def __init__(self, name, features, label=None):
        self.name = name
        self.features = features
        self.label = label
    def dimensionality(self):
        return len(self.features)
    def getFeatures(self):
        return self.features
    def getLabel(self):
        return self.label
    def getName(self):
        return self.name
    def distance(self, other):
        return minkowsikiDist(self.features, other.features, 2)
    def __str__(self):
        return self.name + ":" + str(self.features) + ":" + str(self.label)

class Cluster(object):
    def __init__(self, examples, exampleType):
        self.examples = examples
        self.exampleType = exampleType
        self.centroid = self.computeCentroid()

    def update(self, examples):
        oldCentroid = self.centroid
        self.examples = examples
        if len(examples) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
        else:
            return 0.0

    def members(self):
        for e in self.examples:
            yield e
    
    def size(self):
        return len(self.examples)
    
    def getCentroid(self):
        return self.centroid

    def computeCentroid(self):
        dim = self.examples[0].dimensionality()
        totVals = pylab.array([0.0]*dim)
        for e in self.examples:
            totVals += e.getFeatures()
        centroid = self.exampleType('centroid', totVals / float(len(self.examples)))
        return centroid
    
    def variance(self):
        totDist = 0.0
        for e in self.examples:
            totDist += (e.distance(self.centroid)) ** 2
        return totDist ** 0.5
    
    def __str__(self):
        names = []
        for e in self.examples:
            names.append(e.getName())
        names.sort()
        result = 'Cluster with centroid '\
            + str(self.centroid.getFeatures()) + ' contains:\n '
        for e in names:
            result = result + e + ', '
        return result[:-2]

def kmeans(examples, exampleType, k, verbose):
    initialCentroids = random.sample(examples, k)

    clusters = []
    for e in initialCentroids:
        clusters.append(Cluster([e], exampleType))
    
    converged = False
    numIteration = 0
    while not converged:
        numIteration += 1

        newClusters = []
        for i in range(k):
            newClusters.append([])

        for e in examples:
            smallestDistance = e.distance(clusters[0].getCentroid())
            index = 0
            for i in range(1, k):
                distance = e.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index  = i
            newClusters[index].append(e)

        converged = True
        for i in range(len(clusters)):
            if clusters[i].update(newClusters[i]) > 0.0:
                converged = False
        if verbose:
            print 'Iteration #' + str(numIteration)
            for c in clusters:
                print c
            print ' '
    return clusters

def dissimilarity(clusters):
    totDist = 0.0
    for c in clusters:
        totDist += c.variance()
    return totDist

def tryKeams(examples, exampleType, numClusters, numTrials, verbose = False):
    best = kmeans(examples, exampleType, numClusters, verbose)
    minDissimilarity = dissimilarity(best)
    for trial in range(1, numTrials):
        clusters = kmeans(examples, exampleType, numClusters, verbose)
        curDissimilarity = dissimilarity(clusters)
        if curDissimilarity < minDissimilarity:
            minDissimilarity = curDissimilarity
            best = clusters
    return best

def genDistribution(xMean, xSD, yMean, ySD, n, namePrefix):
    samples = []
    for s in range(n):
        x = random.gauss(xMean, xSD)
        y = random.gauss(yMean, ySD)
        samples.append(Example(namePrefix + str(s), [x, y]))
    return samples

def plotSamples(samples, marker):
    xVals, yVals = [], []
    pylab.figure(1)
    for s in samples:
        x = s.getFeatures()[0]
        y = s.getFeatures()[1]
        pylab.annotate(s.getName(), xy=(x, y),
        xytext=(x+0.13, y-0.07), 
        fontsize='x-large')
        xVals.append(x)
        yVals.append(y)
    pylab.plot(xVals, yVals, marker)

def contrivedTest(numTrials, k, verbose):
    random.seed(0)
    xMean = 3
    xSD = 1
    yMean = 5
    ySD = 1
    n = 10
    d1Samples = genDistribution(xMean, xSD, yMean, ySD, n, '1.')
    plotSamples(d1Samples, 'b^')
    d2Samples = genDistribution(xMean+3, xSD, yMean+1, ySD, n, '2.')
    plotSamples(d2Samples, 'ro')
    clusters = tryKeams(d1Samples + d2Samples, Example, k, numTrials, verbose)
    pylab.show()
    print 'Finl result'
    for c in clusters:
        print '', c

contrivedTest(1, 2, True)