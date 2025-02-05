from gurobipy import *

# corrigir isso
c = G.capacities ???
nodes_minus_st = nodes[(nodes != 's') & (nodes != 't')]

# create model
model = Model(name = "primal maxflow")

# set variables
x = model.addVar(name = 'x', vtype = GRB.CONTINUOUS, lb = 0)

# define objective function
delta_plus_s = list(G.successors('s'))
obj_fn = sum(x['s', j] for j in delta_plus_s)
model.setObjective(obj_fn, GRB.MAXIMIZE)

# add constraints
model.addConstrs(x[e] <= c[e] for e in edges, name = 'c1')
model.addConstrs(sum(x[j, i] for j in list(G.predecessors(i))) <= sum(x[i, j] for j in list(G.successors(i)))
                 for i in nodes_minus_st, name = 'c2')

# solve
model.optimize()
model.write("primal_maxflow.lp")

# print results
print('Objective function value: %f' % model.objVal)
for v in model.getVars():
    print('%s: %g' % (v.varName, v.x))