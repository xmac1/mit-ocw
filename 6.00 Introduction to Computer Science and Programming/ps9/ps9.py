# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    m = {}
    for line in inputFile:
        sli = line.strip('\n').split(',')
        m[sli[0]] = (int(sli[1]), int(sli[2]))
    return m

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return float(subInfo1[0])/float(subInfo1[1]) > float(subInfo2[0]) / float(subInfo2[1])

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    select_subs = {}

    left = maxWork
    while left > 0:
        best = None
        for name in subjects.keys():
            if name in select_subs:
                continue
            work = subjects.get(name)[1]
            if (best == None or comparator(subjects[name], subjects[best])) and work <= left:
                best = name
        if best == None or subjects[best][1] > left:
            break
        select_subs[best] = subjects[best]
        left = left - subjects[best][1]
    return select_subs



#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    validSubs = {}
    nameList = subjects.keys()
    allList = power(nameList, [], [])
    invalidList = []
    for selectList in allList:
        totalWork = 0
        for name in selectList:
            totalWork += subjects[name][1]
        if totalWork > maxWork:
            invalidList.append(selectList)
    for l in invalidList:
        allList.remove(l)
    bestValue = 0
    bestChoice = None
    for l in allList:
        value = 0
        for name in l:
            value += subjects[name][0]
        if value > bestValue:
            bestChoice = l
            bestValue = value
    m = {}
    for name in bestChoice:
        m[name] = subjects[name]
    return m
        

def power(nameList, validList, ret):
    if len(nameList) <= 0:
        if len(validList) == 0:
            ret.append([])
        return ret
    x = validList[:]
    x.append(nameList[0])
    ret.append(x)
    power(nameList[1:], x, ret)
    power(nameList[1:], validList, ret)
    return ret


def testPower():
    ret = power([1, 2, 3], [], [])
    print ret


if __name__ == '__main__':
    testPower()