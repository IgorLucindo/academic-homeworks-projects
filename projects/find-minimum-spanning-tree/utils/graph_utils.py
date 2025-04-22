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

    # Add weights attributes
    weights = {e: random.randint(1, 10) for e in G.edges()}
    nx.set_edge_attributes(G, weights, 'weight')

    return G


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
        edge_labels = nx.get_edge_attributes(G, 'weight')

        # Get position for every graph
        pos = nx.spring_layout(G)

        # Draw graph
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, width=2, ax=axes[i])

        # Draw labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=axes[i])

    axes[0].set_title(f"Graph")
    axes[1].set_title(f"Minimum Spanning Tree")
    axes[2].set_title(f"NX Minimum Spanning Tree")

    # Show figure
    plt.tight_layout()
    plt.show()