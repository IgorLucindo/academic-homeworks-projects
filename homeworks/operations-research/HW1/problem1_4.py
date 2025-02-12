from utils.graph_utils import *
from utils.solve_utils import *


# generate network graph and get attributes
G = network_generator(5, 8)

# solve max flow
model = max_flow_solver(G)

# print results
print('Objective function value: %f' % model.objVal)
for var in model.getVars():
    print('%s: %g' % (var.varName, var.x))

# plot graph
show_graph(G)