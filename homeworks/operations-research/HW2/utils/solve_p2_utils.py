import gurobipy as gp
from gurobipy import GRB


# master subproblem method for solving semi-infinite 
class MasterSubproblemMethod:
    def __init__(self, instance, time_limit=3600):
        # set attributes
        self.S, self.C, self.a, self.c, self.d = instance

        # create master problem model
        self.master = gp.Model("master")

        # suppress output
        self.master.setParam("OutputFlag", 0)

        # 1 hour time limit for solving
        self.master.setParam("TimeLimit", time_limit)

        # add variables
        self.x = self.master.addVars(self.S, self.C, vtype=GRB.BINARY, name="x")

        # set the objective function
        obj_fn = gp.quicksum(self.c[i] * self.x[i, j] for i in self.S for j in self.C)
        self.master.setObjective(obj_fn, GRB.MINIMIZE)



    # solve subproblem
    def solve_subproblem(self, x, j):
        # create subproblem model
        subproblem = gp.Model("subproblem")

        # suppress output
        subproblem.setParam("OutputFlag", 0)
        
        # add variables
        xi = subproblem.addVars(self.S, vtype=GRB.CONTINUOUS, name="xi")

        # set the objective function
        obj_fn = gp.quicksum((self.a[i, j] + xi[i])*x[i, j] for i in self.S)
        subproblem.setObjective(obj_fn, GRB.MINIMIZE)
        subproblem.addConstr(gp.quicksum(xi[i]**2 for i in self.S) <= 1, "c1")
        
        # solve subproblem
        subproblem.optimize()

        # return solution and value of objective function
        return [xi[i].X for i in self.S], subproblem.objVal
    

    def lazy_callback(self, model, where):
        # add lazy constraints
        if where == GRB.Callback.MIPSOL:
            # get current x solution
            x = model.cbGetSolution(self.x)
            
            # iterate for every constraint
            for j in self.C:
                # solve subproblem
                xi, sub_prob_obj_val = self.solve_subproblem(x, j)

                # add lazy constraints if solution is infeasible to master problem
                if sub_prob_obj_val < self.d[j]:
                    model.cbLazy(gp.quicksum((self.a[i, j] + xi[i])*self.x[i, j] for i in self.S) >= self.d[j])


    # solve using master subproblem method
    def solve(self):
        self.master.setParam(GRB.Param.LazyConstraints, 1)
        self.master.optimize(self.lazy_callback)

        # return optimal solution, objective funciton value, running time and optimality gap
        return [[self.x[i, j].X for i in self.S] for j in self.C], self.master.objVal, self.master.Runtime, self.master.MIPGap
    

# solve using the formulation found using the dualization method
def dualization_solver(instance, time_limit=3600):
    # get instance
    S, C, a, c, d = instance

    # create model
    model = gp.Model("dualization")

    # suppress output
    model.setParam("OutputFlag", 0)

    # 1 hour time limit for solving
    model.setParam("TimeLimit", time_limit)

    # add variables
    x = model.addVars(S, C, vtype=GRB.BINARY, name="x")
    u = model.addVar(vtype=GRB.CONTINUOUS, lb=0, name="u")

    # set the objective function
    obj_fn = gp.quicksum(c[i] * x[i, j] for i in S for j in C)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    model.addConstrs((gp.quicksum((a[i, j] - x[i, j]/4/u)*x[i, j] for i in S) - u >= d[j] for j in C), name="c1")

    # solve
    model.optimize()

    # return optimal solution, objective funciton value, running time and optimality gap
    return [[x[i, j].X for i in S] for j in C], model.objVal, model.Runtime, model.MIPGap