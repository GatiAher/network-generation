import networkx as nx
import matplotlib.pyplot as plt
import math

# parameters
N = 15
K = 8
P = 0.2

halfK = math.floor(K/2)
nodes = range(1,N+1)

# create ring lattice
ring_lattice = nx.Graph()
ring_lattice.add_nodes_from(nodes)

for i, u in enumerate(ring_lattice.nodes):
    for j in range(i+1, i+1+halfK):
        v = (j % N) + 1
        ring_lattice.add_edge(u, v)

nx.draw_circular(ring_lattice)
plt.show()

# randomize ring lattice to create Watts-Strogatz
ws = nx.Graph(ring_lattice)