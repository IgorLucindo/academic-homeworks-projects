import networkx as nx
import gurobipy as gp
from gurobipy import GRB


# solve max flow
def max_flow_solver(G):
    # vertices
    nodes = list(G.nodes)
    # edges
    edges = list(G.edges)
    # capacities
    c = nx.get_edge_attributes(G, 'capacity')
    # vertices minus s and t
    nodes_minus_st = [x for x in nodes if x not in ['s', 't']]

    # create model
    model = gp.Model(name="max-flow")

    # set variables
    x = model.addVars(edges, lb=0, name='x')

    # define objective function
    delta_plus_s = list(G.successors('s'))
    obj_fn = gp.quicksum(x['s', j] for j in delta_plus_s)
    model.setObjective(obj_fn, GRB.MAXIMIZE)

    # add constraints
    model.addConstrs((x[e] <= c[e] for e in edges), name = 'c1')
    model.addConstrs((gp.quicksum(x[j, i] for j in list(G.predecessors(i))) == gp.quicksum(x[i, j] for j in list(G.successors(i)))
                      for i in nodes_minus_st), name = 'c2')

    # solve
    model.optimize()

    # return model
    return model


# solve min cut
def min_cut_solver(G):
    # vertices
    nodes = list(G.nodes)
    # edges
    edges = list(G.edges)
    # capacities
    c = nx.get_edge_attributes(G, 'capacity')

    # create model
    model = gp.Model(name="min-cut")

    # set variables
    v = model.addVars(edges, lb=0, name='v')
    u = model.addVars(nodes, name='u')

    # define objective function
    obj_fn = gp.quicksum(v[e] * c[e] for e in edges)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    model.addConstrs((u[e[0]] - u[e[1]] <= v[e] for e in edges), name = 'c1')
    model.addConstr(u['s'] == 1, name = 'c2')
    model.addConstr(u['t'] == 0, name = 'c3')

    # solve
    model.optimize()

    # return model
    return model


# solve min ships
def min_ship_solver(num_of_cargoes, DD, PO, PD, sailing_time, M):
    # variables
    S = range(num_of_cargoes)
    C = range(num_of_cargoes)

    # create model
    model = gp.Model(name="min-ships")

    # set variables
    x = model.addVars(S, C, vtype=GRB.BINARY, name='x')
    y = model.addVars(S, vtype=GRB.BINARY, name='y')

    # define objective function
    obj_fn = gp.quicksum(y[s] for s in S)
    model.setObjective(obj_fn, GRB.MINIMIZE)

    # add constraints
    model.addConstrs((DD[j] - DD[i] - sailing_time[PO[i]][PD[i]] - sailing_time[PO[j]][PD[i]] >= M*(x[s, i] + x[s, j] - 2)
                    for i in C for j in C if j > i for s in S), name='c1')
    model.addConstrs((gp.quicksum(x[s, i] for s in S) == 1 for i in C), name = 'c2')
    model.addConstrs((x[s, i] <= y[s] for i in C for s in S), name = 'c3')

    # solve
    model.optimize()

    # return model
    return model