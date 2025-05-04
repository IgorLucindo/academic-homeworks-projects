import gurobipy as gp
from gurobipy import GRB
from itertools import product
import numpy as np


def solve_shipping(instance):
    """
    Return optimal shipping for minimum expected total cost
    """
    s, S, beta, cost = instance
    mean = np.mean(cost, axis=0)
    sigma = np.cov(cost, rowvar=False)

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


def solve_shipping_min_CVaR(instance):
    """
    Return optimal shipping for minimum CVaR
    """
    s, S, beta, cost = instance
    sigma = np.cov(cost, rowvar=False)
    N = range(len(cost))

    # Create model
    model = gp.Model("Solve_Shipping_Min_CVaR")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(S, vtype=GRB.INTEGER, lb=0, name="x")
    alpha = model.addVar(vtype=GRB.CONTINUOUS, name="alpha")
    w = model.addVars(N, vtype=GRB.CONTINUOUS, lb=0, name="w")

    # Set objective function
    obj_fn = alpha + gp.quicksum(w[n] for n in N) / 0.05 / len(N)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraints
    model.addConstrs((w[n] >= gp.quicksum(x[i] * cost[n, i] for i in S) for n in N), name="c1")
    model.addConstr(gp.QuadExpr(sum(x[i] * sigma[i, j] * x[j] for i, j in product(S, S))) <= beta, name="c2")
    model.addConstrs((x[i] <= s[i] for i in S), name="c3")
    model.addConstr(gp.quicksum(x[i] for i in S) == 150, name="c4")

    # Solve
    model.optimize()

    return [x[i].X for i in S]


def solve_ordering(instance):
    """
    Return optimal order
    """
    S, C, a, c, d = instance
    Xi = range(len(d))

    # Create model
    model = gp.Model("Solve_Ordering")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(S, C, vtype=GRB.INTEGER, lb=0, name="x")
    y = model.addVars(C, Xi, vtype=GRB.INTEGER, lb=0, name="y")

    # Set objective function
    obj_fn = gp.quicksum(c[i] * x[i, j] for i in S for j in C) + \
             (1 / len(Xi)) * gp.quicksum(2 * y[j, xi] for j in C for xi in Xi)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraints
    model.addConstrs((gp.quicksum(x[i, j] for i in S) + y[j, xi] >= d[xi, j] for j in C for xi in Xi), name="c1")
    model.addConstrs((x[i, j] <= a[i, j] for i in S for j in C), name="c2")

    # Solve
    model.optimize()

    return [[x[i, j].X for i in S] for j in C]