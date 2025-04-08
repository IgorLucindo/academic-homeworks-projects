from itertools import product
import numpy as np


def _get_shortest_path_optimal_policy(G):
    """
    Return best policy for shortest path problem
    """
    T = len(G.nodes)
    # Initialize value and policy tables
    V = {i: [float('inf')] * T for i in G.nodes}
    V['t'] = [0] * T
    pi = {i: [None] * T for i in G.nodes}

    # Backward induction for shortest path
    for tau, i in product(reversed(range(T - 1)), G.nodes):
        for j in G.neighbors(i):
            value = 1 + V[j][tau + 1]
            if value < V[i][tau]:
                V[i][tau] = value
                pi[i][tau] = j
                    
    return pi


def _shortest_path(G, s, pi):
    """
    Return solution of shortest path using best policy
    """
    T = len(G.nodes)
    i = s
    path = [i]

    # Construct path
    for tau in range(T - 1):
        if pi[i][tau] is None: break
        i = pi[i][tau]
        path.append(i)
        if i == 't': break

    return path


def solve_shortest_paths(G):
    """
    Return shortest paths using backward induction
    """
    pi = _get_shortest_path_optimal_policy(G)
    
    return [_shortest_path(G, v, pi) for v in G.nodes if v != 't']


def left(a):
    return [-a[1], a[0]]


def right(a):
    return [a[1], -a[0]]


def P(s_prime, s, a):
    sa = np.add(s, a)
    sa_left = np.add(sa, left(a))
    sa_right = np.add(sa, right(a))

    if np.array_equal(s_prime, sa):
        return 0.8
    elif np.array_equal(s_prime, sa_left):
        return 0.1
    elif np.array_equal(s_prime, sa_right):
        return 0.1
    else:
        return 0.0


def solve_grid_world(grid):
    """
    Return optimal policy of grid world obtained by using the policy iteration method
    """
    # Setup
    mask = ~np.isnan(grid)
    S = np.array(np.nonzero(mask)).T
    A = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    # Initialization
    V = {s: 0 for s in S}
    pi = {s: A[0] for s in S}

    return V, pi