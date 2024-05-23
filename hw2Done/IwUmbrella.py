import random
import numpy as np

def algo(numSamples, numSteps, observationList): 
    # note from the picture 
    # P(Ro = T) = P(Ro = F) = 0.5 

    # lets set up the prior prob 
    prior_prob = 0.5 

    samples_lst = np.array(numSamples * [None])
    weight_lst  = np.array(numSamples * [None])

    # we are going to let sample be true if val is 1 and sample be false if val is 0
    # first step we need to generate numSamples
    for i in range(numSamples): 
        sample = random.choice([0,1]) # works for our [0.5, 0.5 ] prior prob
        wt = 1.00

        # now we need to adjust the weight based on the evidence 
        for observation in observationList: 
            if observation: # the observatoin is 1, so we think it rained
                if sample: wt *= 0.9
                else: wt*= 0.2
            
            else: 
                if sample: wt *= 0.1
                else: wt*=0.8
        

            # now update the sample var so that it corresponds to the next observation
            value = random.random()
            if value < 0.7: # map sample to be raining 
                sample = 1
            else: 
                sample = 0
        
        samples_lst[i] = sample
        weight_lst[i] = wt

    # adjust the weights so that are normalized 
    weight_lst = weight_lst/weight_lst.sum()

    # now we have to calcualte the prob
    prob = 0 
    for i in range(len(samples_lst)): 
        if samples_lst[i]: 
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









                



