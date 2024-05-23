import numpy as np 


def create_observations_matrices(observations):
    observationsMatrices = []
    for i in range(len(observations)):
        if observations[i]: # the observation is true
            O = np.array([[0.9,0],[0,0.3]])
            observationsMatrices.append(O)
        else: # the observation is false
            O = np.array([[0.1,0],[0,0.7]])
            observationsMatrices.append(O)
    
    return observationsMatrices 

def forward_backward(observations, evidenceLength): 
    # create the transition matrix
    T = np.array([[0.7,0.3],[0.4,0.6]])
    observations= create_observations_matrices(observations)
    prior = [0.5, 0.5]
    # follow psuedocode from book
    b = np.array([1,1])
    fv = list(range(len(observations) + 1))
    fv[0] = np.array(prior)
    sv = list(range(len(observations) + 1))

    for i in range(1,len(observations)+1): 
        fv[i] = observations[i-1] @ np.transpose(T) @ fv[i-1]

    for i in range((len(observations)),0,-1):
        vec = fv[i] * b
        normalizedVec = vec/vec.sum()
        sv[i] = normalizedVec
        b = T @ observations[i-1] @ b

    smoothed_estimates_for_state_true = []
    for i in sv[1:]: 
        smoothed_estimates_for_state_true.append(i[0])
    

    return smoothed_estimates_for_state_true



if __name__ == "__main__":
    # for problem 1.1 the smoothing for e1 and e2 
    O1 = [0,0,0,1,1,1,1,0,0,0]
    O2 = [0,1,0,1,0,1,0,1,0,1]
    sv1 = forward_backward(O1,10)
    sv2 = forward_backward(O2,10)
    print(sv1)
    print("---------------------")
    print(sv2)

