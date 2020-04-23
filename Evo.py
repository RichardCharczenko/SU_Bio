'''
File: Evo.py
Authors: Robert Rutherford, Jeremy Bjeljac, Sam Levy, Richard Charczenko, Madeline McMahon
See: Seattle University Biology Department
'''
import re #regular expression operations
import random #generates random number from range
import sys #used to exit python
from collections import OrderedDict #implement specialized data types, OrderedDict organizes dictionary numerically
from SimClimate import Simulate_Climate #opens other module, makes new object of Simulate_Climate class
from copy import deepcopy #create new object and recursively copies values from original, any changes are not reflected in original

'''Inspired by this Snowshoe hare research: https://www.sciencenews.org/blog/wild-things/climate-change-may-be-deadly-snowshoe-haresprimary
research artile here: http://onlinelibrary.wiley.com/doi/10.1111/ele.12568/abstract?campaign=wolearlyview'''

def justNum(stringList):
    '''Takes a list of strings, converts to list of stripped ints'''
    newList=[]
    num=re.compile(r'[^\d.]+')
    for item in stringList:
        item = num.sub('',item)
        item = int(item)
        newList.append(item)
    return newList


def average(numList):
    '''returns the float average of list of numbers.  Calls: JustNUM'''
    testMe=numList[0]
    if type(testMe)==str:
        numList=justNum(numList)
    return (float(sum(numList))/len(numList))


def testInputs(carryingCapacity,years):
    '''Checks the user supplied inputs for flaws, if found returns error message(s).  If OK,
    returns none.'''
    errorLog=''
    if ((carryingCapacity%2!=0) or (carryingCapacity>1000)): #remainder divided by 2 not equal to 0
        errorLog+= "  CARRYING CAPACITY (of alleles) value must be an even integer between 2 and 1000.\n "
    if (years<1 or years>1000) :
        errorLog+= " YEARS (to  simulate) must be a integer between 1 and 1000.\n"
    if errorLog !='':
        return "SORRY, PARAMETERS NEED ADJUSTING:\n", errorLog

aliveanddead= {} #conjoined dictionary output, includes both surviving and dead alleles with counts

def calcAlleleFreqs(list):
    '''calculates the freqs of all alleles, returns a dictionary of counts'''
    dict={x:list.count(x) for x in list}
    for key in dict:
        dict[key]=float(dict[key])/len(list)
    return dict

def calcPhenoFreqs(list):
    '''calculates freq of phenotypes'''
    dict={x:list.count(x) for x in list}
    for key in dict:
        dict[key]=float(dict[key])/len(list)
    return dict

validAlleles = [2, 3, 4, 5, 8, 10, 20] #referenced by alleleDef(), contains number of alleles that CAN be tested #still not sure what used for
thatWeek = range(1, 53) #list of numbers from 1-52


def alleleDef(geneSize):
    '''If user chooses random diversity, takes the raw inputs of number of alleles to be tested and ge\
    nerates alleles with traits that correspond to which week they will change color'''
    wiki = 0
    alleles = []
    while wiki < geneSize:
        wiki += 1
        a = random.choice(thatWeek)
        if a not in alleles:
            alleles.append(a)
        else:
            wiki -= 1
    return alleles

