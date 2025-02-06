import gurobipy as gp
from gurobipy import GRB
from utils import *


# generate network graph and get attributes
G = network_generator(5, 8)