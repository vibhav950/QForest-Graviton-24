from TSP.classical.gps import GPS as GPSc
from TSP.quantum.gps import GPS as GPSq
from TSP.quantum.fqs import FQS as FQSq

import numpy as np

def random_routing_instance(n, seed=None):
    """
    Generate a random TSP instance (n+1 random coordinates and a cost matrix which is same as the distance between them).
    Args:
        n: No. of nodes exclusing depot.
        seed: Seed value for random number generator. Defaults to None, which sets a random seed.
    Returns:
        A list of (n + 1) x coordinates, a list of (n + 1) y coordinates and an (n + 1) x (n + 1) numpy array as the
        cost matrix.
    """
    
    # Set seed
    if seed is not None:
        np.random.seed(seed)

    # Generate TSP distance_matrix
    xc = (np.random.rand(n + 1) - 0.5) * 20
    yc = (np.random.rand(n + 1) - 0.5) * 20
    xc[0], yc[0] = 0, 0
    dist_mat = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            dist_mat[i, j] = np.sqrt((xc[i] - xc[j]) ** 2 + (yc[i] - yc[j]) ** 2) * 100
            dist_mat[j, i] = dist_mat[i, j]

    # Return output
    return dist_mat.astype(int), xc, yc

n = 4
cost, xc, yc = random_routing_instance(n, seed=0)

print(n, type(n))
print(cost, type(cost), cost.shape)
print(xc, type(xc), xc.shape)
print(yc, type(yc), yc.shape)

# GPSc(n, cost, xc, yc)

# fqs = FQSq(n, cost, xc, yc)
# res = fqs.solve()
# fqs.visualize()

# gps = GPSq(n, cost, xc, yc)
# res = gps.solve()
# gps.visualize()