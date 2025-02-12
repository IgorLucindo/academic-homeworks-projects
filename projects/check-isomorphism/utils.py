import networkx as nx
import matplotlib.pyplot as plt


# create non isomorphs graphs
def non_isomorphs_graphs():
    # create G
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4), (5, 6), (6, 7), (7, 8), (5, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # create H
    H = nx.Graph()
    H.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (1, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # return graphs
    return G, H


# create isomorphs graphs
def isomorphs_graphs():
    # create G
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4), (5, 6), (6, 7), (7, 8), (5, 8), (1, 5), (2, 6), (3, 7), (4, 8)])

    # create H
    H = nx.Graph()
    H.add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'd'), ('e', 'f'), ('f', 'g'), ('g', 'h'), ('e', 'h'), ('a', 'e'), ('b', 'f'), ('c', 'g'), ('d', 'h')])

    # return graphs
    return G, H


# show graph
def show_graph(G):
    pos = nx.spring_layout(G)

    # draw graph
    nx.draw(G, pos, with_labels=True)
    
    # show
    plt.show()