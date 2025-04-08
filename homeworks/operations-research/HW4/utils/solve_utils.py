from itertools import product


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