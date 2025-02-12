import networkx as nx
import matplotlib.pyplot as plt


# create non isomorphs graphs
def non_isomorphs_graphs():
    # create G
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4), (5, 6), (6, 7), (7, 8), (5, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # create H
    H = nx.Graph()
    H.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (1, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # return graphs
    return G, H


# create isomorphs graphs
def isomorphs_graphs():
    # create G
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4), (5, 6), (6, 7), (7, 8), (5, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # create H
    H = nx.Graph()
    H.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'd'), ('e', 'f'), ('f', 'g'), ('g', 'h'), ('e', 'h'), ('a', 'e'), ('b', 'f'), ('c', 'g'), ('d', 'h')])

    # return graphs
    return G, H


# show graphs
def show_graphs(graphs):
    # number of graphs
    num_graphs = len(graphs)
    # create subplots
    _, axes = plt.subplots(1, num_graphs, figsize=(5 * num_graphs, 5))

    # if there's only one graph, axes will not be an array, so we wrap it in a list
    if num_graphs == 1:
        axes = [axes]

    # iterate over the graphs and draw them
    for i, G in enumerate(graphs):
        pos = nx.spring_layout(G)  # Compute positions for the graph
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, width=2, ax=axes[i])
        axes[i].set_title(f"Graph {i + 1}")  # Set title for each subplot

    # show the figure
    plt.tight_layout()
    plt.show()