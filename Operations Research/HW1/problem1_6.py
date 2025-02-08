from utils.graph_utils import *
from utils.solve_utils import *


# generate network graph and get attributes
G = network_generator(5, 8)

# solve max flow
model1 = max_flow_solver(G)
# solve min cut
model2 = min_cut_solver(G)

# print results
print('Max-flow - objective function value: %f' % model1.objVal)
for var in model1.getVars():
    print('%s: %g' % (var.varName, var.x))
print('\nMin-cut - objective function value: %f' % model2.objVal)
for var in model2.getVars():
    print('%s: %g' % (var.varName, var.x))

# plot graph
show_graph(G)