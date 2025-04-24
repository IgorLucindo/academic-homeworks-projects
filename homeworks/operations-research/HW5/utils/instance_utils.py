from scipy.stats import uniform, beta, triang
import numpy as np


def get_shipping_instance(num_samples=1e4):
    """
    Return instance for the minimum expected total cost
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
    data = np.column_stack([dist.rvs(size=int(num_samples)) for dist in c_dist])

    # Apply transformation: 5 + 3 * Beta(2, 2) for the second column
    data[:, 1] = 5 + 3 * data[:, 1]

    # Compute empirical mean and covariance
    mean = np.mean(data, axis=0)
    sigma = np.cov(data, rowvar=False)

    return s, S, _beta, mean, sigma