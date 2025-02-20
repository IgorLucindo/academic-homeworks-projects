import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import os

def initialize_data():
    n_suppliers = 9
    n_centers = 2
    demands = [46, 54]
    fixed_costs = [9, 11, 7, 8, 8, 13, 21, 16, 11]
    supply_matrix = np.array([
        [10, 23, 13, 4, 9, 20, 15, 6, 12],
        [3, 8, 30, 11, 6, 33, 17, 18, 9]
    ]).T
    return n_suppliers, n_centers, demands, fixed_costs, supply_matrix

def create_master_problem(n_suppliers, n_centers, fixed_costs):
    master = gp.Model("Robust_Optimization")
    x = master.addVars(n_suppliers, n_centers, vtype=GRB.BINARY, name="x")
    master.setObjective(gp.quicksum(fixed_costs[i] * x[i, j] for i in range(n_suppliers) for j in range(n_centers)), GRB.MINIMIZE)
    return master, x

def solve_subproblem(supply_matrix, solution, j, n_suppliers):
    subproblem = gp.Model("Subproblem")
    xi = subproblem.addVars(n_suppliers, lb=-GRB.INFINITY, ub=GRB.INFINITY, name="xi")
    subproblem.setObjective(gp.quicksum((supply_matrix[i, j] + xi[i]) * solution[i, j] for i in range(n_suppliers)), GRB.MINIMIZE)
    subproblem.addConstr(gp.quicksum(xi[i] * xi[i] for i in range(n_suppliers)) <= 1)
    subproblem.setParam(GRB.Param.OutputFlag, 0)
    subproblem.optimize()
    return subproblem.objVal, {i: xi[i].X for i in range(n_suppliers)}

def lazy_callback(model, where, n_suppliers, n_centers, supply_matrix, demands):
    if where == GRB.Callback.MIPSOL:
        solution = model.cbGetSolution(model._x)
        
        for j in range(n_centers):
            worst_case_supply, xi_values = solve_subproblem(supply_matrix, solution, j, n_suppliers)
            
            if worst_case_supply < demands[j]:
                model.cbLazy(gp.quicksum((supply_matrix[i, j] + xi_values[i]) * model._x[i, j] for i in range(n_suppliers)) >= demands[j])
            if worst_case_supply == -GRB.INFINITY:
                model.cbLazy(gp.quicksum((supply_matrix[i, j] + xi_values[i]) * model._x[i, j] for i in range(n_suppliers)) >= 0)

def save_solution_to_csv(x, n_suppliers, n_centers, optimal_value, run_time, optimality_gap, filename="Supplier-Center_Master-Sub_Solution.csv"):
    solution_data = [["Optimal Value", optimal_value],
                     ["Running Time (seconds)", run_time],
                     ["Optimality Gap", optimality_gap]]
    
    for i in range(n_suppliers):
        for j in range(n_centers):
            if x[i, j].x > 0.5:
                solution_data.append([i+1, j+1])
    
    df = pd.DataFrame(solution_data, columns=["Supplier", "Distribution Center"])
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    df.to_csv(file_path, index=False)
    print(f"Solution saved to {file_path}")

def solve_robust_optimization():
    n_suppliers, n_centers, demands, fixed_costs, supply_matrix = initialize_data()
    master, x = create_master_problem(n_suppliers, n_centers, fixed_costs)
    master._x = x
    master.setParam(GRB.Param.LazyConstraints, 1)
    master.optimize(lambda model, where: lazy_callback(model, where, n_suppliers, n_centers, supply_matrix, demands))
    
    optimal_value = master.objVal if master.status == GRB.OPTIMAL else None
    run_time = master.Runtime
    optimality_gap = master.MIPGap if master.status in [GRB.OPTIMAL, GRB.SUBOPTIMAL] else None
    
    print(f"Optimal Value: {optimal_value}")
    print(f"Running Time: {run_time} seconds")
    print(f"Optimality Gap: {optimality_gap}%")
    
    if master.status == GRB.OPTIMAL:
        save_solution_to_csv(x, n_suppliers, n_centers, optimal_value, run_time, optimality_gap)

if __name__ == "__main__":
    solve_robust_optimization()
