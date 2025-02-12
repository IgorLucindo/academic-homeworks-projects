import gurobipy as gp
from gurobipy import GRB
import networkx as nx
from utils import *


# create graphs
G, H = non_isomorphs_graphs()
# G, H = isomorphs_graphs()
H_complement = nx.complement(H)

# create model
model = gp.Model(name="model")

# add variables
x = model.addVars(G.nodes, H.nodes, vtype=GRB.BINARY, name='x')

# objective functiom
model.setObjective(0, GRB.MINIMIZE)

# add constraints
model.addConstrs((gp.quicksum(x[u, v] for v in H.nodes) == 1 for u in G.nodes), name='c1')
model.addConstrs((gp.quicksum(x[u, v] for u in G.nodes) == 1 for v in H.nodes), name='c2')
model.addConstrs((x[u1, v1] + x[u2, v2] + x[u1, v2] + x[u2, v1] <= 1
                 for (u1, u2) in G.edges for (v1, v2) in H_complement.edges), name='c3')

# solve
model.optimize()

# print results if feasible
if model.status != 3:
    print('Objective function value: %f' % model.objVal)
    for var in model.getVars():
        print('%s: %g' % (var.varName, var.x))

# show graphs
show_graphs([G, H])