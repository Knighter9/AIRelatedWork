# define the reward matrices for the three games
# row player is first in the key, and column player is second in the key
import random
prisoners_dilema_reward_matrix = {
    ('testify','testify'): (1.0,1.0),
    ('testify','refuse'):(5.0,0.0),
    ('refuse','testify'): (0.0,5.0),
    ('refuse','refuse'): (3.0,3.0)
}

chicken_reward_reward_matrix = {
    ('swerve','swerve'): (3.0,3.0),
    ('swerve','straight'): (1.5,3.5),
    ('straight','swerve'): (3.5,1.5),
    ('straight','straight'): (1.0,1.0),
}

movie_coordination_reward_matrix = {
    ('action','action'): (3.0,2.0),
    ('action','comedy'): (0.0,0.0),
    ('comedy','action'): (0.0,0.0),
    ('comedy','comedy'): (2.0,3.0),
}

actions_for_games = {
    "prisoners dilema": ['testify','refuse'],
    "chicken": ['swerve','straight'],
    "movie": ['action','comedy']
}

dictOfRewardMatrices = {
    "prisoners dilema": prisoners_dilema_reward_matrix,
    "chicken": chicken_reward_reward_matrix,
    "movie": movie_coordination_reward_matrix,
}
def fictious_play(game_being_played,move_history):
    # check to see if the opponent has any moves, if not we are going to create a move strategy with a uniform distrubution
    count_availableActions = len(actions_for_games[game_being_played])
    opponent_game_strat = {}
    if not move_history:
        # create the uniform dist for opponenent strategey for all available actions
        for action in actions_for_games[game_being_played]:
            opponent_game_strat[action] = 1/(count_availableActions)
    
    else: # the opponent has a move history so compute and update strategy predction
        # the move history like [(agent move, opponent move)]
        for action in actions_for_games[game_being_played]:
            opponent_game_strat[action] = 0
        
        # count up the number of instances for each action found in move history
        for currHistory in move_history: 
            opponent_game_strat[currHistory[1]] += 1
        
        # for each action divide by length of move history to form probability dist
        for action in actions_for_games[game_being_played]:
            opponent_game_strat[action] = opponent_game_strat[action]/ len(move_history)
    
    # compute the best response action my looking at expected rewards for given action against prob dist for oponenet action and
    # select the max
    currBestReward = -1
    bestAction = "dummyVar"

    for potentialAction in actions_for_games[game_being_played]:
        rewardExpectation = 0
        for opponentAction, probabilityOfAction in opponent_game_strat.items():
            rewardExpectation += probabilityOfAction * dictOfRewardMatrices[game_being_played][(potentialAction,opponentAction)][0]
        
        if rewardExpectation>currBestReward:
            currBestReward = rewardExpectation
            bestAction = potentialAction
    
    return bestAction
        



def tit_for_tat(game_being_played, move_history):
    # if this is first move then we will cooperate
    if not move_history:
        if game_being_played == "chicken":
            return 'swerve'
        elif game_being_played == "prisoners dilema":
            return 'refuse'
        else: 
            return random.choice(['action','comedy']) # not really as determinastic for best action as the two games above so random choice
    
    else:  # play the last action by the opponent
        return move_history[-1][1]


def bully(game_being_played,move_history):
    # simply compute opponenet best action and then compute our best response to it
    bestAction = "dummyVar"
    bestActionReward = -1
    # for each possible action the bully can take, compute the opponents best response to it
    # and get the reward we get from it and then update if reward is greater than bestActionReward 
    for bullyPotentialAction in actions_for_games[game_being_played]:

        opponentAction = "dummyVar"
        opponentBestReward = -1

        for opponentResponseAction in actions_for_games[game_being_played]: 
            opponentCurReward = dictOfRewardMatrices[game_being_played][(bullyPotentialAction,opponentResponseAction)][1] # get the reward for the opponent
            if opponentCurReward > opponentBestReward: 
                opponentBestReward = opponentCurReward
                opponentAction = opponentResponseAction

        
        # we have calculated the best opponenent response to the current action so determine the reward for the bully

        bullyReward = dictOfRewardMatrices[game_being_played][(bullyPotentialAction,opponentAction)][0]

        # check to see if bullyReward is the best we have seen yet
        if bullyReward > bestActionReward:
            bestActionReward = bullyReward
            bestAction = bullyPotentialAction
    
    # return the action 
    return bestAction


# helper function for grandfather algo
def getTargetPairs(game_being_played):
    # get target pairs for the game based on if we and the opponenet get a reward better than security value
    targetPairs = []
    for potentialAction in actions_for_games[game_being_played]:
        for oppAction in actions_for_games[game_being_played]:

            playerReward = dictOfRewardMatrices[game_being_played][(potentialAction,oppAction)][0]
            oppReward = dictOfRewardMatrices[game_being_played][(potentialAction,oppAction)][1]

            if playerReward > 1 and oppReward > 1: # condition will work for all three games based on reward matrices return values
                targetPairs.append((potentialAction,oppAction))
    
    return targetPairs

