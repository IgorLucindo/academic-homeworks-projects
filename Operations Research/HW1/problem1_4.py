import gurobipy as gp
from gurobipy import GRB
from utils import *


# generate network graph and get attributes
G = network_generator(5, 8)
# vertices
nodes = list(G.nodes)
# edges
edges = list(G.edges)
# capacities
c = nx.get_edge_attributes(G, 'capacity')
# vertices minus s and t
nodes_minus_st = [x for x in nodes if x not in ['s', 't']]


# create model
model = gp.Model(name="primal max-flow")

# set variables
x = model.addVars(edges, lb=0, name='x')

# define objective function
delta_plus_s = list(G.successors('s'))
obj_fn = sum(x['s', j] for j in delta_plus_s)
model.setObjective(obj_fn, GRB.MAXIMIZE)

# add constraints
model.addConstrs((x[e] <= c[e] for e in edges), name = 'c1')
model.addConstrs((sum(x[j, i] for j in list(G.predecessors(i))) == sum(x[i, j] for j in list(G.successors(i)))
                 for i in nodes_minus_st), name = 'c2')


# solve
model.optimize()
model.write("primal_maxflow.lp")

# print results
print('Objective function value: %f' % model.objVal)
for v in model.getVars():
    print('%s: %g' % (v.varName, v.x))


show_graph(G)