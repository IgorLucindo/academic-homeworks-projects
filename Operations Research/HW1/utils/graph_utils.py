import networkx as nx
import random
import matplotlib.pyplot as plt


# network graph generator
def network_generator(n, m):
    if m < n or m > n*(n-1)/2:
        raise ValueError("wrong number of edges.")
    
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

    # transform G to a directed graph D
    D = nx.DiGraph()
    for u, v in G.edges:
        D.add_edge(u, v)

    # rename s and t vertices
    D = nx.relabel_nodes(D, {0: 's', n-1: 't'})

    # add capacities
    capacities = {e: random.randint(10, 20) for e in D.edges()}
    nx.set_edge_attributes(D, capacities, 'capacity')

    # return the connected graph
    return D


# show graph
def show_graph(G):
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    pos = nx.spring_layout(G)

    # draw graph
    nx.draw(G, pos, with_labels=True)

    # draw capacities
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # show
    plt.show()