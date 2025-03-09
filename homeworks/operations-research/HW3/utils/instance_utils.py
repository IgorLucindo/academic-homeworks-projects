# return set of diagonal coordinates of a chess board
def get_diagonals_set(n):
    # positive diagonals
    D_plus = [tuple([(i, k - i) for i in range(n) if i <= k < n + i]) for k in range(2 * n - 1)]

    # negative diagonals
    D_minus = [tuple([(i, i - k) for i in range(n) if k <= i < n + k]) for k in range(-(n - 1), n)]
    
    # return set
    return D_plus + D_minus