from utils.graph_utils import *
from utils.solve_utils import *


# parameter flags
flags = {
    'plot': True
}


def main():
    # Get graphs
    graphs = get_random_graphs(n=8, m=13, num_graphs=1)

    for G in graphs:
        # Solve shortest path
        paths = solve_shortest_paths(G)
        print(f"path: {paths}")

    show_graphs(graphs, flags['plot'])


if __name__ == "__main__":
    main()