from itertools import product


def get_tic_tac_toe_optimal_policy(boards, successor, remaining_plays, board_result):
    """
    Return optimal policy for Tic-Tac-Toe
    """
    # MDP parameters
    T = remaining_plays + 1

    # Initialize value and policy tables
    def default_value(t): return float('-inf') if t % 2 == 0 else float('inf')
    V = {
        t: {b: board_result.get(b, default_value(t)) for b in boards[t]}
        for t in range(T)
    }
    pi = {t: {b: None for b in boards[t]} for t in range(T)}

    # Get optimal policy by backward induction
    for t in reversed(range(T - 1)):
        for s in boards[t]:
            for s_prime in successor[s]:
                value = V[t + 1][s_prime]
                if (t % 2 == 0 and value > V[t][s]) or (t % 2 == 1 and value < V[t][s]):
                    V[t][s] = value
                    pi[t][s] = s_prime

    return pi


def solve_shortest_paths(G):
    """
    Return shortest paths using backward induction
    """
    # MDP parameters
    S = G.nodes
    T = len(G.nodes)

    # Initialize value and policy tables
    V = {i: [float('inf')] * T for i in S}
    V['t'] = [0] * T
    pi = {i: [None] * T for i in S}

    # Get optimal policy by backward induction
    
    for t, s in product(reversed(range(T - 1)), S):
        for s_prime in G.neighbors(s):
            value = 1 + V[s_prime][t + 1]
            if value < V[s][t]:
                V[s][t] = value
                pi[s][t] = s_prime
    
    return [_shortest_path(G, v, pi) for v in G.nodes if v != 't']


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