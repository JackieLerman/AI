'''
HW01 Due 02172020 -  Code from Alex's Computer (I guess?)
Authors: Alexander L, Jackie L.
'''

import select
from math import *
import numpy as np
from myro import *
import cv2
import imageUtils as iu
from colorfinder import *




def takePicture():
    '''Return cv2 image object of current camera capture.'''
    v = cv2.VideoCapture(0)
    r,pic = v.read()
    v.release()
    return pic


def getObst():
    '''Returns True iff robot is stalled or
    there is an obstacle on either side.'''
    if getStall() == 1:
        print('stalled')
        return True
    L, R = getIR()
    if (L == 0 or R == 0):
        print('obst!',L,R)
        return True
    return False


def endRun():
    '''non-blocking listen for ENTER key'''
    i,o,e = select.select([sys.stdin],[],[],0)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

###############################################################################

class Behavior(object):
    '''High level class for all behaviors.  Any behavior is a
    subclass of Behavior.'''
    NO_ACTION = 0
    def __init__(self):
        self.state = None
    def check(self):
        '''Return True if this behavior wants to execute
        Return False if it does not.'''
        return False
    def run(self):
        '''Execute whatever this behavior does.'''
        return

class Avoid(Behavior):
    '''Behavior to avoid obstacles.  Simply turns away.'''
    TURN_LEFT = 1
    TURN_RIGHT = 2
    TURN_180 = 3
    BACK_TURN_180 = 4;
    IR_OBST = 0
    STALLED = 1
    def __init__(self):
        self.state = Avoid.NO_ACTION
        self.turnspeed = 0.9

    def check(self):
        '''see if there are any obstacles.  If so turn other direction'''
        # Do backup+180 ballistic motion if stalled
        if getStall() == self.STALLED:
            print("avoid: stalled")
            self.state = Avoid.BACK_TURN_180
            return True

        L, R = getIR()
        if L == self.IR_OBST:
            if R == self.IR_OBST: # obst on either size; reverse dir.
                self.state = Avoid.TURN_180
            else:
                self.state = Avoid.TURN_RIGHT
            print("avoid: obst",L,R)
            return True
        elif R == self.IR_OBST:
            self.state = Avoid.TURN_LEFT
            print("avoid: obst",L,R)
            return True
        else:
            self.state = Avoid.NO_ACTION
        return False

    def reverseDirection(self):
        '''Make 180 degree turn (approx).'''
        turnLeft(1,1.3)

    def run(self):
        '''see if there are any obstacles.  If so turn other direction'''
        print('Avoid')
        if self.state == Avoid.TURN_RIGHT:
            move(0,self.turnspeed)
        elif self.state == Avoid.TURN_LEFT:
            move(0,-self.turnspeed)
        elif self.state == Avoid.TURN_180:
            self.reverseDirection()
        elif self.state == Avoid.BACK_TURN_180:
            backward(.2,.4) # back for .4 sec (enough to clear serial wires)
            self.reverseDirection()


###############################################################################

class Wander(Behavior):
    '''Behavior to wander.  Heads in direction that varies a bit
    each time it executes.'''
    WANDER = 1
    IR_OBST = 0

    def __init__(self):
        self.state = Wander.NO_ACTION
        self.lspeed = 0.5 # speed of left motor
        self.rspeed = 0.5 # speed of right motor

    def check(self):
        '''see if there are any possible obstacles.  If not, then wander.'''

        if getObst():
            self.state = self.NO_ACTION
        else:
            self.state = self.WANDER
            return True

    def run(self):
        '''Modify current motor commands by a value in range [-0.25,0.25].
        But can we make it go faster? Hehehe... '''
        print('Wander')
        self.lspeed += 5.9 * (random.random() - 0.5)
        self.rspeed += 5.9 * (random.random() - 0.5)
        if (self.lspeed < 0 and self.rspeed < 0): #prevent backwards motion
            self.lspeed = 5.9    #random.random() MAKING LUCIUS FASTER 
            self.rspeed = 5.9    #random.random() 
        motors(self.lspeed,self.rspeed)
        wait(0.4) # guarantee some movement

        
class Scan(Behavior):
    
    
    def __init__(self):
        self.timer = 0
        self.found = False
        self.sz = 0
        self.x = 0
        self.y = 0
       
    
    def check(self):
        
        #We always want Lucius to be scanning, even when pushing obj,
        # but only once every three or so seconds.
        if self.timer == 5:
           # print(timer)
            self.timer = 0
            return True
        
        elif self.timer >= 0:
             self.timer = self.timer + 1
            # print(timer)
             return False
           
       
        
    
    def run(self):
        print("Scanning!")
        scanner = ColorFinder(True,False)

        for i in range(7):
            self.sz, self.x, self.y = scanner.findBlob(takePicture(),debug=False)
            turnLeft(5, 3.6 / 8)  # Turn 45 degrees approx.
            wait (0.5)
        
        
            if self.sz == 0: # If there is no size then no obj is found.
                self.found = False

                
            else: 
                self.found = True
                forward(7,4)
                beep(1, 880,369.994*2)
                wait(4)
                break
            
         # move forward if cone is not found at end of scan 
        if self.found == False:
            forward(3,2)
            wait(.6)
                                                     
        
    
        

'''Behavior we created intending to push cone once found. We were unable to figure
    out how to access the data we needed to make this work. Alex and I will be at
    your office soon :)'''

class Push(Behavior):

    def __init__(self):
        #Set our found boolean to T/F value of boolean in Scan(Not Working)  
        self.found = Scan().found
    
    def check(self):
       # print("CALLING PUSH CHECK")
        
   #Return true if Scan has set found to True (We found the cone!!)This is never
   #returning true. Accessing found,sz,x, and y, was our biggest challenge
    
        if self.found:
            print("RETURNED TRUE")
            return True
        else:
            return False
    
    def run(self):
       # print("PUSH SAYS" ,self.sz)
        pass

    
class Controller(object):

    def __init__(self):
        '''Create controller for object-finding robot.'''

        self.message = "empty"

        self.avoidBehavior = Avoid()
        self.wanderBehavior = Wander()
        self.scanBehavior = Scan()
        self.pushBehavior = Push()
        self.behaviors = [self.scanBehavior, self.wanderBehavior, self.avoidBehavior]

    def arbitrate(self):
        '''
        Decide which behavior, in order of priority
        has a recommendation for the robot.
        '''

        for behavior in self.behaviors:
            wantToRun = behavior.check()
            if wantToRun:
                behavior.run()
                return # no other behavior runs

    def run(self):
        while not endRun():
            self.arbitrate()
        print("End key hit")
        stop()

if __name__ == '__main__' :
    init('/dev/ttyUSB0')
    ctl = Controller()
    print(getObst())
    ctl.run()
