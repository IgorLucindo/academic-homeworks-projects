import gurobipy as gp
from gurobipy import GRB
import numpy as np


def solve_max_lp_simplex(instance, tol=1e-6):
    """
    Solves max c^T x  s.t. A x >= b, x >= 0
    using the primal simplex method (assuming feasible start).
    Internally reformulated as a minimization problem.
    """
    An, b, cn = instance
    n = An.shape[0]
    cn = -cn
    Ab = -np.eye(n)
    cb = np.zeros((n, 1))

    # Initialize
    Ab_inv = np.linalg.inv(Ab)
    xb = Ab_inv @ b
    S = Ab_inv @ An
    reduced_cost = cn - S.T @ cb

    iteration = 0
    while np.any(reduced_cost < -tol):
        iteration += 1

        # Choose entering variable (most negative reduced cost)
        j = np.argmin(reduced_cost)
        d = S[:, j].reshape(-1, 1)

        # Feasibility check: if all d ≤ 0 → unbounded
        positive = d > tol
        if not np.any(positive):
            return {'x': None, 'objective': None, 'status': 'unbounded'}

        # Ratio test
        ratios = np.where(positive, xb / d, np.inf)
        i = np.argmin(ratios)
        theta = ratios[i]

        # Update basic variable values
        xb = xb - theta * d
        xb[i, 0] = theta

        # Pivot
        Ab[:, i] = An[:, j].flatten()
        Ab_inv = np.linalg.inv(Ab)
        S = Ab_inv @ An
        cb[i, 0] = cn[j, 0]
        reduced_cost = cn - S.T @ cb

    return {
        'x': xb,
        'objective': -float(cb.T @ xb),
        'status': 'optimal'
    }


def solve_max_lp_simplex_gurobi(instance):
    """
    Solves max lp using Gurobi
    """
    A, b, c = instance
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).flatten()
    c = np.array(c, dtype=float).flatten()
    n, m = A.shape

    # Create model
    model = gp.Model("Max_lp")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(range(m), lb=0, name="x")

    # Set objective function
    obj_fn = gp.quicksum(c[j] * x[j] for j in range(m))
    model.setObjective(obj_fn, GRB.MAXIMIZE)

    # Add constraints
    model.addConstrs((gp.quicksum(A[i, j] * x[j] for j in range(m)) >= b[i] for i in range(n)), name="c2")

    # Solve
    model.optimize()

    if model.status in [3, 4, 15]:
        return {'x': None, 'objective': None, 'status': 'infeasible'}

    return {
        'x': [x[j].X for j in range(m)],
        'objective': model.objVal,
        'status': 'optimal'
    }