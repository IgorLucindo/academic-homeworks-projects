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
                if sub_prob_obj_val == -GRB.INFINITY:
                    model.cbLazy(gp.quicksum((self.a[i, j] + xi[i])*self.x[i, j] for i in self.S) >= 0)


    # solve using master subproblem method
    def solve(self):
        self.master.setParam(GRB.Param.LazyConstraints, 1)
        self.master.optimize(self.lazy_callback)

        # return optimal solution, objective funciton value and optimality gap
        return [self.x[i, j].X for i in self.S for j in self.C], self.master.objVal, self.master.MIPGap