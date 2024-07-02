

    
#definitely can make better with more classes and stuff. shouldp rob make an action class

#actions is a dictionary from state to set of available actions, nad each action is of the form (cost, probsChanger,nameOfAction) where probsChanger is a dictionary from children node to probability distributions on their states
#onesteps map list of list of value,prob tuples to number.


#posStates is the possbile states any node can take
#state represents ones current state, never actually really gets used though
#children represent a list of the children node.
#actions reoresent the actions, they are in the form of above. 
#oneStep is a function that maps a list(list(tuple)) to a number
class Node:
    def __init__(self, posStates, children, actions, oneStep, label):
        self.posStates=posStates
        #self.state=state
        self.children = children
        self.actions=actions
        self.oneStep = oneStep
        self.label= label
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
                    
                    
                    lister.append((vChildren[i][state],action[1][self.children[i]][state]))
                valueProbslists.append(lister)
            #value based on probability distribution
            value = self.oneStep(valueProbslists) + cost
            if value < bestValue:
                bestValue = value
                bestAction = action
        return bestAction, bestValue
    #returns what the v of this node is, as well as thr optimal policy from here on out.
    def getVAMe(self):
        actionSeq = {}
        if not self.children:
            returner = {}
            actionRet = {}
            for state in self.posStates:
                
                bestVal = 1000000
                for action in self.actions[state]:
                    if action[0] < bestVal:
                        bestVal = action[0]
                        actionRet[state] = action[2]
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
                actionRet[state] = act[2]
                valueReturner[state] = val

            actionSeq[self] = actionRet
            return valueReturner, actionSeq

#actions is a dictionary from state to available actions, nad each action is of the form (cost, probsChanger) where probsChanger is a dictionary from children node to probability distributions on their states
#onesteps map list of list of value,prob tuples to number.
        
posStates = {'1','2'}
children = []
actions = {}
actions['1']=[(100,{},"ji")]
actions['2']=[(6,{},"hi")]



def jointProb(lister):
    if len(lister) == 1:
        return lister[0]
    if len(lister) == 2:
        jointProb = []
        for i in range(0, len(lister[0])):
            for j in range(0,len(lister[1])):
                
                jointProb.append((lister[0][i][0]+lister[1][j][0],lister[0][i][1]*lister[1][j][1]))
        return jointProb
    else:
        holder = lister[0]
        inputer = [lister[0],jointProb(lister[1:])]
        return jointProb(inputer)
    






def cvarOfSum(lister, alpha = .1):
    print("at CVAR")
    #construct total probs and costs.
    #print(lister)
    listUse = jointProb(lister)
    #print(listUse)
    jointDist = sorted(listUse, key=lambda x: -x[0])
    wAve = 0
    totalProb = 0
    for i in range(0, len(jointDist)):
        if totalProb < alpha:
            weight = jointDist[i][1]
            if (totalProb + weight) < alpha:
                wAve = wAve + weight*jointDist[i][0]
                totalProb = totalProb + weight
            else:
                wAve = wAve + jointDist[i][0]* (alpha-totalProb)
                totalProb = alpha
                break
    return wAve * (1.0/alpha)


node1 = Node(posStates, children, actions, cvarOfSum, "1")

node3 = Node(posStates, children, actions, cvarOfSum, "3")

actions2 = {}
actions2['1']=[(100,{node3: {'1':.75, '2':.25}},"hello")]
actions2['2']=[(10,{node3: {'1':.75, '2':.25}},"hello")]

node2 = Node(posStates, [node3], actions2, cvarOfSum, "2")

actions0 = {}
actions0['1']=[(10,{node1: {'1':.75, '2':.25}, node2: {'1':.25, '2':.75}},"act"),(69,{node1: {'1':.1, '2':.9}, node2: {'1':.1, '2':.9}},"fact")]
actions0['2']=[(11,{node1: {'1':.25, '2':.75}, node2: {'1':.25, '2':.75}},"ji")]

node0 = Node(posStates, [node1, node2], actions0, cvarOfSum, "0")




val, act = node0.getVAMe()
print(val)


#prints polciy
for key in act.keys():
    print(key.label + ", " + str(act[key]))
#print(noder.getVAMe()[0])














    
    
    
        
                
            







        

