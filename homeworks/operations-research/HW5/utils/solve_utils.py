import gurobipy as gp
from gurobipy import GRB
from itertools import product


def solve_shipping(instance):
    """
    Return optimal shipping for minimum expected total cost
    """
    s, S, beta, mean, sigma = instance

    # Create model
    model = gp.Model("Solve_Shipping")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(S, vtype=GRB.INTEGER, lb=0, name="x")

    # Set objective function
    obj_fn = gp.quicksum(x[i] * mean[i] for i in S)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraints
    model.addConstr(gp.QuadExpr(sum(x[i] * sigma[i, j] * x[j] for i, j in product(S, S))) <= beta, name="c1")
    model.addConstrs((x[i] <= s[i] for i in S), name="c2")
    model.addConstr(gp.quicksum(x[i] for i in S) == 150, name="c3")

    # Solve
    model.optimize()

    return [x[i].X for i in S]