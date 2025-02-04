from gurobipy import *

# create model
opt_mod = Model(name = "primal maxflow")

# set variables
x = opt_mod.addVar(name = 'x', vtype = GRB.CONTINUOUS, lb = 0)

# define objective function
obj_fn = 5*x
opt_mod.setObjective(obj_fn, GRB.MAXIMIZE)

# add constraints
c1 = opt_mod.addConstr(x >= 0, name = 'c1')

# solve
opt_mod.optimize()
opt_mod.write("primal_maxflow.lp")

# print results
print('Objective function value: %f' % opt_mod.objVal)
for v in opt_mod.getVars():
    print('%s: %g' % (v.varName, v.x))