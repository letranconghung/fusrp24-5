

    


#actions is a dictionary from state to available actions, nad each action is of the form (cost, probsChanger) where probsChanger is a dictionary from children node to probability distributions on their states
#onesteps map list of list of value,prob tuples to number.


#posStates is the possbile states any node can take
#state represents ones current state, never actually really gets used though
#children represent a list of the children node.
#actions reoresent the actions, they are in the form of above. 
#oneStep is a function that maps a list(list(tuple)) to a number
class Node:
    def __init__(self, posStates, state, children, actions, oneStep):
        self.posStates=posStates
        self.state=state
        self.children = children
        self.actions=actions
        self.oneStep = oneStep
                        #vChildren is a lsit of the v's of the children, as a function of the childs state
    
    #computes the best action given current state, and given the v's of the children
    def bestActionValue(self,state, vChildren):

        #should add a if no chuildren section to this, except should never get called

        #initiation values
        bestAction = self.actions[state][0]
        bestValue = 10000000000

        #finds best action given current state
        for action in self.actions[state]:
            cost = action[0]

            #will be tuples of probabilities and actions
            valueProbslists = []

            #computes the probability disctribution of the each the vChildren for the action.
            for i in range(0,len(self.children)):
                lister=[]
                probSeq = action[1]
                for state in self.posStates:
                    lister.append((vChildren[i](state),action[1][state]))
                valueProbslists.append(lister)
            #value based on probability distribution
            value = self.oneStep(valueProbslists)
            if value < bestValue:
                bestValue = value
                bestAction = action
        return bestAction, bestValue
    #returns what the v of this node is, as well as thr optimal policy from here on out.
    def getVAMe(self):
        actionSeq = {}
        if self.children.empty():
            returner = {}
            actionRet = {}
            for state in self.posStates:
                
                bestVal = 1000000
                for action in self.actions[state]:
                    if action[0] < bestVal:
                        bestVal = action[0]
                        actionRet[state] = action
                returner[state] = bestVal
            actionSeq[self] = actionRet
            return returner, actionSeq
        else:
            actionRet = {}
            vChildren = []
            valueReturner = {} 
            for i in range(0,len(self.children)):
                vChild, actChild = self.children[i].getVAMe()
                actionSeq.update(actChild)
                vChildren.append(vChild)
            for state in self.posStates:
                
                act, val = self.bestActionValue(state,vChildren)
                actionRet[state] = act
                valueReturner[state] = val

            actionSeq[self] = actionRet
            return valueReturner, actionSeq


        





    
    
    
        
                
            







        

