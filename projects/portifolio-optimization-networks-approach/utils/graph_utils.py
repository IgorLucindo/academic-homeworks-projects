import networkx as nx
import matplotlib.pyplot as plt


def get_financial_correlation_graph(instance, threshold=0.5):
    """
    Returns an undirected graph representing correlated financial assets
    """
    assets, correlation_matrix, asset_pairs = instance
    
    # Create graph
    G = nx.Graph()

    # Add vertices
    G.add_nodes_from(range(len(assets)))

    # Add edges
    edges_to_add = {
        (i, j) for i, j in asset_pairs if correlation_matrix[i, j] > threshold
    }
    G.add_edges_from(edges_to_add)

    return G


def relabel_vertices(G, labels):
    label_mapping = {i: labels[i] for i in G.nodes}
    return nx.relabel_nodes(G, label_mapping)


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
        pos = nx.spring_layout(G, k=1)

        # Draw graph
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1400, width=2, ax=axes[i])

        # Draw labels
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=axes[i])

        # Draw title
        axes[i].set_title(f"Graph {i}")

    # Show figure
    plt.tight_layout()
    plt.show()