def diversityChoice(diversityQuery, alleleQuery, weekStart):
    '''Takes the user's raw input and determines whether the user would like small, med, or random diversity.
    Calls on alleleDef(geneSize) if random is picked'''

    if diversityQuery == 'FourAllele': #RRMMM debugging
        return [15,24,26,35]

    newGenes = [] #blank list to be populated and become genePool
    if diversityQuery == 'small': #this will serve as a model for the rest of the func
        alleleQuery = weekStart
        step = alleleQuery
        list1 = thatWeek[weekStart-3:weekStart+2] #creates a list of the allele, two below it, and two above it
        won = 0
        alleles = [] #blank list for the new chosen alleles, small cluster was kept at 4 for users sake and to better simulate a random population
        while won < 4:
                won += 1
                aj = random.choice(list1) #randomly chooses from the users desired cluster
                if aj not in alleles:
                    alleles.append(aj) #adds allele to new allele list, ONLY if it isn't already in there
                else:
                    won -= 1 #if allele was already chosen by above while loop, the loop takes one step back and tries again
        return alleles #therefore alleles will have no repeats and will be a random collection around the cluster

    if diversityQuery == 'medium':
        alleleQuery = weekStart
        step = alleleQuery
        list1 = []
        if step in thatWeek and step > 5 and step < 48:
            for x in range(len(thatWeek)):
                if x == step:
                    list1 = thatWeek[x-6:x+5]
                    won = 0
                    alleles = []
                    while won < 10: #number of alleles for medium is set at 10
                        won = won + 1
                        aj = random.choice(list1)
                        if aj not in alleles:
                            alleles.append(aj)
                        else:
                            won = won - 1
                    return alleles
            newGenes = alleles
            return newGenes
        else:
            errorLog = 'Please enter a week greater than 5 and less than 48'
            sys.exit(0)
    if diversityQuery == 'random':
        newGenes = alleleDef(2)
        return newGenes
    genePool = newGenes #sets variable newGenes to global variable genePool
    return genePool

def firstFill(thisGenePool,carryingCapacity):
    '''Initially fills the genePool so that all the alleles are initially arounds the same frequency.
    Only called once at the begining of the simulation. Calls random'''
    #fills with original list of alleles, adds a random allele and repeats till carrycapacity reached, makes sure the frequencies are around the same
    missingAlleles=carryingCapacity-len(thisGenePool) #calculates 'missing alleles' of the population to be filled
    alleleIncreasingFreq = [] #list to be populated with the missing alleles
    while len(alleleIncreasingFreq) < missingAlleles: #while the list of alleles is less than the alleles missing
        z = 0 #counter and list position for below
        while z < len(thisGenePool): #indicates when the 'window' has scanned through the thisGenePool list once
            alleleIncreasingFreq.append(thisGenePool[z]) #appends whatever allele is at this position in thisGenePool[]
            z = z + 1 #increases z to next position in thisGenePool
            if len(alleleIncreasingFreq) == missingAlleles: #if the allele's added = the alleles needed, the while loop breaks
                break
        else: #only happens if while loop is false, does not occur if its broken
            ran = random.choice(thisGenePool) #when the list has been scanned through
            alleleIncreasingFreq.append(ran) #a random choice of allele is picked (random choice was used bc a lot of alleles at the 0 position of thisGenePool[] were being added
            z = 0                           #and the beginning of the list is then scanned again
    thisGenePool = thisGenePool + alleleIncreasingFreq #fills the gene pool to carrying capacity
    return thisGenePool

def fillHabitat(thisGenePool,carryingCapacity):
    '''If genePool is smaller than carrying Capacity, fill it randomly from
    genePool, return bigger genePool. Gene Frequencies may fluctuate. Calls:random'''
    if len(thisGenePool)==0:  # If gene pool empty bc all animals dead
        thisGenePool.append(15) # add a 15 to keep program from crashing: temporary fix
    missingAlleles=carryingCapacity-len(thisGenePool)
    for num in range(missingAlleles):
        alleleIncreasingFreq=random.choice(thisGenePool)
        thisGenePool.append(alleleIncreasingFreq)
    return thisGenePool

def doesAmimalSurvive(animalAve,survivalChance):
    '''Need to see if mismatch in current week, compares animalAve week to brown (phenotype)
    to week of snowout to determine survival pct. Returns the animalAve, or 0 if animal dies '''
    survivalNum=float(random.randint(1,100)/100.00) #draw a number to determine survival..
    if (survivalNum < survivalChance): #survives this week
        next # lives to next week
    elif (survivalNum >= survivalChance): #dies this week
        animalAve=0 #dead #testing
    #fyi genetic variabilty of phenotype primarily in spring. Fall seems fixed
    return animalAve

phenoList = [] #empty list

