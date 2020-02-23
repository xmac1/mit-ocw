import random

def throwCoin():
    if random.random() > 0.5:
        return 'H'
    else:
        return 'T'

def simCoin(numTrials, numThrows):
    results = {}
    for n in range(numTrials):
        l = []
        for t in range(numThrows):
            l.append(throwCoin())
        t = tuple(l)
        results[t] = results.get(t, 0) + 1
    return results

numTrials = 100000
results = simCoin(numTrials, 3)
print '{H, H, H} probability: ', float(results[('H', 'H', 'H')]) / float(numTrials)
print '{H, T, H} probability: ', float(results[('H', 'T', 'H')]) / float(numTrials)
