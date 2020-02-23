# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import matplotlib.pyplot as plt
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {__DRUG__:False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException
        
        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException

        child_res = {}
        for key in self.resistances.keys():
            if random.random() < self.mutProb:
                child_res[key] = not self.resistances[key]
            else:
                child_res[key] = self.resistances[key]
        
        return ResistantVirus(self.maxBirthProb, self.clearProb, child_res, self.mutProb)

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.drugs = []
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        numPop = 0
        for virus in self.viruses:
            flag = False
            for drug in drugResist:
                flag = False
                if virus.resistances.get(drug, False):
                    flag = True
                else:
                    break
            if flag:
                numPop += 1
        return numPop
                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        density = self.popDensity
        dieList = []
        for virus in self.viruses:
            if virus.doesClear():
                dieList.append(virus)
        for virus in dieList:
            self.viruses.remove(virus)
        childViruses = []
        for virus in self.viruses:
            try:
                offspring = virus.reproduce(density, self.getPrescriptions())
            except NoChildException as identifier:
                pass
            else:
                childViruses.append(offspring)
        self.viruses.extend(childViruses)
        self.popDensity = float(self.getTotalPop()) / float(self.maxPop)
        return len(self.viruses)

        


#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    dataTotal = {}
    dataResist = {}
    numTrials = 50
    for t in range(numTrials):
        t = simOneTrial(0, 150, {__DRUG_GUTTAGONOL__: False})
        for key in t[0].keys():
            dataTotal[key] = dataTotal.get(key, 0) + t[0][key]
        for key in t[1].keys():
            dataResist[key] = dataResist.get(key, 0) + t[1][key]
    for key in dataTotal.keys():
        dataTotal[key] = float(dataTotal[key]) / float(numTrials)
    for key in dataResist.keys():
        dataResist[key] = float(dataResist[key]) / float(numTrials)
    
    x = range(1, 0+150+1)
    y = [dataTotal[i] for i in x]
    plt.plot(x, y, 'b', label='total population')
    y = [dataResist[i] for i in x]
    plt.plot(x, y, 'b:', label='resist population')
    plt.xlabel('times/steps')
    plt.ylabel('virus populaton')
    plt.suptitle('viruses population for steps')
    plt.legend()
    plt.show()
    
__DRUG_GUTTAGONOL__ = 'guttagonol'
__DRUG_GRIMPEX__ = 'grimpex'
def simOneTrial(stepBeforeDrug, stepAfterDrug, resistances):
    viruses = []
    popTotal = []
    popResist = []
    for i in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, resistances, 0.005))
    patient = Patient(viruses, 1000)
    for t in range(stepBeforeDrug):
        popTotal.append(patient.update())
        popResist.append(patient.getResistPop([__DRUG_GUTTAGONOL__]))
    patient.addPrescription(__DRUG_GUTTAGONOL__)
    for t in range(stepAfterDrug):
        popTotal.append(patient.update())
        popResist.append(patient.getResistPop([__DRUG_GUTTAGONOL__]))
    mPop = {}
    mResist = {}
    i = 1
    for n in popTotal:
        mPop[i] = n
        i += 1
    i = 1
    for n in popResist:
        mResist[i] = n
        i += 1
    return (mPop, mResist)


#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    stepAfterDrug = 150
    numTrials = 100
    i = 1
    for stepBeforeDrug in [300, 150, 75, 0]:
        vals = []
        for t in range(numTrials):
            m = simOneTrial(stepBeforeDrug, stepAfterDrug, {__DRUG_GUTTAGONOL__: False})
            popDict = m[0]
            popFinal = popDict[stepBeforeDrug+stepAfterDrug]
            vals.append(popFinal)
        plt.subplot(2, 2, i)
        plt.hist(vals)
        plt.suptitle(str(stepBeforeDrug) + ' steps delay drug administration')
        plt.legend()
        i += 1
    
    plt.show()
#
# PROBLEM 4
#

