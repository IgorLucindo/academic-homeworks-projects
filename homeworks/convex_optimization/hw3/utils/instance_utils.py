import numpy as np
import random


def generate_lp_instances(num_of_instances):
    """
    Generates a list of random LP instances
    """
    return [_generate_lp_instance() for _ in range(num_of_instances)]


def generate_lp_feasible_instances(num_of_instances):
    """
    Generates a list of random LP instances
    """
    return [_generate_lp_feasible_instance() for _ in range(num_of_instances)]


def _generate_lp_instance():
    """
    Generates a random LP instance (A, b, c)
    """
    n = random.randint(3, 10)
    m = random.randint(3, 10)
    A = np.random.randint(10, 100, size=(n, m))
    b = np.random.randint(1, 2, size=(n, 1))
    c = np.random.randint(1, 100, size=(m, 1))

    return A, b, c


def _generate_lp_feasible_instance():
    """
    Generates a random LP instance (A, b, c)
    """
    n = random.randint(3, 10)
    m = random.randint(3, 10)
    A = -np.random.randint(10, 100, size=(n, m))
    b = -np.random.randint(1, 2, size=(n, 1))
    c = np.random.randint(1, 100, size=(m, 1))

    return A, b, c