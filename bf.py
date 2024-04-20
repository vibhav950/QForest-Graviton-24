# Brute force TSP solver

import csv
from itertools import permutations
import numpy as np

from time import perf_counter

def read_edges_from_csv(file_path):
    edges = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                src, dst, weight = map(int, row)
                edges.append((src, dst, weight))
    return edges

def build_adjacency_matrix(edges, num_nodes):
    adjacency_matrix = np.zeros((num_nodes, num_nodes))
    for src, dst, weight in edges:
        adjacency_matrix[src][dst] = weight
    return adjacency_matrix


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
            # print("order = " + str(order) + " Distance = " + str(distance))
    return last_best_distance, best_order

def brute_force_tsp_ex(w, N):
    # Initialize the order as [1, 2, ..., N-1]
    order = list(range(1, N))
    last_best_distance = 1e10
    
    # Generate permutations sequentially
    while True:
        # Calculate the distance for the current permutation
        distance = 0
        pre_j = 0
        for j in order:
            distance += w[j, pre_j]
            pre_j = j
        distance += w[pre_j, 0]
        
        # Construct the order with start node 0
        order_with_start = [0] + order
        
        # Update the best order and distance if necessary
        if distance < last_best_distance:
            best_order = order_with_start
            last_best_distance = distance
            # Uncomment the line below to print each iteration
            # print("order = " + str(order_with_start) + " Distance = " + str(distance))
        
        # Generate the next permutation
        i = len(order) - 2
        while i >= 0 and order[i] >= order[i + 1]:
            i -= 1
        if i >= 0:
            j = len(order) - 1
            while order[j] <= order[i]:
                j -= 1
            order[i], order[j] = order[j], order[i]
        order[i + 1:] = reversed(order[i + 1:])
        
        # Check if all permutations have been generated
        if order == list(range(1, N)):
            break
    
    return last_best_distance, best_order

# Example CSV file path
csv_file_path = 'graph3.csv'

# Read edges from CSV
edges = read_edges_from_csv(csv_file_path)

# Determine the number of nodes in the graph
num_nodes = max(max(edge[0], edge[1]) for edge in edges) + 1

# Build adjacency matrix
# adj_matrix = build_adjacency_matrix(edges, num_nodes)

adj_matrix = np.array([
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
])
# print("distances\n", adj_matrix)

# mats = [
#     [[0, 19, 20, 64],
#     [19,  0, 37, 81],
#     [20, 37,  0, 59],
#     [64, 81, 59,  0]],

#     [[ 0, 35, 30, 55],
#      [35,  0, 32, 25],
#      [30, 32,  0, 37],
#      [55, 25, 37,  0]],

#     [[ 0, 34, 40, 44,],
#      [34,  0, 74, 76,],
#      [40, 74,  0, 16,],
#      [44, 76, 16,  0]],

#     [[ 0, 69, 55, 60,],
#      [69,  0, 26, 40,],
#      [55, 26,  0, 54,],
#      [60, 40, 54,  0]]
# ]

# adj_matrix = np.array(mats[0])

# Solve TSP using brute force
start = perf_counter()
best_distance, best_order = brute_force_tsp_ex(adj_matrix, 10)
end = perf_counter()

print("Best distance:", best_distance)
print("Best order:", best_order)
print(f"Time: {(end - start) * 1e0}s")