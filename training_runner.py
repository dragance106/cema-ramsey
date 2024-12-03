import numpy as np
import math
import multiprocessing as mp

INF = 1000000                   # a very large number used by compute_reward to signify unwanted graphs


def two_walk_projection(n, A):
    """
    Computes the projection of A**2.j onto the span of {j, A.j},
    where j is the all-one vector.

    :param n:   The number of vertices
    :param A:   The adjacency matrix
    :return:    The tuple consisting of degrees A.j, two-walks A**2.j,
                the coefficients alpha and beta in the projection A**2.j = alpha A.j + beta j,
                the actual projection alpha A.j + beta j and
                the difference A**2.j - alpha A.j - beta j
    """
    # the all-one vector
    j = np.ones(n)
    # the degree vector A.j
    d = np.dot(A, j)
    # the two-walks vector A**2.j
    t = np.dot(A, d)

    # the projection of A**2.j onto the space spanned by j and A.j is
    # given by A**2.j = alpha * A.j + beta j,
    # where alpha = det([[j.T A**2 j, j.T j],
    #                    [j.T A**3 j, j.T A j]])
    #              /det([[j.T A j, j.T j],
    #                    [j.T A**2 j, j.T A j]])
    #    and beta = det([[j.T A j, j.T A**2 j],
    #                    [j.T A**2 j, j.T A**3 j]])
    #              /det([[j.T A j, j.T j],
    #                    [j.T A**2 j, j.T A j]])

    # auxiliary values first
    n0 = n                      # = j.T j
    n1 = np.dot(j.T, d)         # = j.T A j
    n2 = np.dot(j.T, t)         # = j.T A**2 j
    n3 = np.dot(d.T, t)         # = j.T A**3 j

    # is graph regular?
    if n1*n1 == n2*n0:
        # yes, so already Aj is a multiple of j
        return d, t, 0, t[0], t, np.zeros(n)

    # non-regular, so you can divide with n1*n1 - n2*n0
    alpha = (n2*n1 - n3*n0) / (n1*n1 - n2*n0)
    beta  = (n3*n1 - n2*n2) / (n1*n1 - n2*n0)

    # the projection and the difference
    p = alpha * d + beta * j
    z = t - p

    return d, t, alpha, beta, p, z


def two_walk_reward(params):
    """
    The graph has two main eigenvalues if and only if
    the dot product A**2.j is in the space spanned by j and A.j,
    where j is the all-one vector from R**n.

    The method computes the sine of the angle between A**2.j and the space spanned by j and A.j,
    as the measure of how far away the graph is from having two main eigenvalues.

    The reward returned is minus of this sine, since we want to minimize the sine.

    :param n:   The number of vertices
    :param A:   The adjacency matrix
    :return:    The negative of the sine of the angle between A**2.j and the space spanned by j and A.j
    """

    n, A = params
    d, t, alpha, beta, p, z = two_walk_projection(n, A)

    # count the number of distinct degrees in d
    # we do not want one or two only
    # or the complements of Rowlinson's tree with isolated vertices
    if len(np.unique(d)) <= 4:
        return -INF

    t_squared = np.dot(t.T, t)
    z_squared = np.dot(z.T, z)

    if z_squared == 0.0:
        return 0.0
    else:
        return -np.dot(t.T, z) / math.sqrt(t_squared * z_squared)


############################################################
# Training the cross entropy method agent on above rewards #
############################################################
if __name__=="__main__":
    mp.freeze_support()
    from cema_train_multiprocessing import train

    for _ in range(100):
        r, A = train(compute_reward=two_walk_reward,
                     n=30,
                     # batch_size=250,
                     # percent_learn=95,
                     # percent_survive=98.5,
                     # act_rndness_max=0.1,
                     num_generations=2000)
