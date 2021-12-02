"""
Produce an undirected Klemm and Eguilez network of size N

Author: Gati Aher
Date: Dec 2, 2021

TODO: fill this in
Source: pseudocode from xxx by xxx

"""

import networkx as nx
import matplotlib.pyplot as plt
import math
import random

# parameters
N = 50 # size of network
M = 5 # length of list of "active nodes"

# P_MU is the probability that new node is connected to random node
# if P_MU is 0, generate network similar to regular lattice
# - relatively long average path length
# - absence of edges to deactivated nodes
# - clustering is very high (all active nodes have all-to-all connectivity)

# if P_MU is 1, generate a scale-free graph (like Barabasi-Albert)
# - average path length comparable to random network
# - relatively low clustering

# intermediate values of P_MU
# - enough randomly chosen edges to reduce the average path length to be comparable to random network
# - significantly higher clustering than Barabasi-Albert

P_MU = 1

active_nodes = [] # store active nodes

# initialize fully connected initial network of size M
# add its nodes to active nodes
G = nx.complete_graph(M)

active_nodes = list(G.nodes)
print("active_nodes:", active_nodes)

# iteratively add remaining N-M nodes with edges to M existing nodes
for i in range(M, N):
    # calculate deactivated nodes
    deactivated_nodes = list(set(list(G.nodes)) ^ set(active_nodes))
    
    print("active_nodes:", active_nodes)
    print("deactivated_nodes:", deactivated_nodes)

    G.add_node(i)
    print("*add node ", i)

    for j in active_nodes:
        chance = random.random()        
        if P_MU > chance or len(deactivated_nodes) == 0:
            # create a reciprocal edge between nodes i and j
            G.add_edge(i, j)
        else:
            connected = False
            while (not connected):
                chance = random.random()
                # choose a random deactivated node to be j
                j = random.choice(deactivated_nodes)
                sum_deg_deactivated_nodes = sum([G.degree[x] for x in deactivated_nodes])
                if ((G.degree[j] / sum_deg_deactivated_nodes) > chance):
                    # preferential attachment to nodes with higher degrees (scale-free)
                    # create a reciprocal edge between nodes i and j
                    G.add_edge(i, j)
                    connected = True
                
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
            print("*deactivate node", j)


pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
nx.draw(G, pos=pos, with_labels=True)
plt.show()

