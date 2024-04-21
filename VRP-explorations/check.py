import numpy as np
from utils import RAS

# Generate input data
n = 5  # Number of clients
m = 2  # Number of vehicles
cost = np.random.randint(1, 10, size=(n+1, n+1))  # Random cost matrix
xc = np.random.rand(n+1) * 10  # Random x coordinates
yc = np.random.rand(n+1) * 10  # Random y coordinates

# Create RAS instance
ras_solver = RAS(n, m, cost, xc, yc)

# Solve the problem
solution = ras_solver.formulate_and_solve()

# Print optimal path and cost
if solution:
    print("Optimal Path:")
    for i in range(ras_solver.n+1):
        for j in range(ras_solver.n+1):
            if ras_solver.sol[0][i][j] == 1:
                print(f"Vehicle travels from node {i} to node {j}")
    print(f"Optimal Cost: {solution['min_cost']}")
else:
    print("No solution found.")