def godfather(game_being_played,move_history):
    # if no move history then we simply seleect the target pair and play that
    # if move history then we check to see if opp held to their part of the deal and if they
    # don't we punish them by selecting action to minimize reward
    if not move_history: 
        # get the target pairs and play our portion of the action
        targetPairs = getTargetPairs(game_being_played)
        return targetPairs[0][0]
    
    else: 
        # check to see that the opp held up to the deal and played the action for getting target pair reward
        targetPairs = getTargetPairs(game_being_played)

        lastOppAction = move_history[-1][1]

        for targetPair in targetPairs:
            if lastOppAction == targetPair[1]:
                return targetPair[0]

        
        # the opp didn't choose an action in list of targetPairs so select best response to punish them and minimize their reward
        minAction = "dummyVar"
        minActionReward = 10000 # hardcoded threshold, suffiecent for these games as max reward is like 3.5 or something

        # loop through and see what action leads to opponents getting the min rewared, assuming opponent will try to maxmize its reward
        # essentialy we want to minmize the max reward the opponeent can get
        for potentialAction in actions_for_games[game_being_played]: 

            curOppMaxReward= -1
            for oppAction in actions_for_games[game_being_played]: 
                opp_reward = dictOfRewardMatrices[game_being_played][potentialAction,oppAction][1]

                if opp_reward > curOppMaxReward: 
                    curOppMaxReward = opp_reward
            # we have computed the maximum reward the opponenet can possibly receive for our given action
            # check to see if the maximu reward they can see is less than the minActionReward

            if curOppMaxReward < minActionReward:
                minActionReward = curOppMaxReward
                minAction = potentialAction 
        
        return minAction

agents = {
    "tit_for_tat": tit_for_tat,
    "bully": bully,
    "fictious_play": fictious_play,
    "godfather": godfather,
}
def simulate_games(agent1, agent2, game_being_played): 
    agent1ActionHistory = [] # of form [(agent1Action,agent2Actoin)]
    agent2ActionHistory = [] # of form [(agent2Action,agent1Action)]
    agent1Rewards = 0
    agent2Rewards = 0
    # rurn 100 rounds
    for i in range(100): 
        agent1Action = agent1(game_being_played,agent1ActionHistory)
        #print("agent1Action: " + str(agent1Action))
        agent2Action = agent2(game_being_played,agent2ActionHistory)
        #print("agent2Action: " + str(agent2Action))
        #print(agent1)
        #print(agent2)

        agent1Reward = dictOfRewardMatrices[game_being_played][(agent1Action,agent2Action)][0]
        agent2Reward = dictOfRewardMatrices[game_being_played][(agent1Action,agent2Action)][1]

        #print("agent1Reward: " + str(agent1Reward))
        #print("agent2Reward: " + str( agent2Reward))
        agent1Rewards += agent1Reward
        agent2Rewards += agent2Reward

        agent1ActionHistory.append((agent1Action,agent2Action))
        agent2ActionHistory.append((agent2Action,agent2Action))


    agent1avgReward = agent1Rewards/100
    agent2avgReward = agent2Rewards/100

    return (agent1avgReward,agent2avgReward)




def runSimulationForAllGames():
    # for each game do the following
        # for each agent play the game against all agents and record results (e.g nested double loop inside outer loop so triple loop)
    
    # for each game: 
        # for each agent
            # for each agent: 


    allGameResults = {}

    for game in actions_for_games.keys():
        #print("Running for the game" + str(game))

        allGameResults[game] = {}

        for agent,agentStrategyFunc in agents.items():
            allGameResults[game][agent] = {}
        
            for opp, oppStrategyFunc in agents.items():
                avg_rewards = simulate_games(agentStrategyFunc,oppStrategyFunc,game)
                allGameResults[game][agent][opp] = avg_rewards
    
    return allGameResults


def printTable(game,resultsForGame):
    agents = ["tit_for_tat", "bully", "fictious_play", "godfather"]  
    header = "                "
    for agent in agents: 
        header += agent 
        header += "        "

    print(header)

    

    for agent in agents: 
        row = ""
        resultsForAgent = resultsForGame[agent]
        row += agent 
        if agent == "bully":
            row += "        "
        elif agent =="tit_for_tat": 
            row += "  "
        
        elif agent == "godfather":
            row+= "    "
        row += "  "
        for value in resultsForAgent: 
            tupleVal = resultsForAgent[value]
            formatedTuple = f"({tupleVal[0]:.2f}, {tupleVal[1]:.2f})"
            row += formatedTuple
            row += "      "
        print(row)



if __name__ == "__main__":
    results = runSimulationForAllGames()
    for key in results.keys():
        
        print('_____________________________________')
        print("game: " + str(key))
        
        printTable(key,results[key])

        print("______________________________________")
    