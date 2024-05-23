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

def computeNextState(currentState, action): 
    # assuming a non terminal state
    actionState = (0,0)
    if action == "up": 
        actionState = (currentState[0], currentState[1] + 1) # go up 
    elif action == "left": 
        actionState = (currentState[0] -1, currentState[1]) # go left
    elif action == "right":
        actionState = (currentState[0] + 1, currentState[1]) # go right
    else: # action must be down
        actionState = (currentState[0], currentState[1]-1) # go down
    
    return actionState

def generateNextState(currentState,nextState): 
    if nextState not in states: 
        return currentState
    else: return nextState
       

def createEpisode(policy, intialState, epislon,non_terminal_state_reward_value):
    statesVistedinEpisode = []
    currState = intialState
    # loop until we have reached a terminal state
    while currState not in term_states: 
        # get the action probabilites based on the policy so far
        actionProbabilities = policy[currState]
        # select the action based on their probabilities
        action = random.choices(actions,actionProbabilities)[0]
        # check to see the next state
        potentialNextState = computeNextState(currState,action)
        # get the next steate
        nextState = generateNextState(currState,potentialNextState) # checks to see if next state is out of bounds
        # get the reward
        reward = rewardForState(currState,nextState, non_terminal_state_reward_value)

        statesVistedinEpisode.append((currState,action,reward))

        # update the currState
        currState = nextState
    
    # return the episode
    return statesVistedinEpisode


 

def monteCarloFirstVisitEpislonSoft(reward, discount, epislon): 
    # need to do some basic intialization
    # 1. intialize policy
    # 2. intialize action value func Q
    numEpisodes = 111111
    policy = {}
    QFunc = {}
    returns = {}
    # setting up random policy, each action gets uniform dist of being chosen
    for state in states: 
        if state not in term_states: 
            policy[state] = []
            for action in actions: 
                policy[state].append(1/len(actions))
        
    # setting QFunc values to 0 for all st, At pairs
    # setting the empty list for returns for all st,At pairs
    for state in states: 
        for action in actions: 
            QFunc[(state,action)] = 0
            returns[(state,action)] = []

    
    # now implement the actual algorithm 
    for i in range(numEpisodes): # looping forever until convergene
        # need to generate an episode from the start state until it reaches a terminal state 
        episode = createEpisode(policy,(1,1),epislon,reward)
        # set G = 0
        G = 0
        visited = []
        # loop for each episode, but do it in reverse
        for index, (currState, currAction, rewardVal) in enumerate(episode[::-1]): 
            #updat the value of G using the equatino
            G = discount * G + rewardVal
            # check to see if this is the first occurence of the state action pair st, at
            # that check to see if st,at not in s0,a0 .... st-1, at-1. 
            if (currState,currAction) not in [(state,action) for (state,action,rewardVal) in episode[:index]]:
                #print('This is running')
                # append G to the returns for this current state
                returns[(currState,currAction)].append(G)
                # update the Q Func. Q(s,a) = average(returns(s,a))
                QFunc[(currState,currAction)] = (sum(returns[(currState,currAction)])/len(returns[(currState,currAction)]))
                # selection the action 
                # get the current best action for the state
                maxVal = QFunc[(currState,currAction)]
                bestAction = currAction
                for action in actions: 
                    if QFunc[(currState,action)] > maxVal: 
                        bestAction = action
                        maxVal = QFunc[(currState,action)]
                
                # update the policy
                # best action gets probability 1-epislon + epislon/len(actions)
                # all other actions get probablilty epislon/len(actions)

                # loop through each index of the actions and update the policy
                if currState not in term_states: 
                    for i in range(len(actions)): 
                        if actions[i] == bestAction: 
                            policy[currState][i] = 1- epislon + (epislon/len(actions))
                        else: 
                            policy[currState][i] = (epislon/len(actions))
                
    return policy, QFunc

    
    


if __name__ == "__main__": 
    print('----------------------------------------------------')
    print("output for monte carlo with params (-2, 0.9, and 0.1)")
    policy,QFunc = monteCarloFirstVisitEpislonSoft(-2,0.9,0.1)
    print("state:             action-values q(s,a),           policy")
    for state in policy: 
        maxIndex = 0
        maxVal = 0
        for i in range(len(policy[state])): 
            if(policy[state][i]) > maxVal: 
                maxVal = policy[state][i]
                maxIndex = i


    
        
        print(f"{state}: up={QFunc[(state,'up')]}, down={QFunc[(state,'down')]}, left={QFunc[(state,'left')]}, right={QFunc[(state,'right')]}  policy={actions[maxIndex]}")
    print('----------------------------------------------------')

    print('----------------------------------------------------')
    print("output for monte carlo with params (-0.2, 0.9, and 0.1)")
    policy,QFunc = monteCarloFirstVisitEpislonSoft(-0.2,0.9,0.1)
    print("state:             action-values q(s,a),           policy")
    for state in policy: 
        maxIndex = 0
        maxVal = 0
        for i in range(len(policy[state])): 
            if(policy[state][i]) > maxVal: 
                maxVal = policy[state][i]
                maxIndex = i


    
        
        print(f"{state}: up={QFunc[(state,'up')]}, down={QFunc[(state,'down')]}, left={QFunc[(state,'left')]}, right={QFunc[(state,'right')]}  policy={actions[maxIndex]}")

    print('----------------------------------------------------')

    print('----------------------------------------------------')
    print("output for monte carlo with params (-0.01, 0.9, and 0.1)")
    policy,QFunc = monteCarloFirstVisitEpislonSoft(-0.01,0.9,0.1)
    print("state:             action-values q(s,a),           policy")
    for state in policy: 
        maxIndex = 0
        maxVal = 0
        for i in range(len(policy[state])): 
            if(policy[state][i]) > maxVal: 
                maxVal = policy[state][i]
                maxIndex = i


    
        
        print(f"{state}: up={QFunc[(state,'up')]}, down={QFunc[(state,'down')]}, left={QFunc[(state,'left')]}, right={QFunc[(state,'right')]}  policy={actions[maxIndex]}")

    print('----------------------------------------------------')
   
   
   