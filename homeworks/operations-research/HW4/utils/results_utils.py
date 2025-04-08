import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from itertools import product
import numpy as np


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

    
def show_grid(grid, plot_flag=True):
    """
    Plot grid world
    """
    if not plot_flag: return

    rows, cols = grid.shape
    fig, ax = plt.subplots()

    # Create a white colormap (all values mapped to white)
    white_cmap = ListedColormap(["white"])

    # Plot the grid with the white colormap
    ax.imshow(np.nan_to_num(grid, nan=0), cmap=white_cmap)

    # Grid lines
    ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
    ax.tick_params(which='minor', size=0)
    ax.set_xticks([])
    ax.set_yticks([])

    # Walls and text
    for i, j in product(range(rows), range(cols)):
        val = grid[i, j]
        if np.isnan(val):
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='black'))
            continue

        ax.text(j, i, str(int(val)), ha='center', va='center', color='black', fontsize=12)
        if val > 0:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='#44AA44'))
        elif val < 0:
            ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='#FF4444'))

    plt.title("GridWorld")
    plt.show()