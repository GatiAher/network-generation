import networkx as nx
import math

N = 7
K = 4
P = 0.2

halfK = math.floor(K/2)
nodes = range(1,N+1)
ring_lattice = nx.Graph()

ring_lattice.add_nodes_from(nodes)

for i, u in enumerate(ring_lattice.nodes):
    for j in range(i+1, i+1+halfK):
        v = (j % N) + 1
        ring_lattice.add_edge(u, v)

print(ring_lattice)