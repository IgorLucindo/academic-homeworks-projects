import networkx as nx
import numpy as np
import random


def network_generator(n, m):
    """
    Return random graph
    """
    # create complete graph
    G = nx.complete_graph(n)
    
    edges = list(G.edges())
    random.shuffle(edges)
    
    # removes valid edges
    while G.number_of_edges() > m:
        u, v = edges.pop()
        G.remove_edge(u, v)

        # make sure edge is valid
        if not nx.is_connected(G) or any(d == 1 for _, d in G.degree()):
            G.add_edge(u, v)

    # rename s and t vertices
    G = nx.relabel_nodes(G, {0: 't'})

    return G


def get_random_graphs(n, m, num_graphs):
    """
    Return list of random graphs
    """
    return [network_generator(n, m) for _ in range(num_graphs)]


def create_grid_world():
    """
    Return grid instance for grid world
    """
    return np.array([
        [0, 0, 0, 1],
        [0, np.nan, 0, -100],
        [0, 0, 0, 0]
    ])