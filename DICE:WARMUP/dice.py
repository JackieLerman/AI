# In the game of high-low, a pair of fair dice are rolled. The outcome is

# high if the sum is 8, 9, 10, 11, or 12.
# low if the sum is 2, 3, 4, 5, or 6
# seven if the sum is 7

# Add a Dice class that has a constructor which allows the user to
# create any number of dice.  The Dice class has a roll function that
# rolls each die and returns the sum of their upward-facing pips.

# Write a main function that simulates 1000 rolls of two dice using
# your Dice class.  Determine and print the frequency of high, low,
# and seven.

import random

class Die(object):
    def __init__(self,num=None):
        if num == None:
            self.pips = random.randint(1,6)
        else:
            self.pips = num

    def getPips(self):
        return self.pips

    def roll(self):
        '''roll once, return rnum in {1,...,6}.'''
        self.pips = random.randint(1,6)
        return self.pips

# Model a bunch of dice.
class Dice(object):
    def __init__(self,num):
        self.num = num
        self.dice = [ ]
        for i in range(num):
            self.dice.append( Die() )

    def roll(self):
        sum = 0
        for i in range(len(self.dice)):
            sum += self.dice[i].roll()
        return sum

def main():
    dice = Dice(2)
    numHi,numLow,num7 = 0,0,0

    for i in range(1000):
        value = dice.roll()
        if value == 7:
            num7 += 1
        elif value >= 2 and value <= 6:
            numLow += 1
        else:
            numHi += 1

    print('Low %d Seven %d High %d' % (numLow,num7,numHi))


# If dice.py is called as a standalone program, run main.
if __name__ == '__main__':
    main()
