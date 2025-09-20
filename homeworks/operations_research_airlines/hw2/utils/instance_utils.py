import numpy as np


# generate instances definite matrices Q and A, vectors c and b as instances
def generate_p1_instances(number_of_instances, dim):
    instances = []
    for i in range(number_of_instances):
        # random symmetric matrix
        Q = np.random.rand(dim, dim)
        Q = np.dot(Q, Q.T)

        # random matrix
        A = np.random.rand(dim, dim)

        # random vectors
        c = np.random.rand(dim, 1)
        b = np.random.rand(dim, 1)

        # append instance
        instances.append([Q, A, c, b])

    # return instances
    return instances


# generate problem 2 instance (ordering from supplier to distribution centers)
def generate_p2_instance():
    # suppliers set
    S = range(9)

    # distribution centers set
    C = range(2)

    # supply
    a = np.array([[10, 23, 13, 4, 9, 20, 15, 6, 12],
                  [3, 8, 30, 11, 6, 33, 17, 18, 9]]).T
    # cost
    c = [9, 11, 7, 8, 8, 13, 21, 16, 11]

    # demand
    d = [46, 54]

    return S, C, a, c, d