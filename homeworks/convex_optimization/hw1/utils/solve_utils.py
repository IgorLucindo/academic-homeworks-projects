from itertools import product
import gurobipy as gp
from gurobipy import GRB


def solve_max_balance(instance):
    """
    Return optimal shipping for minimum expected total cost
    """
    T, I, r = instance

    # Create model
    model = gp.Model("Max_Balance")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(T, lb=0, name="x")
    y = model.addVars(I, T, lb=0, name="y")

    # Set objective function
    obj_fn = x[6]
    model.setObjective(obj_fn, GRB.MAXIMIZE)

    # Add constraints
    x[1].ub = 5000
    model.addConstr(x[2] <= r[1] * y[1, 1], name="c1")
    model.addConstrs((x[t] <= gp.quicksum(r[i] * y[i, t-i] for i in [1, 2]) for t in [3, 4]), name="c2")
    model.addConstrs((x[t] <= gp.quicksum(r[i] * y[i, t-i] for i in I) for t in [5, 6]), name="c3")
    model.addConstrs((gp.quicksum(y[i, t] for i in I) <= x[t] for t in T if t != 6), name="c4")

    # Solve
    model.optimize()

    return {
        "objval": model.objVal,
        "x": [x[t].x for t in T],
        "y": [[y[i, t].x for t in T] for i in I]
    }


def solve_min_shipping_cost(instance):
    """
    Return optimal shipping for minimum expected total cost
    """
    E, F, S, D, c_exp, mu_exp, su, de = instance

    # Create model
    model = gp.Model("Min_Shipping_Cost")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(E, vtype=GRB.INTEGER, name="x", lb=0)

    # Set objective function
    obj_fn = gp.quicksum(c_exp[e] * x[e] for e in E)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraints
    for e in E:
        x[e].ub = mu_exp[e]
    model.addConstrs((
        gp.quicksum(x[f, d] for f in F) - gp.quicksum(x[d, s] for s in S) == 0
        for d in D), name="c1"
    )
    model.addConstrs((gp.quicksum(x[f, d] for d in D) <= su[f]for f in F), name="c2")
    model.addConstrs((gp.quicksum(x[d, s] for d in D) >= de[s]for s in S), name="c3")

    # Solve
    model.optimize()

    return {
        "objval": model.objVal,
        "x": [x[e].x for e in E]
    }


def solve_sudoku(instance):
    """
    Return optimal solution for sudoku
    """
    N, B, a = instance
    
    # Create model
    model = gp.Model("Sudoku")
    
    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(N, N, N, vtype=GRB.BINARY, name="x", lb=0)

    # Set objective function
    model.setObjective(0, GRB.MINIMIZE)

    # Add constraints
    model.addConstrs(
        (gp.quicksum(x[i, j, n] for n in N) == 1 for i in N for j in N),
        name="c1"
    )
    model.addConstrs(
        (gp.quicksum(x[i, j, n] for i in N) <= 1 for j in N for n in N),
        name="c2"
    )
    model.addConstrs(
        (gp.quicksum(x[i, j, n] for j in N) <= 1 for i in N for n in N),
        name="c3"
    )
    model.addConstrs(
        (gp.quicksum(x[i, j, n] for (i, j) in B[k]) <= 1 for k in N for n in N),
        name="c4"
    )
    for i, j, n in product(N, N, N):
        x[i, j, n].lb = a[(i, j, n)]

    # Solve
    model.optimize()

    return {
        'x': {(i, j): n + 1 for i, j, n in product(N, N, N) if x[i, j, n].X >= 0.5}
    }