import networkx as nx
import matplotlib.pyplot as plt
import math, random

# def rewire(graph, prob, )


# parameters
N = 8
K = 4
P = 0.8

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
    for v in ws[u]:
        if random.random() <= P:
            trash_edges.append((u,v))
            new_edges.append((u, random.choice(non_neighbors)))
    ws.remove_edges_from(trash_edges)
    ws.add_edges_from(new_edges)

nx.draw_circular(ws)
plt.show()