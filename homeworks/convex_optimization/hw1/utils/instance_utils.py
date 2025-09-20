from itertools import product
import random


def get_max_balance_instance():
    """
    Returns instance for the max balance problem
    """
    # Periods
    T = range(1, 7)

    # Deposit type
    I = [1, 2, 3]

    # Interest rates
    r = {1: 1.04, 2: 1.09, 3: 1.15}

    return T, I, r


def get_min_shipping_cost_instance():
    """
    Returns instance for the min shipping cost problem
    """
    # Factories
    F = ["f1", "f2"]

    # Distribution centers
    D = ["d1", "d2"]

    # Stores
    S = ["s1", "s2", "s3"]

    # Routes
    E = [(f, d) for f in F for d in D] + [(d, s) for d in D for s in S]

    # Costs
    c_exp = {
        ("f1", "d1"): uniform_expectation(2),
        ("f1", "d2"): uniform_expectation(4),
        ("f2", "d1"): uniform_expectation(3),
        ("f2", "d2"): uniform_expectation(1),
        ("d1", "s1"): uniform_expectation(3),
        ("d1", "s2"): uniform_expectation(1),
        ("d1", "s3"): uniform_expectation(2),
        ("d2", "s1"): uniform_expectation(2),
        ("d2", "s2"): uniform_expectation(3),
        ("d2", "s3"): uniform_expectation(2)
    }

    # Capacities
    mu_exp = {
        ("f1", "d1"): uniform_expectation(60),
        ("f1", "d2"): uniform_expectation(50),
        ("f2", "d1"): uniform_expectation(40),
        ("f2", "d2"): uniform_expectation(60),
        ("d1", "s1"): uniform_expectation(40),
        ("d1", "s2"): uniform_expectation(40),
        ("d1", "s3"): uniform_expectation(40),
        ("d2", "s1"): uniform_expectation(40),
        ("d2", "s2"): uniform_expectation(40),
        ("d2", "s3"): uniform_expectation(40)
    }

    # Supply capacity at factories
    su = {"f1": 70, "f2": 50}

    # Demand at stores
    de = {"s1": 40, "s2": 45, "s3": 35}

    return E, F, S, D, c_exp, mu_exp, su, de


def get_sudoku_instance():
    """
    Returns instance for the sudoku problem
    """
    # Set of rows, columns, blocks or numbers
    N = range(9)

    # Sets of cells in sub blocks
    B = {
        k: [((k // 3) * 3 + di, (k % 3) * 3 + dj) for di in range(3) for dj in range(3)]
        for k in N
    }

    # Given Sudoku puzzle
    givens = {
        (0, 2): 2, (0, 5): 5,
        (1, 2): 1, (1, 3): 6, (1, 5): 2,
        (2, 0): 9, (2, 1): 3, (2, 2): 8,
        (3, 4): 7, (3, 5): 4, (3, 7): 6,
        (4, 1): 7, (4, 6): 2,
        (5, 0): 3, (5, 7): 1,
        (6, 3): 9,
        (7, 4): 2, (7, 6): 9, (7, 8): 8,
        (8, 1): 1, (8, 3): 8, (8, 8): 3,
    }

    # Initial sudoku instance
    a = {
        (i, j, n): int((i, j) in givens and givens[(i, j)] == n + 1)
        for i, j, n in product(N, N, N)
    }

    return N, B, a


def uniform_expectation(val, n_samples=1000, variation=0.01):
    """
    Returns expected value of a random variable with uniform distribution
    """
    return sum(val * (1 + random.uniform(-variation, variation)) for _ in range(n_samples)) / n_samples