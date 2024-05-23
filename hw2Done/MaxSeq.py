import numpy as np

# create the transition matrix
T = np.array([[0.7,0.3],[0.4,0.6]])
#create the sensor matrix 
E = np.array([[0.9,0.1],[0.3,0.7]])


def MLEALGO(ObservationList,length):
    TransitionMatrix = np.array([[0.7,0.3],[0.4,0.6]])
    EmissionMatrix = np.array([[0.9,0.1],[0.3,0.7]])
    states = [0,1]
    intialProbs = [0.5,0.5]
    
    # intialize the tables
    v_tbl = np.zeros((len(states),len(ObservationList)))
    pointer_tbl = np.zeros((len(states),len(ObservationList)),dtype=int)

    # set up probs for starting states
    for i in range(len(states)):
        v_tbl[i,0] = intialProbs[i] * EmissionMatrix[i,ObservationList[0]]

    # construct probs for non starting states
    for i in range(1, len(ObservationList)):
        for j in range(len(states)):
            # find max value: 
            curMaxval = -1
            curIndex = 0
            for m in range(len(states)): 
                val = v_tbl[m,i-1] * TransitionMatrix[m,j] * EmissionMatrix[j,ObservationList[i]]
                if val > curMaxval:
                    curMaxval = val
                    curIndex = m
            
            v_tbl[j,i] = curMaxval
            pointer_tbl[j,i] = curIndex 

    # construct path from the best value found in pointer, work backwards
    path = []

    curMaxval = -1
    curIndex = 0
    for i in range(len(states)):
        val = v_tbl[i,len(ObservationList)-1]
        if val > curMaxval: 
            curMaxval = val 
            curIndex = i 
    for i in range(len(ObservationList)-1, -1, -1): 
        path.insert(0,states[curIndex])
        curIndex= pointer_tbl[curIndex,i]
    

    return path


if __name__ == "__main__":
    O1 = [0,1,0,1,0,1,0,1,0,1]
    O2 = [0,0,0,1,1,1,1,0,0,0]
    print(MLEALGO(O1,10))
    print(MLEALGO(O2,10))
