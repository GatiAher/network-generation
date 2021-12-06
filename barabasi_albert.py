"""
Produce an undirected Barabasi-Albert network of size N with 

Author: Mira Flynn
Date: Dec 6, 2021

TODO: fill this in
Source: pseudocode from xxx by xxx

"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np

frameData = []

def generate_ba_graph(n = 10, m = 3):
    g = nx.empty_graph(n = n)
    pos = nx.circular_layout(g)
    g = nx.complete_graph(m)
    for i in range(m, n):
        nodes, weights = list(zip(*g.degree()))
        weights = [w/sum(weights) for w in weights]
        chosen_nodes = np.random.choice(nodes, size = m, p = weights, replace=False)
        node_colors = ['k' for i in range(len(g.nodes()))]
        node_colors.append('r')
        g.add_node(i)
        frameData.append((g.copy(), pos, node_colors, 'k', 50, False))
        for n in chosen_nodes:
            g.add_edge(n, i)
            edge_colors = ['r' if (e[0] == i or e[1] == i) else 'k' for e in g.edges]
            frameData.append((g.copy(), pos, node_colors, edge_colors, 50, False))
    frameData.append((g.copy(), pos, 'k', 'k', 50, False))
    return g

def animate(i):
        if(i < len(frameData)):
            plt.clf()
            g, pos, node_color, edge_color, node_size, with_labels = frameData[i]
            nx.draw_networkx(G = g, pos = pos, node_color = node_color, edge_color = edge_color, node_size = node_size, with_labels = with_labels)
            artists = plt.findobj()
            # print(artists)
            plt.xlim(-1.1,1.1)
            plt.ylim(-1.1,1.1)
            return artists
        else:
            return None

def do_animation():
    fig, ax = plt.subplots()
    frameData = []
    generate_ba_graph()
    ani = animation.FuncAnimation(
        fig, animate, interval=200, blit=False, save_count=500)
    plt.show()

do_animation()