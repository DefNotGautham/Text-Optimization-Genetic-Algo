import numpy as np
import string
import random
import math
import time

class Object:
    def __init__(self, length):
        self.score = 0.0
        self.length = length
        self.genes = []
        self.mutateFlag = False
    
    def newChar(self):
        return "".join(random.choice(string.ascii_letters + " "))

    def geneCoder(self):
        for i in range(0,self.length):
            self.genes.append(self.newChar())


    def fitnessMeas(self,target):
        scr = 0
        for i in range(0,len(self.genes)):
            if self.genes[i]==target[i]:
                scr+=1
        self.score = scr/len(target)
        return scr/len(target)

    def crossOver(self,partner):
        baccha = Object(len(self.genes))
        slicePoint = np.floor(random.randint(0,len(self.genes)))
        for i in range(0,len(self.genes)):
            if i>slicePoint:
                baccha.genes.append(self.genes[i])
            else:
                baccha.genes.append(partner.genes[i])
        return baccha

    def mutate(self,mut_rate):
        for i in range(0,len(self.genes)):
            if random.uniform(0,1) < mut_rate:
                self.genes[i] = self.newChar()
                self.mutateFlag = True






class Population:
    def __init__(self, target, mut_rate, maxPop):
        self.maxPop = maxPop
        self.mut_rate = mut_rate
        self.target = target

        self.population = []
        self.popGenecode = []
        self.matepool = []
        self.fitnessArr = []
        self.prevPopulation = []
        self.generation = 0
        self.finishState = False
        self.fittestPopElement = []

        self.fittest = 0
        self.normFitness = [] 

    def populationInit(self):
        for i in range(0,self.maxPop):
            ob = Object(len(self.target))
            ob.geneCoder()
            self.population.append(ob)
            self.popGenecode.append(ob.genes)
    
    def fitnessChk(self):
        #fitn = []
        for i in range(len(self.population)):
            self.fitnessArr.append(self.population[i].fitnessMeas(self.target))

    
    def selectionProc(self):
        self.fittest = 0.0
        for i in range(0,len(self.target)):
            if self.population[i].score>self.fittest:
                self.fittest = self.population[i].score
                self.fittestPopElement = self.population[i].genes
        
        lower = 0
        upper = 1
        #TO BE TESTED self.population[i].score VAL
        for i in range(0,len(self.population)):
            normFit = math.floor((lower + (upper - lower) * self.population[i].score**2)*100)
            for j in range(0,normFit):
                self.matepool.append(self.population[i])

    def sexytime(self):
        try:
            for i in range(0,len(self.population)):
                index_a = math.floor( random.randint(1,len(self.matepool)) )
                index_b = math.floor( random.randint(1,len(self.matepool)) )
                partner_a = self.matepool[index_a-1]
                partner_b = self.matepool[index_b-1]
                child = partner_a.crossOver(partner_b)
                child.mutate(self.mut_rate)
                self.population[i] = child
        except Exception as e:
            print("Error occured : {}\nindex a : {}\nindex b : {}\n len(matepool) : {}\n".format(e,index_a, index_b, len(self.matepool)))
    
    def finishCheck(self):
        if self.fittest == 1:
            self.finishState=True


def stringSlice(test_str):
    res_first, res_second = test_str[:len(test_str)//2], test_str[len(test_str)//2:] 
  
# printing result  
    print("The first part of string : " + res_first) 
    print("The second part of string : " + res_second)


def mainfun():
    
    target = str(input("Enter String to mutate into : "))
    popMax = 200
    mutRate = 0.01

    pop = Population(target,mutRate,popMax)
    pop.populationInit()
    t1 = time.time()
    while True:
        pop.fitnessChk()
        pop.selectionProc()
        pop.sexytime()
        pop.finishCheck()
        print("population is : {}, with fitness : {}\n".format("".join([el for el in pop.fittestPopElement]),pop.fittest))
        tt = time.time()
        if tt-t1>35:
            print("Time limit reached")
            break
        if pop.finishState==True:
            t2 = time.time()
            print("Optimal Evolution found in {} s".format(t2-t1))
            break
    

stringSlice("gauthamjs")
