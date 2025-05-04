from utils.instance_utils import *
from utils.graph_utils import *
from utils.solve_utils import *


# Set parameter flags
flags = {
    'plot': True
}


def main():
    # Get instance
    instance = get_financial_stock_assets()
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]

    for t in thresholds:
        # Create graph based on instance
        G = get_financial_correlation_graph(instance, t)

        # Solve optimal portifolio
        selected_assets, avg_corr = solve_max_indep_set_min_correlation(G, instance)

        # Relabel vertices
        G = relabel_vertices(G, instance[0])

        print(selected_assets, avg_corr)

        # Show graphs
        show_graphs([G], flags['plot'])


if __name__ == "__main__":
    main()