import numpy as np
from knapsack import *
from time import time
# Author: S. Anderson

class ga:
    '''Implement simplest genetic algorithm with bitstrings, mutation and
    single-point crossover.
    '''
    def __init__(self,stringLen,fitnessFunc,nEpochs,popSize,mutationProb):
        self.stringLen = stringLen
        # force popsize to be even
        if popSize % 2 == 1:
            raise exception("Population size must be even.")
        self.popSize = popSize
        if mutationProb < 0:
            raise exception("Mutation must be non-negative.")
        self.mutationProb = mutationProb
        self.nEpochs = nEpochs
        self.fitnessFunc = fitnessFunc
        # create random bitstrings
        self.pop = np.random.rand(self.popSize,self.stringLen)
        self.pop = np.where(self.pop<0.5,0,1) # less than 0.5 -> 0, ge 0.5 -> 1
        #print('pop',self.pop)

    def run(self,useCrossover=True,useMutation=True):
        '''Runs num epochs of selection/crossover/mutation'''
        best = np.zeros(self.nEpochs)
        oldmax = 0
        for i in range(self.nEpochs):
            # compute pop fitness
            fitness = self.fitnessFunc(self.pop) # eval(self.fitnessFunc)(self.pop)
            # keep copy of best
            idx = np.argmax(fitness)
            fittest = np.array(self.pop[idx])
            # pick parents
            newpop = self.select(self.pop,fitness)

            if useCrossover:
                newpop = self.crossover(newpop)
            if useMutation:
                newpop = self.mutate(newpop)

            newpop[0] = fittest # replace first with fittest individual
            best[i] = fitness.max()
            if i > 0 and (best[i] != best[i-1]):
                print(i,fitness.max())
            self.pop = newpop
        pass

    def rouletteSelect(self,cumprob):
        '''From pop choose a new individual based
        on probabilities reprsented in bins.'''
        r = np.random.random()
        for i, cp in enumerate(cumprob):
            if r < cp: return i

    def select(self,pop,fitness):
        '''
        pop: np array of bitstrings
        fitness: np array of fitness values, one for each member of pop
        Return new population with size of pop in which the number of copies of
        a string in pop depend on fitness.
        '''
        newpop = np.zeros((self.popSize,self.stringLen))
        if (np.min(fitness) < 0):
            fitness = fitness - np.min(fitness)
        if np.sum(fitness) == 0: # if all zero, set to share probability
            for i in range(len(fitness)):
                fitness[i] = 1.0/len(fitness)

        fitness = fitness / np.sum(fitness)  # percentage

        cumProb = np.cumsum(fitness) # cummulative sum
        #print('cum prob',cumProb)
        for i in range(len(fitness)):
            choice = self.rouletteSelect(cumProb)

            newpop[i] = pop[choice]
        return newpop

    def crossover(self,pop):
        '''Implement one point crossover of adjacent bitstrings.'''
        newpop = np.zeros(np.shape(pop))
        crossoverPoint = np.random.randint(0,self.stringLen,self.popSize)
        # Selection is random, so just grabbing adjacent pairs is OK.
        for i in range(0,self.popSize,2):
            newpop[i,:crossoverPoint[i]] = pop[i,:crossoverPoint[i]]
            newpop[i+1,:crossoverPoint[i]] = pop[i+1,:crossoverPoint[i]]
            newpop[i,crossoverPoint[i]:] = pop[i+1,crossoverPoint[i]:]
            newpop[i+1,crossoverPoint[i]:] = pop[i,crossoverPoint[i]:]
        return newpop

    def mutate(self,pop):
        '''Flip random bits in bitstrings.'''
        mutPts = np.random.rand(np.shape(pop)[0],np.shape(pop)[1])
        pop[np.where(mutPts < self.mutationProb)] = 1 - pop[np.where(mutPts < self.mutationProb)]
        return pop

def main():
    ''' Apply to knapsack problem.'''
    if len(sys.argv) != 2:
        print('USAGE python3 easy|hard')
        sys.exit(-1)

    kprob = ksack(sys.argv[1])
    gaProb = ga(stringLen=kprob.nbits,fitnessFunc=kprob.fitnessfunc,
                nEpochs=1000,popSize=200,mutationProb=0.5)
    gaProb.run(useCrossover=False,useMutation=True)


if __name__ == "__main__":
    t0 = time()
    main()
    print( 'Time elapsed (sec)', time() - t0)
