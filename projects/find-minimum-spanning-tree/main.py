from utils.graph_utils import *
from utils.solve_utils import *


# Set parameter flags
flags = {
    'plot': True
}


def main():
    # Get random connected graph
    G = network_generator(n=8, m=13)

    # Solve minimum spanning tree
    H = solve_minimum_spanning_tree(G)

    T = nx.minimum_spanning_tree(G)

    # Show graphs
    show_graphs([G, H, T], flags['plot'])


if __name__ == "__main__":
    main()