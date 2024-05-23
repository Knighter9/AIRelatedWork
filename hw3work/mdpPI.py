import random

'''
    Here is an important assumption that I am making. I am assuming that all actions are valid for every state. 
    so for example it is a totally valid action to try and move up from state (1,3), I will just ensure that 
    in this envirnemnt if that action is taken the robot will actually just remain in the given state like hitting a wall
    
    - Another example would be the user choosing to go left when in state (3,2). This might create an odd bug where
    the optimal move would actually be to go left at this state and hope that the robot actually moves to the right with prob 0.1 so we 
    get closer to the terminal state

    - I am going to be explicit and write out what actions do for each state 
'''

# create a set of states 
states = [(1,1),(1,2),(1,3),(2,1),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3)]
term_states = [(4,2),(4,3)] # no action can be done with these states so won't have to worry about them
actions = ["up","down","left","right"]


def rewardForState(currState,nextState,non_terminal_state_reward_value):
    if nextState not in term_states:
        return non_terminal_state_reward_value
    elif nextState == (4,2):
        return -1
    elif nextState == (4,3):
        return 1

def computePossibleStatesForAction(currentState, action): 
    # assuming a non terminal state
    actionState = (0,0)
    leftSlipState = (0,0)
    rightSlipState = (0,0)
    if action == "up": 
        actionState = (currentState[0], currentState[1] + 1) # go up 
        leftSlipState = (currentState[0]-1,currentState[1]) # go left 
        rightSlipState = (currentState[0]+1,currentState[1]) # go right
    elif action == "left": 
        actionState = (currentState[0] -1, currentState[1]) # go left
        leftSlipState = (currentState[0],currentState[1]-1) # go down
        rightSlipState = (currentState[0],currentState[1]+1) # go up
    elif action == "right":
        actionState = (currentState[0] + 1, currentState[1]) # go right
        leftSlipState = (currentState[0],currentState[1]+1) # go up
        rightSlipState = (currentState[0],currentState[1]-1) # go down
    else: # action must be down
        actionState = (currentState[0], currentState[1]-1) # go down
        leftSlipState = (currentState[0]+1,currentState[1]) # go right
        rightSlipState = (currentState[0]-1,currentState[1]) # go left

    return [actionState, leftSlipState,rightSlipState]

def checkValidStates(currentState,lst_of_future_states):
    newList = []
    for state in lst_of_future_states: 
        if state not in states: 
            newList.append(currentState) 
        else: 
            newList.append(state)

    return newList
       
def transitionModel(currentState,action):
    # check to see if the currentState is the terminal state, in this case we can't ever leave terminal states so just return probability as 100%
    if currentState in term_states:
        return [(currentState, 1)]

    # getStates from possible actions
    lst_of_states = computePossibleStatesForAction(currentState,action) # of form [actionstate, leftSLip,rightSlip]

    # pass the list of states to helper function to update if they are not valid states
    lst_of_valid_states = checkValidStates(currentState, lst_of_states)

    # return the lst of states with probailites
    return [(lst_of_valid_states[0],0.8), (lst_of_valid_states[1],0.1),(lst_of_valid_states[2],0.1)]
    
    
value = {}
policy = {}


for state in states: 
    value[state] = 0

for state in states: 
    if state not in term_states: 
        policy[state] = actions[random.choice([0,1,2,3])]

def setValueToZero():
    for state in states: 
        value[state] = 0

def randomPolicyIntiation():
    for state in states: 
        if state not in term_states: 
            policy[state] = actions[random.choice([0,1,2,3])]



def policyIteration(reward,discount): 
    '''
    general outline for the algorithm
    while not converged: 
        1. Run policy evaluation for all the states
        2. Run policy improvemnt for all the states with a one step lookahead

    '''
    setValueToZero()
    randomPolicyIntiation()
    convergenceValue = 0.00001
    while 1: 
        # 1. policy evalution phase
        while 1: 
            change = 0
            for state in states: 
                # get the current value for the state
                currValue = value[state]
                # get the current action for the state specified by the policy
                action = "right"
                if state not in term_states: 
                    action = policy[state]
                # loop through and use the update equation to calculate values for one ply lookahead
                calculatedValue = 0
                for nextState, probability in transitionModel(state, action): 
                    calculatedValue += probability * (rewardForState(state,nextState,reward) + discount* value[nextState])
                # update the value for the state
                value[state] = calculatedValue
                # determine to see if we can move on to policy improvement
                change = max(change, abs(currValue-value[state]))
                
            if change < convergenceValue: 
                break
        
        # 2.) policy improvement phase
        polyDone = True 
        for state in states: 
            if state not in term_states: 
                # get the current action specfied by the policy
                policyAction = policy[state]
                # create a list to store all the possible actions values
                actionVals = []
                # calculate the excpected reward for each action and store in the actionVals list
                for action in actions: 
                    rewardVal = 0
                    for nextState, probability in transitionModel(state, action): 
                        rewardVal += probability * (rewardForState(state,nextState,reward) + discount* value[nextState])
                
                    actionVals.append(rewardVal)

                # get the best argument by looking at max value in the action Vals and update the policy
                maxVal = actionVals[0]
                index = 0
                for i in range(len(actionVals)): 
                    if actionVals[i] > maxVal: 
                        maxVal = actionVals[i]
                        index = i

                # update the policy
                policy[state] = actions[index]

                # check to see if the policy actually updated and set polyDone accordinly
                if policy[state] != policyAction: # the policy was updated so set polyDone to false
                    polyDone = False
            
        if polyDone: 
            break











if __name__ == "__main__": 
    print('----------------------------------------------------')
    print("output for policy iteration with params (-2, 0.9)")
    policyIteration(-2,0.9)
    for state in states: 
        if state not in term_states: 
            print(f"State: {state}, val: {value[state]}, policy: {policy[state]}")
        else: 
             print(f"State: {state}, val: {value[state]}, policy: NO POLICY For TERM States")
    print('----------------------------------------------------')


    print('----------------------------------------------------')
    print("output for policy iteration with params (-0.2, 0.9)")
    policyIteration(-0.2,0.9)
    for state in states: 
        if state not in term_states: 
            print(f"State: {state}, val: {value[state]}, policy: {policy[state]}")
        else: 
             print(f"State: {state}, val: {value[state]}, policy: NO POLICY For TERM States")
    print('----------------------------------------------------')

    print('----------------------------------------------------')
    print("output for policy iteration with params (-0.01, 0.9)")
    policyIteration(-0.01,0.9)
    for state in states: 
        if state not in term_states: 
            print(f"State: {state}, val: {value[state]}, policy: {policy[state]}")
        else: 
             print(f"State: {state}, val: {value[state]}, policy: NO POLICY For TERM States")
    print('----------------------------------------------------')




    