def simOneTrial2(stepBeforeDrug1, stepBeforeDrug2, stepAfterDrug, resistances):
    viruses = []
    popTotal = []
    popResist = []
    drugList = [__DRUG_GUTTAGONOL__, __DRUG_GRIMPEX__]
    numTotal = 0
    for i in range(100):
        viruses.append(ResistantVirus(0.1, 0.05, resistances, 0.005))
    patient = Patient(viruses, 1000)
    for t in range(stepBeforeDrug1):
        numTotal = patient.update()
    patient.addPrescription(__DRUG_GUTTAGONOL__)
    for t in range(stepBeforeDrug2):
        numTotal = patient.update()
    patient.addPrescription(__DRUG_GRIMPEX__)
    for t in range(stepAfterDrug):
        numTotal = patient.update()
    return numTotal

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    stepBeforeDrug1 = 150
    stepAfterDrug = 150
    numTrials = 100
    i = 1
    for stepBeforeDrug2 in [300, 150, 75, 0]:
        vals = []
        for t in range(numTrials):
            total = simOneTrial2(stepBeforeDrug1, stepBeforeDrug2, stepAfterDrug, {__DRUG_GUTTAGONOL__: False, __DRUG_GRIMPEX__: False})
            vals.append(total)
        plt.subplot(2, 2, i)
        plt.hist(vals)
        plt.legend()
        i += 1
    
    plt.show()

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    runSim(100, 150, 0, 150)


def runSim(numTrials, stepBeforeDrug1, stepBeforeDrug2, stepAfterDrug):
    drugList = [__DRUG_GUTTAGONOL__, __DRUG_GRIMPEX__]
    resistances = {__DRUG_GRIMPEX__: False, __DRUG_GUTTAGONOL__: False}
    popTotal = {}
    popResistToGut = {}
    popResistToGrim = {}
    popResistBoth = {}
    def f():
        popTotal[count] = popTotal.get(count, 0) +  patient.update()
        popResistToGut[count] = popResistToGut.get(count, 0) +  patient.getResistPop([__DRUG_GUTTAGONOL__])
        popResistToGrim[count] = popResistToGrim.get(count, 0) +  patient.getResistPop([__DRUG_GRIMPEX__])
        popResistBoth[count] = popResistBoth.get(count, 0) +  patient.getResistPop(drugList)

    for t in range(numTrials):
        viruses = []
        count = 1

        for i in range(100):
            viruses.append(ResistantVirus(0.1, 0.05, resistances, 0.005))
        patient = Patient(viruses, 1000)
        for i in range(stepBeforeDrug1):
            f()
            count += 1
        patient.addPrescription(__DRUG_GUTTAGONOL__)
        for i in range(stepBeforeDrug2):
            f()
            count += 1
        patient.addPrescription(__DRUG_GRIMPEX__)
        for i in range(stepAfterDrug):
            f()
            count += 1
    x = range(1, stepBeforeDrug1+stepBeforeDrug2+stepAfterDrug+1)
    yTotal = [float(popTotal[i]) / float(numTrials) for i in x]
    yResistGut = [float(popResistToGut[i]) / float(numTrials) for i in x]
    yResistGrim = [float(popResistToGrim[i]) / float(numTrials) for i in x]
    yResistBoth = [float(popResistBoth[i]) / float(numTrials) for i in x]
    print len(yTotal), len(yResistGut), len(yResistGrim),len(yResistBoth)
    plt.plot(x, yTotal, '1', label='population of total virus')
    plt.plot(x, yResistGut, '2', label='population of virus resistent to guttagonol')
    plt.plot(x, yResistGrim, '-', label='population of virus resistent to grimpex')
    plt.plot(x, yResistBoth, '.', label='poplulation fo virus resisten to both drug')
    plt.xlabel('time/step')
    plt.ylabel('population of virus')
    plt.suptitle('virus population dynamics with drug')
    plt.legend()
    plt.show()





# simulationDelayedTreatment()
# simulationWithDrug()
# simulationTwoDrugsDelayedTreatment()
simulationTwoDrugsVirusPopulations()