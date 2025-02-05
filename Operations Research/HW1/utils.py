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

    # rename s and t vertices
    G = relabel_nodes_special(G, n)

    # transform to a directed graph
    G = G.to_directed()

    # add capacities
    capacities = {e: random.randint(10, 20) for e in G.edges()}
    nx.set_edge_attributes(G, capacities, 'capacity')

    # return the connected graph
    return G


# rename vertices to s and t
def relabel_nodes_special(G, n):
    node_s = next((node for node in G.nodes if G.degree[node] < n-1), None)
    
    # Create a mapping for relabeling
    if node_s != None:
        node_t = next((node for node in G.nodes if node != node_s and not G.has_edge(node, node_s)), None)
        G = nx.relabel_nodes(G, {node_s: 's', node_t: 't'})
    else:
        G = nx.relabel_nodes(G, {0: 's', n-1: 't'})
    
    return G


# show graph
def show_graph(G):
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    pos = nx.spring_layout(G)

    # draw capacities
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # draw graph
    nx.draw_spring(G, with_labels=True)

    # show
    plt.show()