def newGeneration(genePool,carryingCapacity,weekStartGen,weekSnowsGone, selection):
    '''Does a generation of weekly selection on the list of alleles in genePool new genePool returned,
     also collects the alleles that don't survive past new generation, sized to int carrying capacity,
     if included. Week gets used for selection, if weather fluctuates.
     Calls: fillHabitat and average'''
    deadgenePool=[] #the genepool of animals that did not survive
    nextGenePool=[] #the genepool for the next generation
    while genePool:  #make and test animals from the whole genePool
        allele1=genePool.pop() #selects alleles from previous gene pool to create new animal
        allele2=genePool.pop()
        animal=(allele1,allele2)  # use the next two alleles to make an animal...
        animalAve=average(animal) # codominant : phenotype is an average of the alleles
        phenoList.append(animalAve)
        unCamoedWeeks=0
        if ((weekStartGen==18) and (selection=='yes')): # spring/summer, possible camo mismatch
            unCamoedWeeks=int(abs(animalAve-weekSnowsGone))

            for num in range(unCamoedWeeks): #for each uncamoed week
                    survivalChance=.92 # 7% less fit if mismatched color, value from experiments
                    animalAve=doesAmimalSurvive(animalAve,survivalChance)
        #For weeks when there is no chance of a camo mismatch

        week=weekStartGen+unCamoedWeeks
        for num in range(week,weekStartGen+18):  # Usually 17 weeks= (aprox 3 hare generations a year)
            survivalChance=.99  #testing value, experimenally for hares, match weekly survival is 0.96
            if (animalAve !=0): #alive
                animalAve=doesAmimalSurvive(animalAve,survivalChance)


        if animalAve !=0: #animal is alive after 17 weeks to breed
            nextGenePool.append(allele1) #if animal survives they are added to the next viable list of alleles that can be placed in new generation
            nextGenePool.append(allele2)
        else:    #animal did not survive after 17 weeks
            aliveanddead[allele1] = 0 #if animal dies they are kept in a separate allele list that is not able to be pulled from when creating the new generation
            aliveanddead[allele2] = 0
    #Use survivors to fill habitat
    if len(nextGenePool)!=0:  # Unless gene pool empty bc all animals dead, keep running new one.
        nextGenePool=fillHabitat(nextGenePool,carryingCapacity)
    return nextGenePool

def runEvo(climate, phenoList, carryingCapacity, years, diversityQuery, selection, ccount, week, alleleQuery, weekStart, outPut, chance1, chance2):
    genePool = diversityChoice(diversityQuery, alleleQuery, weekStart) #returns genes to be used based on amount of diversity wanted
    alleles = deepcopy(genePool) #makes object called alleles and copies values of gene pool into it, keeps track of alleles started with
    deadgenePool = genePool #separate gene pool with all original genotypes to keep track of when certain alleles die off, shallow copy
    genePool = firstFill(genePool, carryingCapacity) #NEED scale up alleles to fill habitat at even frequencies, first time only :)b
    '''Empty lists to be populated for use in ploting data'''
    #returns a full gene pool reflective of diversity #list
    Snowmelt=[]
    Xaxis=[]   #keep track of weeks past in simulation
    allele1=[] #empty lists for all alleles present in the population, values are recorded after every week
    allele2=[]
    allele3=[]
    allele4=[]
    allele5=[]
    Ordered={}   #the same as aliveanddead dictionary except the keys will be ordered numerically to keep track of allele changes per week

    climate_simulator = Simulate_Climate(climate, years) #create object of simulate_climate called climate_simulator
    outPut = climate_simulator.generate_climate() #calls generate_climate() function of climate_simulator object, assigns it to output

    snowWeekValues = dict.values(outPut) #returns a list of all values in the dictionary, these values represent what week each year their will be snow melt
    weekSnowCount = 0
    for year in range(1,years+1):  #every week # range is (1-20) #range doesn't include stop number #difference in year vs years
        weekSnowCount = weekSnowCount + 1
        snowCounting = weekSnowCount - 1  #for list format
        weekSnowsGone = snowWeekValues[snowCounting] #Ave week 26 July 1 for now.... but fluctuates
        for weekStartGen in (1,18,34): #These weeks start a new Generation
            random.shuffle(genePool) # Random mating simulated by shuffling: each ordered pair becomes an animal
            aliveanddead.update(calcAlleleFreqs(genePool))  #adds surviving alleles to this dictionary and calculates the frequency of each
            Ordered = OrderedDict(sorted(aliveanddead.items(), key=lambda t: t[0]))  #calls ordereddict to sort keys in aliveandead dictionary on increasing numerical order
            phenoFreq = calcPhenoFreqs(phenoList)
            OrdPheno = OrderedDict(sorted(phenoFreq.items(), key=lambda t: t[0]))
            phenoList = []

            Xaxis.append(1)   #all the possible weeks in the simulation
            Xaxis = [(x)+18 for x in Xaxis]  #gives list of the numbered weeks (at the start of each generation) for entire simulation
            allele1.append(Ordered.values()[0]) #allele1 is a list that will be populated by the first key's frequency (first genotype in the genepool dictionary)
            if len(Ordered.values()) > 1:   #allows the second allele's frequencies (and so on) over the course of the simulation be recorded in another list
                allele2.append(Ordered.values()[1])
                if len(Ordered.values()) > 2: #recordes third allele frequencies in same way as before
                    allele3.append(Ordered.values()[2])
                    if len(Ordered.values()) > 3:  #recordes fourth allele frequencies...
                        allele4.append(Ordered.values()[3])
                        if len(Ordered.values()) > 4:  #records fifth allele frequencies...
                            allele5.append(Ordered.values()[4])
                genePool=newGeneration(genePool,carryingCapacity, weekStartGen,weekSnowsGone, selection)
    graph_data = [Xaxis, snowWeekValues, allele1, allele2, allele3, allele4, allele5]
    return Xaxis, snowWeekValues, allele1, allele2, allele3, allele4, allele5, alleles

