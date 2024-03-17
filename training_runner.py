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


# kcoloring.jar has implemented counters for:
# graph   to get the count of copies in color c, call:
# K3:     g.numK3(c)
# K4      g.numK4(c)
# K4-e    g.numK4e(c)
# K5      g.numK5(c)
# K5-e    g.numK5e(c)
# K6      g.numK6(c)
# K6-e    g.numK6e(c)
# K2,4    g.numK24(c)
# K2,5    g.numK25(c)
# K3,3    g.numK33(c)
# K3,4    g.numK34(c)
# K3,5    g.numK35(c)
# K2,2,2  g.numK222(c)
# W4      g.numW4(c)
# W5      g.numW5(c)
# W6      g.numW6(c)
# W7      g.numW7(c)
# W8      g.numW8(c)
# B2      g.numB2(c)
# B3      g.numB3(c)
# B4      g.numB4(c)
# B5      g.numB5(c)
# B8      g.numB8(c)
# C3      g.numC3(c)
# C4      g.numC4(c)
# C5      g.numC5(c)
# C6      g.numC6(c)

# USE CEMA TO TRY TO CONSTRUCT A GRAPH THAT WILL ESTABLISH
# A LOWER BOUND FOR EACH OF THE FOLLOWING RAMSEY NUMBERS:

# TWO-COLOR RAMSEY NUMBERS

# - R(K5, K5-e) on 30-32 vertices
def R_K5_K5e(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK5(0)          # number of copies of K5 with edge color 0
    b = g.numK5e(1)         # number of copies of K5-e with edge color 1
    return -a-b             # we want to see zero here!

# - R(K4, K6-e) on 30-31 vertices
# - R(K4-e, K7) on 28 vertices

# - R(K2,4, K3,5) on 19 vertices
def R_K24_K35(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numK24(0)
    b = g.numK35(1)
    return -a-b

# - R(K2,5, K3,5) on less than 23 vertices

# - R(W5, W7) on 13-15 vertices
def R_W5_W7(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numW5(0)
    b = g.numW7(1)
    return -a-b

# - R(W4, W8) on 22-25 vertices

# - R(B4, B5) on less than 19 vertices
def R_B4_B5(n, colors, A):
    g = Kcoloring(JInt[:,:](A))
    a = g.numB4(0)
    b = g.numB5(1)
    return -a-b

# - R(B3, B6) on less than 19 vertices

# - R(B2, B8) on 19-21 vertices

# - R(W5, K6) on 33-35 vertices
# - R(W6, K6) on 34-39 vertices
# - R(K2,2,2, K2,2,2) on 30 vertices

# MULTICOLOR RAMSEY NUMBERS

# - R(4x C6) on 18-20 vertices,
# - R(C4, 3x C6) on 18-20 vertices,
# - R(2x C4, 2x C6) on 18-20 vertices,
# - R(2x C4, K4) on 20 vertices,
# - R(C3, 2x C6) on 15-18 vertices,
# - R(C5, 2x C6) on 15-17 vertices,
# - R(K3, 2x K4-e) on 21 vertices,
# - R(K3,3, K3,4) on 20 vertices,
# - R(W5, W7) on 14-16 vertices,
# - R(C3, 3x C4) on 24-26 vertices,
# - R(5x C4) on 27-28 vertices,
# - R(C3, C4, K4) on 27-31 vertices,
# - R(K3, K4, K4-e) on 31-39 vertices,
# - R(C4, K4, K4-e) on 29-35 vertices,
# - R(4x K3) on 51-61 vertices?!
#
# Reference: S.P.Radziszowski, Small Ramsey Numbers, EJC DS#1,
# https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1/pdf


############################################################
# Training the cross entropy method agent on above rewards #
############################################################
if __name__=="__main__":
    from cema_train_ramsey import train

    r, A = train(compute_reward=R_W5_W7,
                 n=13,
                 colors=2,
                 act_rndness_max=0.1,
                 output_best_graph_rate=100,
                 num_generations=100000)

# r, A = train(compute_reward=R_K5_K5e,
#              n=30,
#              colors=2,
#              batch_size=200,
#              num_generations=10000,
#              percent_learn=92,
#              percent_survive=94,
#              learning_rate=0.0015,
#              neurons=[192,16],
#              act_rndness_init=0.0005,
#              act_rndness_max=0.0015)

# when jpype is no longer needed...
jpype.shutdownJVM()
