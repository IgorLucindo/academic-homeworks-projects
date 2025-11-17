def get_cutting_stock_instance():
    """
    Returns instance for cutting stock problem
    """
    # Roll length
    L = 20

    # Lengths
    l = [1, 2, 4, 7]

    # Demands
    d = [25, 12, 42, 21]

    # Total number of rolls
    n = sum(d)

    return L, l, d, n


def get_investment_instance():
    """
    Returns instance for investment problem
    """
    # Transaction
    c = [0.004, 0.006, 0.003]

    # Gross returns of each asset in each scenario
    G = [
        [1.06, 1.01, 0.98],
        [0.95, 1.03, 1.02],
        [1.10, 0.97, 0.96]
    ]

    # Required liabilities
    L = [1.01, 1.00, 1.02]

    # Borrowing cost coefficients
    k = [0.08, 0.09, 0.10]

    # Scenario probabilities
    p = [0.3, 0.4, 0.3]

    return c, G, L, k, p