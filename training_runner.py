#################################################################
# JPYPE starts the java virtual machine and makes it possible   #
# to use java methods from graph6java.jar directly from python. #
#################################################################
# import jpype
import jpype.imports
import networkx as nx
from jpype.types import *

# startJVM method scans the provided class path for jar files and loads them all at once.
# hence you have to specify here the path to graph6java.jar
# if it is in the same directory as this file, then classpath=['*'] is enough.
jpype.startJVM(classpath=['*'], convertStrings=False)
from kcoloring import Kcoloring


#################################################################
# Examples of computing rewards by using graph6java.jar methods #
#################################################################
import numpy as np
import math
INF = 1000000                   # a very large number used by compute_reward to signify unwanted graphs

# TWO-COLOR RAMSEY NUMBERS

# - R(K5, K5-e) on 30-32 vertices
def R_K5_K5e(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK5(0)          # number of copies of K5 with edge color 0
    b = g.numK5e(1)         # number of copies of K5-e with edge color 1
    return -a-b             # we want to see zero here!

# - R(K4, K6-e) on 30-31 vertices

# - R(K4-e, K7) on 28 vertices
#   best: -206 after 5,400 gens
def R_K4e_K7(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK4e(0)
    b = g.numK7(1)
    return -a-b

# + R(K2,4, K3,5) on 19 vertices
#   best: reward -32 after 6,000 gens
def R_K24_K35(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK24(0)
    b = g.numK35(1)
    return -a-b

# + R(K2,5, K3,5) on less than 23 vertices
#   best: *** reward 0 on 19 vertices after 9,600 gens ***
#         reward -16 on 20 vertices after 16,000 gens
def R_K25_K35(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK25(0)
    b = g.numK35(1)
    return -a-b

def R_K25_K35_vert(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = np.array(g.numK25_vert(0))
    b = np.array(g.numK35_vert(1))
    return np.sum(np.exp(-a)) + np.sum(np.exp(-b)) - 2*n

# - R(K3,3, K3,4) on 19 vertices
#   best: reward -75 after 11,500 gens
def R_K33_K34(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK33(0)
    b = g.numK34(1)
    return -a-b

# + R(W5, W7) on 13-15 vertices
#   best: *** reward 0 on 13 vertices after 1,200 gens ***
#         reward -11 on 14 vertices after 38,000 gens
def R_W5_W7(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numW5(0)
    b = g.numW7(1)
    return -a-b

# - R(W4, W8) on 22-25 vertices
#   best: reward -202 on 22 vertices after 34,000 gens
def R_W4_W8(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numW4(0)
    b = g.numW8(1)
    return -a-b

# + R(B4, B5) on less than 19 vertices
#   best: *** reward 0 on 17 vertices after 4200 gens ***
#         reward -8 on 18 vertices after 14,800 gens
def R_B4_B5(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numB4(0)
    b = g.numB5(1)
    return -a-b

# - R(B3, B6) on less than 19 vertices
#   best: *** reward 0 on 16 vertices after 500 gens ***
#         !!! on 17 vertices reward stays stubbornly at -1, no matter what you do !!!
def R_B3_B6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numB3(0)
    b = g.numB6(1)
    return -a-b

# - R(B2, B8) on 19-21 vertices
#   best: reward -10 on 19 vertices after 45,000 gens
#         (jump from -13 to -10 after 23,000 gens!)
def R_B2_B8(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numB2(0)
    b = g.numB8(1)
    return -a-b

# - R(W5, K6) on 33-35 vertices
#   best: reward -833 on 33 vertices after 3,300 gens

# - R(W6, K6) on 34-39 vertices
#   best: reward -2019 on 34 vertices after 3,200 gens

# - R(K2,2,2, K2,2,2) on 30 vertices
#   best: reward -1170 after 4,500 gens

# MULTICOLOR RAMSEY NUMBERS

# - R(4x C6) on 18-20 vertices
#   best: reward -1198 on 18 vertices after 8,500 gens
def R_C6_C6_C6_C6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC6(0)
    b = g.numC6(1)
    c = g.numC6(2)
    d = g.numC6(3)
    return -a-b-c-d

# - R(C4, 3x C6) on 18-20 vertices
#   best: reward -175 on 18 vertices after 11,500 gens
def R_C4_C6_C6_C6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC4(0)
    b = g.numC6(1)
    c = g.numC6(2)
    d = g.numC6(3)
    return -a-b-c-d

# - R(2x C4, 2x C6) on 18-20 vertices,
#   best: reward -40 on 18 vertices after 8,900 gens
def R_C4_C4_C6_C6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC4(0)
    b = g.numC4(1)
    c = g.numC6(2)
    d = g.numC6(3)
    return -a-b-c-d

# - R(2x C4, K4) on 20 vertices
#   best: reward -17 after 5,600 gens
def R_C4_C4_K4(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC4(0)
    b = g.numC4(1)
    c = g.numK4(2)
    return -a-b-c

# - R(C3, 2x C6) on 15-18 vertices
#   best: reward -70 on 15 vertices after 22,000 gens
def R_C3_C6_C6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC3(0)
    b = g.numC6(1)
    c = g.numC6(2)
    return -a-b-c

# + R(C5, 2x C6) on 15-17 vertices
#   best: -70 on 15 vertices after 11,000 gens
def R_C5_C6_C6(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC5(0)
    b = g.numC6(1)
    c = g.numC6(2)
    return -a-b-c

# - R(K3, 2x K4-e) on 21 vertices,
#   best: reward -115 after 7,300 gens
def R_K3_K4e_K4e(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK3(0)
    b = g.numK4e(1)
    c = g.numK4e(2)
    return -a-b-c

# - R(C3, 3x C4) on 24-26 vertices,
def R_C3_C4_C4_C4(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC3(0)
    b = g.numC4(1)
    c = g.numC4(2)
    d = g.numC4(3)
    return -a-b-c-d

# - R(5x C4) on 27-28 vertices,
def R_C4_C4_C4_C4_C4(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC4(0)
    b = g.numC4(1)
    c = g.numC4(2)
    d = g.numC4(3)
    e = g.numC4(4)
    return -a-b-c-d-e

# - R(C3, C4, K4) on 27-31 vertices,
def R_C3_C4_K4(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC3(0)
    b = g.numC4(1)
    c = g.numK4(2)
    return -a-b-c

# - R(K3, K4, K4-e) on 31-39 vertices,
def R_K3_K4_K4e(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK3(0)
    b = g.numK4(1)
    c = g.numK4e(2)
    return -a-b-c

# - R(C4, K4, K4-e) on 29-35 vertices,
def R_C4_K4_K4e(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numC4(0)
    b = g.numK4(1)
    c = g.numK4e(2)
    return -a-b-c

# - R(4x K3) on 51-61 vertices?!
def R_K3_K3_K3_K3(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK3(0)
    b = g.numK3(1)
    c = g.numK3(2)
    d = g.numK3(3)
    return -a-b-c-d

# Reference: S.P.Radziszowski, Small Ramsey Numbers, EJC DS#1,
# https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1/pdf


############################################################
# Training the cross entropy method agent on above rewards #
############################################################
if __name__=="__main__":
    from cema_train_ramsey import train
            # how does learning go with a single step indicator instead of one-hot encoding?

    # how to prevent that the maximum reward does not decrease?!

    r, A = train(compute_reward=R_B3_B6,
                 n=17,
                 colors=2,
                 batch_size=500,
                 # neurons=[100,50,25,12,6],
                 percent_learn=97.5,
                 percent_survive=99,
                 act_rndness_init=0.01,
                 act_rndness_wait=20,
                 act_rndness_mult=1.25,
                 act_rndness_max=1,
                 output_best_graph_rate=200,
                 num_generations=100000)

# when jpype is no longer needed...
jpype.shutdownJVM()
