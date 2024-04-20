import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
from itertools import permutations
from qiskit.circuit.library import TwoLocal
from qiskit_optimization.applications import Tsp
from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import SPSA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from dwave.system import DWaveSampler, EmbeddingComposite
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
from itertools import permutations

def draw_graph(G, colors, pos):
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(G, node_color=colors, node_size=600, alpha=0.8, ax=default_axes, pos=pos)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)


def draw_tsp_solution(G, order, colors, pos):
    G2 = nx.DiGraph()
    G2.add_nodes_from(G)
    n = len(order)
    for i in range(n):
        j = (i + 1) % n
        G2.add_edge(order[i], order[j], weight=G[order[i]][order[j]]["weight"])
    default_axes = plt.axes(frameon=True)
    nx.draw_networkx(
        G2, node_color=colors, edge_color="b", node_size=600, alpha=0.8, ax=default_axes, pos=pos
    )
    edge_labels = nx.get_edge_attributes(G2, "weight")
    nx.draw_networkx_edge_labels(G2, pos, font_color="b", edge_labels=edge_labels)

def brute_force_tsp(w, N):
    a = list(permutations(range(1, N)))
    last_best_distance = 1e10
    for i in a:
        distance = 0
        pre_j = 0
        for j in i:
            distance = distance + w[j, pre_j]
            pre_j = j
        distance = distance + w[pre_j, 0]
        order = (0,) + i
        if distance < last_best_distance:
            best_order = order
            last_best_distance = distance
            print("order = " + str(order) + " Distance = " + str(distance))
    return last_best_distance, best_order

# Generating a graph of n nodes
# Number of vertices in G = (V, E) with n = |V|
n = 4

# We need to resolve the entire graph as Hamiltonian cycles represented by n^2 variables 
num_qubits = n**2

tsp = Tsp.create_random_instance(n, seed=random.randint(0,999))
adj_matrix = nx.to_numpy_array(tsp.graph)
print("distance\n", adj_matrix)

colors = ["r" for node in tsp.graph.nodes]
pos = [tsp.graph.nodes[node]["pos"] for node in tsp.graph.nodes]
draw_graph(tsp.graph, colors, pos)

# Solve using brute force to verify
best_distance, best_order = brute_force_tsp(adj_matrix, n)
print(
    "Best order from brute force = "
    + str(best_order)
    + " with total distance = "
    + str(best_distance)
)
draw_tsp_solution(tsp.graph, best_order, colors, pos)

# Map the TSP cost function to the Ising Problem
qp = tsp.to_quadratic_program()
print(qp.prettyprint())


qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(qp)
qubitOp, offset = qubo.to_ising()
print("Offset:", offset)
print("Ising Hamiltonian:")
# print(qubitOp.coeffs.tolist(), type(qubitOp.coeffs.tolist()))

# Solve QUBO using D-Wave hybrid solver
sampler = DWaveSampler(solver='Advantage_system4.1')
hybrid_sampler = EmbeddingComposite(sampler)
sampleset = hybrid_sampler.sample_qubo(Q=qubitOp.coeffs.tolist())

# Extract solution
solution = sampleset.first.sample

# Interpret solution
solution_list = [solution[i] for i in range(len(solution))]
x = tsp.sample_most_likely(solution_list)
print("solution:", x)
print("feasible:", qubo.is_feasible(x))
z = tsp.interpret(x)
print("interpreted solution:", z)
print("solution objective:", tsp.tsp_value(z, adj_matrix))
draw_tsp_solution(tsp.graph, z, colors, pos)
