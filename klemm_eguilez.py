"""
Produce an undirected Klemm and Eguilez network of size N

Author: Gati Aher
Date: Dec 2, 2021

Source: pseudocode from "Methods for Generating Complex Networks with Selected Structural Properties for Simulations: A Review and Tutorial for Neuroscientists" (Prettejohn, Berryman, McDonnell1 2011) 
Link: https://www.frontiersin.org/articles/10.3389/fncom.2011.00011/full
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random

frameData = [] # data for each frame, will be put into nx.draw()

def klemm_eguilez(N=50, M=5, P_MU=0.01, draw_flag=False):
    """
    Produce an undirected Klemm-Eguilez (small-world and scale-free topology) network of size N. 
    The generative algorithm creates a fully connected initial network of size M, and then, 
    for each new node, the generative algorithm creates connections between the new node and M of the existing nodes.

    P_MU is the probability that new node is connected to random node
    if P_MU is 0, generate network similar to regular lattice
    - relatively long average path length
    - absence of edges to deactivated nodes
    - clustering is very high (all active nodes have all-to-all connectivity)

    if P_MU is 1, generate a scale-free graph (like Barabasi-Albert)
    - average path length comparable to random network
    - relatively low clustering

    intermediate values of P_MU
    - enough randomly chosen edges to reduce the average path length to be comparable to random network
    - significantly higher clustering than Barabasi-Albert

    Arguments:
    - N (int): number of nodes in network
    - M (int): number of active nodes used in network generation
    - P_MU (float): probability that new node is connected to random node
    - draw_flag (boolean): draw the graph
    
    Return:
    - networkx graph object
    """

    active_nodes = [] # store active nodes

    # initialize fully connected initial network of size M
    # add its nodes to active nodes
    G = nx.empty_graph(n = N)
    pos = nx.circular_layout(G)
    G = nx.complete_graph(M)
    active_nodes = list(G.nodes)

    # FRAME

    # iteratively add remaining N-M nodes with edges to M existing nodes
    for i in range(M, N):
        # calculate deactivated nodes
        deactivated_nodes = list(set(list(G.nodes)) ^ set(active_nodes))
        # add node
        G.add_node(i)

        # FRAME
        node_colors = ['r' if n in active_nodes else 'k' for n in G.nodes]
        node_colors[-1] = 'b'
        edge_colors = ['g' if (e[0] == i or e[1] == i) else 'k' for e in G.edges]
        frameData.append((G.copy(), pos, node_colors, edge_colors, 50, False))

        for j in active_nodes:
            chance = random.random()        
            if P_MU > chance or len(deactivated_nodes) == 0:
                # create a reciprocal edge between nodes i and j
                G.add_edge(i, j)
                node_colors = ['r' if n in active_nodes else 'k' for n in G.nodes]
                node_colors[-1] = 'b'
                edge_colors = ['g' if (e[0] == i or e[1] == i) else 'k' for e in G.edges]
                frameData.append((G.copy(), pos, node_colors, edge_colors, 50, False))

            else:
                connected = False
                while (not connected):
                    chance = random.random()
                    # choose a random deactivated node to be j
                    j = random.choice(deactivated_nodes)
                    sum_deg_deactivated_nodes = sum([G.degree[x] for x in deactivated_nodes])
                    if (G.has_edge(i, j)):
                        continue
                    if (((G.degree[j] / sum_deg_deactivated_nodes) > chance)):
                        # preferential attachment to nodes with higher degrees (scale-free)
                        # create a reciprocal edge between nodes i and j
                        G.add_edge(i, j)
                        # remove node j from this loop's list of deactivated nodes
                        # so that this node j will not be picked twice
                        deactivated_nodes.remove(j)
                        connected = True

                        node_colors = ['r' if n in active_nodes else 'k' for n in G.nodes]
                        node_colors[-1] = 'b'
                        edge_colors = ['g' if (e[0] == i or e[1] == i) else 'k' for e in G.edges]
                        frameData.append((G.copy(), pos, node_colors, edge_colors, 50, False))
            # FRAME
                    
        # replace active node with node i
        # active nodes with lower degree are more likely to be replaced
        # randomly choose node j from active nodes list
        chosen = False
        while(not chosen):
            j = random.choice(active_nodes)
            # probability of deactivating node j, probability increases if degree is comparatively low
            P_D = 1/G.degree[j] / sum(1/G.degree[x] for x in active_nodes)
            chance = random.random()
            if (P_D > chance):
                chosen = True
                active_nodes.remove(j)
                active_nodes.append(i)
                # MAKE ALL ACTIVE NODES (INCLUDING NEW NODE) A PARTICULAR COLOR
                # NEW NODE DIFF COLOR THAN ACTIVE
                # node_colors = ['r' if n in active_nodes else 'k' for n in G.nodes]
                # node_colors[-1] = 'b'
                # frameData.append((G.copy(), pos, node_colors, 'k', 50, False))

    if (draw_flag):
        pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
        nx.draw(G, pos=pos, with_labels=True)
        plt.show()

    return G

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
    klemm_eguilez(N = 20, P_MU=0.5)
    ani = animation.FuncAnimation(
        fig, animate, interval=200, blit=False, save_count=500)
    writergif = animation.PillowWriter(fps=5) 
    ani.save("klemm_eguilez_animation.gif", writer=writergif)
    plt.show()

do_animation()