import numpy as np


# generate instances definite matrices Q, matrices A and vectors c as instances
def generate_instances(number_of_instances, dim):
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