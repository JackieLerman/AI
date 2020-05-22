'''
   Solves the generalized Tower of Hanoi using forms of AI search.
   Date: 02/28/2020
   Name: Jackie Lerman 
'''

from search import *


class HanoiProblem(Problem):
    '''
    Class to solve the M disk, K stack Hanoi problem.
    '''

    def __init__(self, initialstate, goal):
        '''initialstate is the starting state'''
        Problem.__init__(self, initialstate)
        self.goal = list(goal)
        
        


    def goal_test(self,state):
        self.state = state
        
        if self.state == self.goal:
            return True
        else:
            return False

    def result(self,state,action):
        '''
        Returns state that results from act.
        returned state is completely independent of state
        '''
        #print("StateAtStart", state)
        stateaslist = list(state)
        new_state = state #Set new state to current state if unable to take action
        
       # print(stateaslist)
        #Nested loops to check all possible pairs that could be swapped as action
        
        if action == "AtoB":
        #Loop to run through number of rods 
            for i in range (len(stateaslist)):
                 # Loop to run through number of disks on first rod which should be all disks 
                for x in range (len(list(stateaslist[0]))):
                    roda = list(stateaslist[x])
                
                    if x == len(stateaslist)-1:
                        rodb =  list(stateaslist[x-1])
                    else:
                        rodb = list(stateaslist[x+1])
                        #print("LENGTH",len(rodb))

                        if  len(roda)>0 and len(rodb) == 0:
                            new_state = rodb.append(roda.pop())
                            exit
                    
                        elif len(roda)==0 and len(rodb) > 0:
                           new_state = tuple(new_state)
                            
                        elif len(roda)==0 and len(rodb)==0:
                           
                            new_state = state
                          
                
                        elif roda[0] < rodb[0]:
                            new_state = rodb.append(roda.pop())

                       # print("A:", roda, "B:", rodb)
                       
                        
        if action == "BtoA":
            # Loop to run through number of disks on first rod which should be all disks 
            for i in range (len(stateaslist)):
                #Loop to run through number of rods 
                for x in range (len(list(stateaslist[0]))):
                    roda = list(stateaslist[x])
                
                    if x == len(stateaslist)-1:
                        rodb =  list(stateaslist[x-1])
                    else:
                        rodb = list(stateaslist[x+1])
                        #print("LENGTH",len(rodb))

                        if  len(roda)>0 and len(rodb) == 0:
                           exit
                    
                        elif len(roda)==0 and len(rodb) > 0:
                            new_state = roda.append(rodb.pop())
                            
                            
                        elif len(roda)==0 and len(rodb)==0:
                            exit  
                
                        elif roda[0] > rodb[0]:
                            new_state = roda.append(rodb.pop())

                       # print("A:", roda, "B:", rodb)
        
                        
                
        new_state = tuple(stateaslist)
        #print("StateAtEnd",state)     
        return new_state 

    def actions(self, statestr):
        '''
        List of actions executable from state.
        '''
        actionlist = ["AtoB", "BtoA"] 
                
        return actionlist
    
    def h(self,state,goal):
        #Simple heuristic which equals twice the number of disks on initial rod, not yet on
        #The last rod 
        statesaslist = list(state)
        rodalength = len(list(stateaslist[0]))
        lastrodlength = stateslist[len(statesaslist)]
        # If goal is found, nummoves should be zero 
        if state == goal:
            nummoves = 0
        #Otherwise, nummoves should equal twice the number of disks on starting stack minus number
        #of disks on last rod  
        else:
            if rodalength == 0:
                nummoves =0
                
            else:
                nummoves = 2*rodalength - lastrodlength 

        return nummoves

    
        


def printProb(searchtype,p):
    print(searchtype,end="\t")
    print("NActions %d\tNgoaltests %d\tNstates %d\tGoalState %s" %
          (p.succs,p.goal_tests,p.states,p.found) )
    print()


if __name__ == '__main__':
    initstate =  ((3,2,1), (), (),)  
    goalstate = ((), (), (3,2,1))
    hp = HanoiProblem(initstate,goalstate)
    p = InstrumentedProblem(hp)

    if len(sys.argv) == 1 or sys.argv[1] == 'bfs':
        breadth_first_graph_search(p)
        printProb('BFS',p)
    else:
        astar_search(p,hp.h)
        printProb('Astar',p)