def generate_scenario(section):
    ''' There are 6 main preselected conditons Evo is known to run under and this function allows for user to simply
    input 1-6 for each scenario and then runs each scenario'''
    global aliveanddead #access dictionary outside of function scope
    aliveanddead = {} #why declare it again?
    global phenoList #access list outside of function scope
    phenoList = [] #why declare it again?

    D = {1:[600, 100, 'random', ''], 2:[100, 100, 'small', ''], 3:[100, 100,'small', '']} #not used anywhere else
    if section == 1:
        carryingCapacity = 1000 #max population
        years = 50 #max years run for
        diversityQuery = 'random'
        a = 2 #what is this?
        selection = "no" #no natural selection
        climate = "" #no climate change
    if section == 2:
        carryingCapacity = 16 #RRMM #max population
        years = 50 #RRMM #max years run for
        diversityQuery = 'small'
        selection = "no" #no natural selection
        climate = "" #no climate change
    if section == 3:
        carryingCapacity = 1000 #max population
        years = 50 #max years run for
        diversityQuery = 'small'
        selection = 'yes' #no natural selection #MM yes
        climate = "no" #no climate change
    if section == 4:
        carryingCapacity = 20 #max population
        years = 50 #max years run for
        diversityQuery = 'small'
        selection = 'yes' #natural selection occuring
        climate = "no" #climate change
    if section == 5:
        carryingCapacity = 1000 #max population
        years = 50 #max years run for
        diversityQuery = 'small'
        selection = 'yes' #natural selection occuring
        climate = "change" #climate change
    if section == 6:
        carryingCapacity = 20 #max population
        years = 50 #max years run for
        diversityQuery = 'small'
        selection = 'yes' #natural selection occuring
        climate = "change" #climate change

    genePool = [] #NEED first definition of genePool #empty list for genes in population
    alleleQuery = '' #empty string
    cChange = 0 #when is this used?
    #week1 = [21, 22, 23, 24, 25, 26, 27, 28]
    week1 = [25] #first week always set as 25
    ccount = 0
    chance1 = 10 #never used, only called upon in functions #connection to simclimate value b?
    chance2 = [11, 12, 13, 14] #find where is used #never used, only called upon in functions #connection to simclimate value b?
    outPut = {}
    weekStart = random.choice(week1) #only used when first week not set
    week = weekStart #absolute for situation
    diversityQuery = 'FourAllele' #sets alleles
    return runEvo(climate, phenoList, carryingCapacity, years, diversityQuery, selection, ccount, week, alleleQuery, weekStart, outPut, chance1, chance2)
