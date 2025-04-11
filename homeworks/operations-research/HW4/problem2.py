from utils.instance_utils import *
from utils.solve_utils import *
from utils.graph_utils import *


# Set parameter flags
flags = {
    'plot': True
}


def main():
    # Get random connected graphs
    graphs = get_random_graphs(n=8, m=13, num_graphs=5)

    for G in graphs:
        # Solve shortest path
        paths = solve_shortest_paths(G)
        print(f"paths: {paths}")

    show_graphs(graphs, flags['plot'])


if __name__ == "__main__":
    main()