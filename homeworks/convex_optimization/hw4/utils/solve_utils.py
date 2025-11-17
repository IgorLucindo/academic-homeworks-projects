import gurobipy as gp
from gurobipy import GRB
import time


def solve_cutting_stock_problem(instance):
    """
    Solve the cutting stock problem
    """
    L, l, d, n = instance
    N = range(n)
    M = range(len(l))

    start_time = time.time()

    # Create model
    model = gp.Model("Cutting_Stock_problem")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(N, vtype=GRB.BINARY, name="x")
    y = model.addVars(N, M, vtype=GRB.INTEGER, lb=0, name="y")

    # Set objective function
    obj_fn = gp.quicksum(x[t] for t in N)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Add constraints
    model.addConstrs((gp.quicksum(y[i, j] for i in N) >= d[j] for j in M), name="c1")
    model.addConstrs((gp.quicksum(l[j] * y[i, j] for j in M) <= L * x[i] for i in N), name="c2")

    # Solve
    model.optimize()

    return {
        "objval": model.objVal,
        "x": [x[i].x for i in N],
        "y": [[y[i, j].x for j in M] for i in N],
        "runtime": time.time() - start_time
    }


def solve_cutting_stock_problem_column_generation(instance):
    """
    Solve the cutting stock problem using column generation
    """
    L, l, d, n = instance
    M = range(len(l))
    patterns = []
    for j in M:
        p = [0] * len(l)     # FIXED (was [0] * 4)
        p[j] = L // l[j]
        patterns.append(p)

    # Subproblem
    def solve_subproblem(dual_prices):
        sp = gp.Model("subproblem")
        sp.setParam("OutputFlag", 0)

        a = sp.addVars(M, vtype=GRB.INTEGER, lb=0, name="a")
        sp.setObjective(gp.quicksum(dual_prices[j] * a[j] for j in M), GRB.MAXIMIZE)
        sp.addConstr(gp.quicksum(l[j] * a[j] for j in M) <= L)

        sp.optimize()

        if sp.Status != GRB.OPTIMAL:
            raise RuntimeError("Subproblem did not solve optimally.")

        pattern = [int(a[j].X) for j in M]
        return sp.ObjVal, pattern

    start_time = time.time()

    # Master problem
    model = gp.Model("master")
    model.Params.OutputFlag = 0

    # λ variables
    lambda_vars = []
    for k in range(len(patterns)):
        λ = model.addVar(lb=0, name=f"lambda_{k}")
        lambda_vars.append(λ)

    # Objective
    obj_fn = gp.quicksum(lambda_vars)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # Demand constraints
    demand_constr = []
    for j in M:
        c = model.addConstr(
            gp.quicksum(patterns[k][j] * lambda_vars[k] for k in range(len(patterns))) >= d[j],
            name=f"demand_{j}"
        )
        demand_constr.append(c)

    # Column Generation
    while True:
        # Solve current RMP
        model.optimize()

        # Get dual prices
        dual = [demand_constr[j].Pi for j in M]

        # Solve subproblem
        best_value, new_pattern = solve_subproblem(dual)

        # Stop condition
        reduced_cost = 1 - best_value
        if reduced_cost >= -1e-6:
            break

        # Add pattern
        patterns.append(new_pattern)

        # New λ variable
        λ = model.addVar(lb=0, name=f"lambda_{len(patterns)-1}")
        lambda_vars.append(λ)

        # Add to demand constraints
        for j in M:
            model.chgCoeff(demand_constr[j], λ, new_pattern[j])

        # FIX: update objective function
        obj_fn += λ
        model.setObjective(obj_fn)

        model.update()

    # Solve
    model.optimize()

    return {
        "objval": model.objVal,
        "runtime": time.time() - start_time
    }


def solve_investment_benders(instance, tol=1e-6, max_iter=50):
    """
    Solve the two-stage investment problem using Benders decomposition.
    """
    c, G, L, k, p = instance
    num_assets = len(c)
    num_scenarios = len(L)

    # Create master problem
    model = gp.Model("Benders_Master")
    model.setParam("OutputFlag", 0)

    # Master decision variables
    x = model.addVars(num_assets, lb=0.0, name="x")
    theta = model.addVars(num_scenarios, lb=0.0, name="theta")

    # Master objective: investment cost + expected recourse cost
    model.setObjective(
        gp.quicksum(c[i]*x[i] for i in range(num_assets)) +
        gp.quicksum(p[s]*theta[s] for s in range(num_scenarios)),
        GRB.MINIMIZE
    )

    # Full investment constraint
    model.addConstr(gp.quicksum(x[i] for i in range(num_assets)) == 1, name="full_investment")

    # Benders iterations
    for it in range(max_iter):
        model.optimize()
        x_val = [x[i].X for i in range(num_assets)]
        cuts_added = 0

        # Check subproblems for each scenario
        for s in range(num_scenarios):
            wealth = sum(G[s][i] * x_val[i] for i in range(num_assets))
            b_star = max(0.0, L[s] - wealth)
            if b_star > tol:
                # Benders cut depends on x
                model.addConstr(
                    theta[s] >= k[s] * (L[s] - gp.quicksum(G[s][i]*x[i] for i in range(num_assets))),
                    name=f"benders_cut_s{s}_iter{it}"
                )
                cuts_added += 1

        if cuts_added == 0:
            # Converged: no violated cuts
            break

    return {
        "objval": model.objVal,
        "x": [x[i].X for i in range(num_assets)],
        "theta": [theta[s].X for s in range(num_scenarios)]
    }