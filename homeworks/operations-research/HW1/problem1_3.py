from utils.graph_utils import *


# generate network graphs
G1 = network_generator(5, 8)
G2 = network_generator(4, 5)
G3 = network_generator(3, 3)

# show graphs
show_graph(G1)
show_graph(G2)
show_graph(G3)