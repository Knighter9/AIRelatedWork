import gymnasium as gym
import pickle
import matplotlib.pyplot as plt 
import numpy as np 
import random


def Q_epislon_greedy_pick_action(Q,state,epislon):
    # with prob 1-epislon choose best action indicated by Q vals. 
    # with prob epislon we explore 
    num = random.random()
    if num < (1-epislon):
        return np.argmax(Q[state])
    else: 
        return random.randint(0,5)

def qlearning_algo(alpha,gamma,epislon):
    numEpisodes = 10000
    env = gym.make("Taxi-v3")

    # create matrix to store the Q values for each state and the possible actions associated
    # 500 states and 6 actions per state so we can create 500, 6 matrix. 
    # each row will represent a state and each coloum in that row will represent a possible action
    # associtated with that state
    # on intiallization i'm gonna set everything to 0 
    Qvals = np.zeros((500,6))
    rewards = []

    for i in range(numEpisodes):
        cur_reward = 0
        # get a start state 
        cur_state, info = env.reset()
        # get the current action based on epislon gready policy
        selectedAction = Q_epislon_greedy_pick_action(Qvals,cur_state,epislon)

        while 1:
            # take the next action in the environment
            next_state, reward, terminated, truncated, info = env.step(selectedAction)
            # find the best overal action for the next_state
            next_state_select_action = np.argmax(Qvals[next_state])
            # update the Q values based on formula for Q learning. Have to find the next_state_action
            Qvals[cur_state,selectedAction] = Qvals[cur_state,selectedAction] + alpha*(reward + ((gamma*Qvals[next_state,next_state_select_action])-Qvals[cur_state,selectedAction]))
            # update the curState and Cur action and reward
            cur_state = next_state
            selectedAction = next_state_select_action
            cur_reward += reward

            # check to see if truncated or terminated and then abort loop
            if truncated or terminated: # episode is done so abort
                break
        
        rewards.append(cur_reward)
    
    env.close()
    return Qvals, rewards




def writeToPickleFiles(Qvals):
    """which contains the dictionary qlearning q vals where the keys are
    the states (encoded exactly as given by the environment) 
    and the values are dictionaries where the keys are the actions 
    and the values are the learned q values q(s, a),

    strucute will look like this
    dict = {
        1: {
            0: learned q value
            1: learned q value
            .
            . 
            . 
            5: learned q value
        }
    }

    """
    qlearning_q_vals = {}
    policy = {}
    for state in range(500):
        temp = {}
        for action in range(6):
            temp[action] = Qvals[state,action]
        
        qlearning_q_vals[state] = temp 
        policy[state] = np.argmax(Qvals[state])
    
    #print(qlearning_q_vals)

    with open("qlearning_q_vals.pickle", "wb") as fileToWrite:
        pickle.dump(qlearning_q_vals,fileToWrite)
    
    with open("qlearning_policy.pickle","wb") as fileToWrite: 
        pickle.dump(policy, fileToWrite)


def plotFigure(rewards):
    plt.figure()
    plt.plot(rewards)
    plt.xlabel("Episodes")
    plt.ylabel("Total Reward")
    plt.title("Q-learning Algo plot for hw")
    plt.legend()
    plt.savefig("qlearning_total_reward.png")


if __name__ == "__main__":
    Qvals,rewards = qlearning_algo(0.1,0.9,0.1)
    writeToPickleFiles(Qvals)
    plotFigure(rewards)
