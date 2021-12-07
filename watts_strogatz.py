import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math, random

frameData = [] # data for each frame, will be put into nx.draw()

def watts_strogatz(N=8, K=4, P=0.8, draw_flag=False):
    """
    Produce a undirected Watts-Strogatz (small-world topography) of size N.
    The generative algorithm creates a ring lattice, and then, for each node, 
    randomly rewires some of the node's edges.  

    Arguments:
    - N (int): number of nodes in the network
    - K (int): degree of each node in the initial ring-lattice
    - P (float): probability that a connection will be rewired 
    - draw_flag (boolean): draw the graph
    
    Return:
    - networkx graph object
    """

    ws = nx.empty_graph(n = N+1)
    pos = nx.circular_layout(ws)

    halfK = math.floor(K/2)
    nodes = range(1,N+1)

    # create ring lattice
    ring_lattice = nx.Graph()
    ring_lattice.add_nodes_from(nodes)

    for i, u in enumerate(ring_lattice.nodes):
        for j in range(i+1, i+1+halfK):
            v = (j % N) + 1
            ring_lattice.add_edge(u, v)


    # randomize ring lattice to create Watts-Strogatz
    ws = nx.Graph(ring_lattice)

    for u in ws:
        trash_edges = []
        new_edges = []
        non_neighbors = [n for n in nx.non_neighbors(ws, u)]
        node_colors = ['r' if n == u else 'k' for n in ws]
        # node_colors[-1] = 'b'
        edge_colors = 'k'
        frameData.append((ws.copy(), pos, node_colors, edge_colors, 50, False))
        for v in ws[u]:
            if random.random() <= P:
                trash_edges.append((u,v))
                # Original, needs to be sorted for edge colorer
                # new_edges.append((u, random.choice(non_neighbors)))
                new_edges.append(tuple(sorted((u, random.choice(non_neighbors)))))
        ws.remove_edges_from(trash_edges)
        ws.add_edges_from(new_edges)
        node_colors = ['r' if n == u else 'k' for n in ws]
        # node_colors[-1] = 'b'
        print(new_edges)
        print(ws.edges)
        edge_colors = ['b' if e in new_edges else 'k' for e in ws.edges]
        frameData.append((ws.copy(), pos, node_colors, edge_colors, 50, False))

    if draw_flag:
        nx.draw_circular(ws)
        plt.show()

    return ws

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
    watts_strogatz(N = 20, P = 0.2)
    ani = animation.FuncAnimation(
        fig, animate, interval=400, blit=False, save_count=500)
    plt.show()

do_animation()