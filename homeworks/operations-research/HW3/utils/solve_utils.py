import gurobipy as gp
from gurobipy import GRB
from itertools import product
from utils.instance_utils import *


# model for solving the n queens problem
def solve_n_queens(n):
    # set parameters
    N = range(n)
    D = get_diagonals_set(n)

    # create model problem model
    model = gp.Model("N_Queens_Problem")

    # suppress output
    model.setParam("OutputFlag", 0)

    # add decision variables
    x = model.addVars(N, N, vtype=GRB.BINARY, name="x")

    # set objective function
    model.setObjective(0, GRB.MINIMIZE)

    # add constraints
    model.addConstrs((gp.quicksum(x[i, j] for i in N) <= 1 for j in N), name="c1")
    model.addConstrs((gp.quicksum(x[i, j] for j in N) <= 1 for i in N), name="c2")
    model.addConstrs((gp.quicksum(x[i, j] for i, j in d) <= 1 for d in D), name="c3")
    model.addConstr(gp.quicksum(x[i, j] for i, j in product(N, N)) == n, name="c4")

    # solve
    model.optimize()

    # return solution
    return [(i, j) for i, j in product(N, N) if x[i, j].x > 0.5]