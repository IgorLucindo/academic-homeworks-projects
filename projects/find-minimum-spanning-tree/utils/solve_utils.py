from utils.calculation_utils import *
import networkx as nx
import gurobipy as gp
from gurobipy import GRB


def solve_minimum_spanning_tree(G):
    """
    MIP formulation for solving minimum spanning tree
    Return Tree graph
    """
    # Set Parameters
    S = [{
            'edges': [e for e in G.edges if e[0] in s and e[1] in s],
            'n': len(s)
         }
         for s in get_subsets(G.nodes) if len(s) > 1
    ]
    
    # Create model problem model
    model = gp.Model("Minimum_Spanning_Tree")

    # Suppress output
    model.setParam("OutputFlag", 0)

    # Enable lazy constraints
    model.setParam(GRB.Param.LazyConstraints, 1)

    # Add decision variables
    x = model.addVars(G.edges, vtype=GRB.BINARY, name="x")
    # x = model.addVars(G.edges, vtype=GRB.CONTINUOUS, name="x")

    # Set objective function
    model.setObjective(gp.quicksum(G.edges[e]['weight'] * x[e] for e in G.edges), GRB.MINIMIZE)

    # Add constraints
    model.addConstr(gp.quicksum(x[e] for e in G.edges) == len(G.nodes) - 1, name="c1")
    
    def lazy_callback(model, where):
        if where != GRB.Callback.MIPSOL: return

        # Get the current solution
        x_vals = model.cbGetSolution(x)

        # Build subgraph from selected edges
        selected_edges = [e for e in G.edges if x_vals[e] > 0.5]
        subgraph = G.edge_subgraph(selected_edges).copy()
        subgraph.add_nodes_from(G.nodes)

        # Only add lazy constraints if the subgraph is disconnected
        if nx.number_connected_components(subgraph) <= 1: return

        # Add a lazy constraint for each connected component
        for component in nx.connected_components(subgraph):
            interior_edges = list(nx.edge_boundary(G, component, component))
            if len(interior_edges) < len(component): continue

            model.cbLazy(gp.quicksum(x[e] for e in interior_edges) <= len(component) - 1)

    # Solve
    model.optimize(lazy_callback)

    if model.Status == 3: return nx.Graph()
    return G.edge_subgraph([e for e in G.edges if x[e].X > 0.5])