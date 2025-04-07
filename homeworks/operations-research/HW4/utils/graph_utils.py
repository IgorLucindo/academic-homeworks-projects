import networkx as nx
import matplotlib.pyplot as plt
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


def show_graphs(graphs, plot_flag=True):
    """
    Plot graphs in a list of graphs
    """
    if not plot_flag: return

    # Number of graphs
    num_graphs = len(graphs)

    # Create subplots
    _, axes = plt.subplots(1, num_graphs, figsize=(5 * num_graphs, 5))

    # If there's only one graph, axes will not be an array, so we wrap it in a list
    if num_graphs == 1:
        axes = [axes]

    # Iterate over the graphs and draw them
    for i, G in enumerate(graphs):
        # Get position for every graph
        pos = nx.spring_layout(G)

        # Draw graph
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, width=2, ax=axes[i])
        axes[i].set_title(f"Graph {i + 1}")

    # Show figure
    plt.tight_layout()
    plt.show()