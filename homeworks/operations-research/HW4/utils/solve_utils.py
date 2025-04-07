import gurobipy as gp
from gurobipy import GRB
from itertools import product


def solve_shortest_path(G):
    """
    Return solution for shortest path using backward induction
    """