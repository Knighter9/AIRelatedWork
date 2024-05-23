import random
# code definitions here
def gibbsSampler(numberOfIterations):
    # we want to sample for P(r |s, w) so we seay s and w are true they are our evidence vars we will fix them to true
    p_c_given_r_w_s = 0.44 # p(c|r,w,s)
    p_notc_given_r_w_s = 0.56 # p(~c|r,w,s)
    p_c_given_notr_w_s = 0.05 # p(c|~r,w,s)
    p_notc_given_notr_w_s = 0.95 # p(~c|~r,w,s)
    p_r_given_c_w_s = 0.81 # p(r|c,w,s)
    p_notr_given_c_w_s = 0.19 # p(~r|c,w,s)
    p_r_given_notc_w_s = 0.22 # p(r| ~c,w,s)
    p_notr_given_notc_w_s = 0.78 # p(~r|~c,w,s)

    # we can represent each sample as a vector so for example say we have 
    # sample =  r=true, w=true,s=true,c = false we could represent it as
    # [1,1,1,0]

    # general steps for algorithm
    # fix the evidence vars. In our case it is s and w. So S=true, and W = true
    # randomly set the values of all other variables
    # for the given number of iterations:
    #     randomly pick a non evidence var
    #     set its value determined by p(var| the other vars left)
    #     check to see if the var we are intrest in, in htis case R is set to true, if so increment a counter:
    # return counter/number of samples

    # we are going to represent the variables in this order
    # sample = [C,R,S,W]
    
    c_value = random.choice([0,1])
    r_value = random.choice([0,1])
    sample = [c_value, r_value,1,1]
    counter = 0
    for i in range(numberOfIterations):
        # randomly select evidence var
        var_indx = random.choice([0,1])
        if var_indx == 0: # we have select to deal with var C
            # check to see if R is true
            if sample[1] == 1: # R is true 
                counter+=1
                num = random.random()
                if num < p_c_given_r_w_s: sample[0] = 1
                else: sample[0] = 0

            else: # R is false
                num = random.random()
                if num < p_c_given_notr_w_s: sample[0] = 1
                else: sample[0] = 0
        
        else: # we have selected to deal with var R
            # first check to see if R is true
            if sample[1] == 1: # R is true
                counter+=1
            
            if sample[0] == 1: # C is true
                num = random.random()
                if num < p_r_given_c_w_s: sample[1] = 1
                else: sample[1] = 0

            else: # C is false
                num = random.random()
                if num < p_r_given_notc_w_s: sample[1] = 1
                else: sample[1] = 0
    
    return counter/numberOfIterations








if __name__ == "__main__":
    print("how many iterations would you like to run")
    num = int(input())
    print(gibbsSampler(num))

    