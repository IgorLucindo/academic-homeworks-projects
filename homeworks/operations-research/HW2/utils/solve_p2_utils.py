from gurobipy import Model, GRB, LinExpr


class MasterSubproblemModel:
    def __init__(self, time_limit=3600):
        self.model = Model("master subproblem model")
        self.model.setParam("time limit", time_limit)  # Set 1-hour time limit if needed
        self.x = self.model.addVar(lb=0, ub=1, vtype=GRB.CONTINUOUS, name="x")  # Decision variable
        self.model.setObjective(self.x, GRB.MINIMIZE)  # Objective function
    

    def lazy_callback(self, model, where):
        """Gurobi callback for adding lazy constraints dynamically."""
        if where == GRB.Callback.MIPSOL:
            x_val = model.cbGetSolution(self.x)  # Get current x solution
            
            # Solve subproblem for the given x_val
            y_val, violation = self.solve_subproblem(x_val)
            
            if violation > 1e-5:  # If constraint violated, add lazy cut
                lhs = LinExpr()  # Define left-hand side of constraint
                lhs += self.x  # Modify based on subproblem structure
                
                # Add the lazy constraint: example form lhs ≤ y_val
                model.cbLazy(lhs <= y_val)
                print(f"Added Lazy Constraint: {lhs} <= {y_val}")


    def solve_subproblem(self, x_val):
        """Solve the subproblem given x_val and return y_val and violation."""
        subproblem = Model("Subproblem")
        subproblem.setParam("OutputFlag", 0)  # Suppress output
        
        y = subproblem.addVar(lb=0, vtype=GRB.CONTINUOUS, name="y")  # Subproblem variable
        subproblem.setObjective(y + 2 * x_val, GRB.MINIMIZE)
        subproblem.addConstr(y >= x_val, "SubConstraint")  # Example constraint
        
        subproblem.optimize()
        y_val = y.X
        violation = max(0, x_val - y_val)  # Check if constraint is violated
        return y_val, violation


    def solve(self):
        """Solve the master problem with lazy constraint callback."""
        self.model.optimize(self.lazy_callback)  # Attach callback
        return self.x.X  # Return optimal solution

