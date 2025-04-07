from utils.graph_utils import *
from utils.solve_utils import *


# parameter flags
flags = {
    'plot': True
}


def main():
    # Get graphs
    graphs = get_random_graphs(n=5, m=8, num_graphs=1)

    for G in graphs:
        # Solve shortest path
        # solve_shortest_path(G)
        pass

    show_graphs(graphs, flags['plot'])


if __name__ == "__main__":
    main()