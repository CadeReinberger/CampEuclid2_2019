from random import randint as rand
import numpy as np
import scipy.stats as stats
from timeit import default_timer as tictoc

p = 11 #We often assume p is not 2 or 3. Don't make p = 2, 3
num = 1000000

class lin_funct:
    def __init__(self, m, l):
        self._mu = m
        self._lambda = l
    
    def act_on_elem(self, phi):
        return (self._mu * phi + self._lambda) % p
    
    def apply_lin_funct(self, applied):
        new_mu = applied.act_on_elem(self._mu)
        new_lambda = applied.act_on_elem(self._mu)
        return lin_funct(new_mu, new_lambda)
        
    def lambdaZeroQ(self):
        return np.abs(self._lambda) < .05 #Just a slight attempt to account for any rounding error buildup, probably wont do anything
    
    def identity():
        return lin_funct(1, 0)
    
class random_walk:
    half = lin_funct((p+1)//2, 0)
    double = lin_funct(2, 0)
    triple_plus_one = lin_funct(3, 1)
    if p % 3 == 2:
        three_inv = (p + 1) // 3
    else:
        three_inv = (2 * p + 1) // 3
    minus_one_thirded = lin_funct(three_inv, p - three_inv)
    
    def iverson_bracket(boool):
        if boool:
            return 1
        else:
            return 0
    
    def apply_random(cur):
        ri = rand(0, 3)
        if ri == 0:
            return cur.apply_lin_funct(random_walk.half)
        elif ri == 1:
            return cur.apply_lin_funct(random_walk.double)
        elif ri == 2:
            return cur.apply_lin_funct(random_walk.triple_plus_one)
        else:
            return cur.apply_lin_funct(random_walk.minus_one_thirded)
        
    def iterate_random(cur_elem, cur_gud, cur_tot):
        elem_prime = random_walk.apply_random(cur_elem)
        return elem_prime, cur_gud + random_walk.iverson_bracket(elem_prime.lambdaZeroQ()), cur_tot + 1
    
    def run(num_times):
        cur_lin = lin_funct.identity()
        cur_lambda_zero = 0
        cur_trials = 0
        while cur_trials <= num_times:
            cur_lin, cur_lambda_zero, cur_trials = random_walk.iterate_random(cur_lin, cur_lambda_zero, cur_trials)
        return cur_lambda_zero / cur_trials
    
    def proccess(N):
        pi_hat = random_walk.run(N)
        pi_naught = 1/p
        std_dev = np.sqrt(pi_naught * (1 - pi_naught) / N)
        z_score = (pi_hat - pi_naught)/std_dev
        moe = 1.96 * std_dev
        pe = 100 * np.abs(pi_hat - pi_naught) / pi_naught
        if z_score >= 0:
            p_value = 2 * stats.norm.sf(z_score)
        else:
            p_value = 2 * stats.norm.cdf(z_score)
        print("With p = " + str(p // 1) + " and N = " + str(N//1))
        print("")
        print("Expected proportion: " + str(pi_naught))
        print("Observed proportion: " + str(pi_hat))
        print("Percent Error: " + str(pe))
        print("Margin of Error at 95% confidence: " + str(moe))
        print("P-Value: " + str(p_value))
        return        
    
t_one = tictoc()
random_walk.proccess(num)  
t_two = tictoc()
print("")
print("Computation time[s]: " + str(t_two - t_one))


############################################################
########### SAMPLE OUTPUT ##################################
############################################################
#
#  With p = 11 and N = 1000000
# 
#  Expected proportion: 0.09090909090909091
#  Observed proportion: 0.09091690908309091
#  Percent Error: 0.008599991400001783
#  Margin of Error at 95% confidence: 0.0005634603830845476
#  P-Value: 0.9783037564607935
#
#  Computation time[s]: 4.184357818000535
#
############################################################
############################################################
############################################################