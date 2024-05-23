import numpy as np 
import random 

def algo(numSamples,numsteps, observationsList): 
    '''
    Very similar to weighted likelyhood sample except we use particles to form a new distrubution and then sample from that distrubtion to 
    get a new particle set which we then form a new distrubution of. This cycle repeats until we run out of steps, and then we just report soln. 
    '''
    # number samples = number particles
    # num steps = length of observations
    # observations = observed states, so umbrealla or not

    particles_lst = np.array(numSamples * [None])
    weight_lst = np.array(numSamples * [None])


    # set up a random first distrubution for the particles 

    for i in range(numSamples):
        particles_lst[i] = random.choice([0,1]) # works for our [0.5, 0.5 ] prior prob
        weight_lst[i] = 1
    
    # normalize the weights so they sum to 1
    weight_lst = weight_lst / weight_lst.sum()

    #update each particle based on the supplied observations
    for observation in observationsList: 
        for i in range(len(particles_lst)):
            val = random.random() 
            if val < 0.7: particles_lst[i] = 1
            else: particles_lst[i] = 0

            # update the weight 
            val = 0
            if observation: 
                if particles_lst[i]: val = 0.9 
                else: val = 0.2
            else: 
                if particles_lst[i]: val = 0.1 
                else: val = 0.8 
            
            weight_lst[i] *= val 
        
        # update the weight so they sum to 1
        weight_lst = weight_lst/weight_lst.sum()


    prob = 0
    for i in range(len(particles_lst)): 
        if particles_lst[i]:
            prob += weight_lst[i]

    return prob


if __name__ == "__main__": 
    lst_for_100_samples_probsO1 = []
    lst_for_1000_samples_probsO1 = []
    lst_for_100_samples_probsO2 = []
    lst_for_1000_samples_probsO2 = []
    lst_for_100_samples_probsO3 = []
    lst_for_1000_samples_probsO3 = []
    for i in range(10): 
        lst_for_100_samples_probsO1.append(algo(100,10,[1,1,1,1,1,0,0,0,0,0]))
        lst_for_1000_samples_probsO1.append(algo(1000,10,[1,1,1,1,1,0,0,0,0,0]))

        lst_for_100_samples_probsO2.append(algo(100,10,[0,0,0,0,0,0,0,1,1,1]))
        lst_for_1000_samples_probsO2.append(algo(1000,10,[0,0,0,0,0,0,0,1,1,1]))

        lst_for_100_samples_probsO3.append(algo(100,10,[0,1,0,1,0,1,0,1,0,1]))
        lst_for_1000_samples_probsO3.append(algo(1000,10,[0,1,0,1,0,1,0,1,0,1]))


    hundred_avgO1 = np.average(lst_for_100_samples_probsO1)
    thousand_avgO1 = np.average(lst_for_1000_samples_probsO1)
    hundred_varO1 = np.var(lst_for_100_samples_probsO1)
    thousand_varO1 = np.var(lst_for_1000_samples_probsO1)

    print("Observation 1 sequence: [1,1,1,1,1,0,0,0,0,0]")
    print("hundred sample data: ")
    print("average: " + str(hundred_avgO1))
    print("var: " + str(hundred_varO1))
    print("thousand sample data: ")
    print("average: " + str(thousand_avgO1))
    print("var: " + str(thousand_varO1))

    print("                                    ")
    hundred_avgO2 = np.average(lst_for_100_samples_probsO2)
    thousand_avgO2 = np.average(lst_for_1000_samples_probsO2)
    hundred_varO2 = np.var(lst_for_100_samples_probsO2)
    thousand_varO2 = np.var(lst_for_1000_samples_probsO2)
    print("                                    ")
    print("Observation 2 sequence: [0,0,0,0,0,0,0,1,1,1]")
    print("hundred sample data: ")
    print("average: " + str(hundred_avgO2))
    print("var: " + str(hundred_varO2))
    print("thousand sample data: ")
    print("average: " + str(thousand_avgO2))
    print("var: " + str(thousand_varO2))

    print("                                    ")


    hundred_avgO3 = np.average(lst_for_100_samples_probsO3)
    thousand_avgO3 = np.average(lst_for_1000_samples_probsO3)
    hundred_varO3 = np.var(lst_for_100_samples_probsO3)
    thousand_varO3 = np.var(lst_for_1000_samples_probsO3)
    print("                                    ")
    print("Observation 3 sequence: [0,1,0,1,0,1,0,1,0,1]")
    print("hundred sample data: ")
    print("average: " + str(hundred_avgO3))
    print("var: " + str(hundred_varO3))
    print("thousand sample data: ")
    print("average: " + str(thousand_avgO3))
    print("var: " + str(thousand_varO3))









                



