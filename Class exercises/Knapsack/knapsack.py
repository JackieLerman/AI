
# Example from Chapter 12 of Machine Learning: An Algorithmic
# Perspective by Stephen Marsland
# (http://seat.massey.ac.nz/personal/s.r.marsland/MLBook.html)

# You are free to use, change, or redistribute the code in any way you
# wish for non-commercial purposes, but please maintain the name of
# the original author.  This code comes with no warranty of any kind.

# Stephen Marsland, 2008


# USAGE: python3 knapsack.py easy|hard

import sys
from numpy import *
from time import time

class ksack():
    def __init__(self,prob):
        self.size = 0 # num items
        self.sizes = [ ] # list of items
        # This is easier problem; solution has size 499.98
        if prob == 'easy':
            self.size = 500
            self.sizes = array([109.60,125.48,52.16,195.55,58.67,61.87,92.95,93.14,
                                155.05,110.89,13.34,132.49,194.03,121.29,179.33,139.02,
                                198.78,192.57,81.66,128.90])
        elif prob == 'hard': # optimal is 2732
            self.size = 2732
            self.sizes = array([94,74,77,74,29,11,73,80,81,82,75,42,44,57,20,20,99,95,52,81,68,16,
                           79,30,16,90,21,49,70,78,77,21,84,19,65,38,25,43,99,75,80,10,44,26,21,
                           74,20,22,81,89,15,35,24,16,43,75,25,76,48,75,15,23,10,81,81,67,58,77,49,
                           16,65,74,14,41,74,74,17,12,95,29,75,61,59,37,75,90,17,79,15,88,76,93,
                           98,80,33,39,96,71,39,49],dtype='f')
        self.nbits = len(self.sizes)

    def fitnessfunc(self,pop):
        # inner product of each individual and sizes
        fitness = sum(self.sizes*pop,axis=1)

        # discount overlimit by twice its excess over maxSize
        fitness = where(fitness>self.size,self.size-2*(fitness-self.size),fitness)
        return fitness

def main(prob):
    '''Exhaustive search on knapsack.'''

    kprob = ksack(prob)
    best = 0
    # make a numpy array
    twos = arange(-len(kprob.sizes),0,1)
    #print('1 twos',twos)
    twos = 2.0**twos
    #print('2 twos',twos)
    for i in range(2**len(kprob.sizes)-1):
        string = remainder(floor(i*twos),2)
        fitness = sum(string*kprob.sizes)
        if fitness > best and fitness<500:
            best = fitness
            bestString = string
        if fitness == kprob.size:
            break
    return best,bestString

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('USAGE python3 easy|hard')
        sys.exit(-1)

    t0 = time()
    best,bstring = main(sys.argv[1])
    print( 'Time elapsed (sec)', time() - t0)
    print('Best',best)
    print('Best String',bstring)
