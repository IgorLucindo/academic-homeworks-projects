import networkx as nx
import matplotlib.pyplot as plt


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