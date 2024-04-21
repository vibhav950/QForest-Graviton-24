import numpy as np

class Initializer:

    def __init__(self, n, a, b):
        self.n = n
        self.a = a
        self.b = b

    def generate_nodes_and_weight_matrix(self):

        n = self.n
        a = self.a
        b = self.b
        
        np.random.seed(100*a + b)

        x = (np.random.rand(n) - 0.5) * 50
        y = (np.random.rand(n) - 0.5) * 50

        weight_matrix = np.zeros([n, n])
        for i in range(n):
            for j in range(i+1, n):
                weight_matrix[i, j] = (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2
                weight_matrix[j, i] = weight_matrix[i, j]

        print(weight_matrix)

        return x, y, weight_matrix
    
from utils import VRPSolver, compare_solvers, random_routing_instance

n=20     # number of clients
m=3     # number of vehicles

initializer = Initializer(n+1, n+1, 3)
xc, yc, cost = initializer.generate_nodes_and_weight_matrix()

### Select the type of model to solve VRP
#    1: Constrained Quadratic Model - A new model released by D-Wave Systems capable of encoding Quadratically Constrained Quadratic Programs (QCQPs)
#    2: Binary Quadratic Model - A model that encodes Ising or QUBO problems
model = 'CQM'

### The time limit (in seconds) for the solvers to run on the `LeapHybridCQMSampler` backend
time_limit = 30


### Select solver
#    1: RAS (Route Activation Solver)
#    2: FQS (Full QUBO Solver)
#    3: GPS (Guillermo, Parfait, Saúl) (only using CQM)
#    4: DBSCANS (Density-Based Spatial Clustering of Applications with Noise - Solver)
#    5: SPS (Solution Partition Solver)
solver = 'fqs'

vrps = VRPSolver(n, m, cost, xc, yc, model=model, solver=solver, time_limit=time_limit)
vrps.solve_vrp()

vrps.plot_solution()

print('here')


# Number of iterations to get the average approximation ratio for a particular solver
# Warning! More iterations will take more time and resources to run
n_iter = 1

comparison_table = compare_solvers(n, m, cost, xc, yc, n_iter=n_iter, time_limit=time_limit)

print('Minimum cost of best known solution:', comparison_table[0]['exact_min_cost'])
for solver_id in comparison_table[1]:
  print(f'{solver_id}:', '\t', f'average min cost = {comparison_table[1][solver_id]["avg_min_cost"]}',
                         '\t', f'average runtime = {comparison_table[1][solver_id]["avg_runtime"]}',
                         '\t', f'number of variables = {comparison_table[1][solver_id]["num_vars"]}',
                         '\t', f'approximation ratio = {comparison_table[1][solver_id]["approximation_ratio"]}'
  )