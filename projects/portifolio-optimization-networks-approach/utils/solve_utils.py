import gurobipy as gp
from gurobipy import GRB


def solve_max_indep_set_min_correlation(G, instance):
    """
    MIP formulation for maximum independent set with min correlation
    Return optimal portifolio and average_corr
    """
    assets, correlation_matrix, asset_pairs = instance

    # Create model
    model = gp.Model("Max_Indep_Set_Min_Corr")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Add decision variables
    x = model.addVars(G.nodes, vtype=GRB.BINARY, name="x")
    y = model.addVars(G.nodes, G.nodes, vtype=GRB.BINARY, name="y")

    # Set objective function
    obj_fn = gp.quicksum(x[i] for i in G.nodes) - gp.quicksum(correlation_matrix[i, j] * y[i, j] for i, j in asset_pairs) / len(asset_pairs)
    model.setObjective(obj_fn, GRB.MAXIMIZE)

    # Add constraints
    model.addConstrs((x[i] + x[j] <= 1 for i, j in G.edges), name="c1")
    model.addConstrs((y[i, j] >= x[i] + x[j] - 1 for i, j in asset_pairs), name="c2")
    
    # Solve
    model.optimize()

    return extract_output(G, x, assets, correlation_matrix)


def extract_output(G, x, assets, correlation_matrix):
    """
    Extracts a selected portfolio based on optimization results, computes
    the average pairwise correlation within the portfolio (weighted by _lambda).
    """
    # Get selected asset indices from solution variables
    selected_indices = [i for i in G.nodes if x[i].X > 0.5]
    pairs = {(i, j) for idx, i in enumerate(selected_indices) for j in selected_indices[idx + 1:]}

    # Map indices to asset names
    selected_assets = [assets[i] for i in selected_indices]

    # Calculate the average pairwise correlation for selected assets
    avg_corr = sum(correlation_matrix[i, j] for i, j in pairs) / len(pairs)

    return selected_assets, avg_corr