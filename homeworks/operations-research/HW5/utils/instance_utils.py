from scipy.stats import uniform, beta, triang
import numpy as np


def get_shipping_instance(num_samples=1e4):
    """
    Return instance for the shipping problem
    """
    s = [100, 80, 120]
    S = range(len(s))
    _beta = 1e5

    # Define distributions cost
    c_dist = [
        uniform(loc=5, scale=3),
        beta(a=2, b=2),
        triang(c=5/7, loc=4, scale=7)
    ]

    # Generate samples (each column is a variable)
    cost = np.column_stack([dist.rvs(size=int(num_samples)) for dist in c_dist])

    # Apply transformation: 5 + 3*Beta(2, 2) for the second column
    cost[:, 1] = 5 + 3*cost[:, 1]

    return s, S, _beta, cost


def get_ordering_instance(num_samples=50):
    """
    Return instance for ordering problem
    """
    # Set of suppliers
    S = range(9)

    # Set of distribution centers
    C = range(2)

    # Capacity
    a = np.array([[10, 23, 13, 4, 9, 20, 15, 6, 12],
                  [3, 8, 30, 11, 6, 33, 17, 18, 9]]).T
    # Cost
    c = [9, 11, 7, 8, 8, 13, 21, 16, 11]

    # Demand
    d_dist = [
        uniform(loc=5, scale=3),
        triang(c=32/35, loc=35, scale=35)
    ]
    d = np.column_stack([dist.rvs(size=num_samples) for dist in d_dist])

    return S, C, a, c, d