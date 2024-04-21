from flask import Flask, request, jsonify
from flask_cors import CORS
from TSP.classical.gps import GPS
from VRP.classical.ras import RAS
from TSP.quantum.gps import GPS as GPSHybrid
import numpy as np
import json

app = Flask(__name__)
CORS(app)

@app.route('/solve_vrp', methods=['POST'])
def solve_vrp():
    data = request.get_json()
    
    # Extract data from JSON
    n = data['n']  # Number of clients
    m = data['m']  # Number of vehicles
    cost = np.array(data['cost'])  # Cost matrix
    xc = np.array(data['xc'])  # X coordinates
    yc = np.array(data['yc'])  # Y coordinates

    # Solve VRP using RAS class
    vrp_solver = RAS(n, m, cost, xc, yc)
    solution = vrp_solver.formulate_and_solve()

    # Prepare response
    if solution:
        response = {
            'status': 'success',
            'min_cost': solution['min_cost'],
            'runtime_ms': solution['runtime'],
            'solution': vrp_solver.sol
        }
    else:
        response = {'status': 'error', 'message': 'No solution found.'}

    return jsonify(response)

@app.route('/solve_tsp', methods=['POST'])
def solve_tsp():
    data = request.get_json()
    
    # Extract data from JSON
    n = data['n']  # Number of clients

    print(n)
    
    cost = np.array(data['cost'])  # Cost matrix
    xc = np.array(data['xc'])  # X coordinates
    yc = np.array(data['yc'])  # Y coordinates

    # Solve TSP using GPS class
    tsp_solver = GPS(n, cost, xc, yc)

    # Prepare response
    response = {
        'status': 'success',
        'solution': tsp_solver.sol,
        # 'min_cost': tsp_solver.model.ObjectiveValue,
        # 'runtime_ms': tsp_solver.runtime * 1000  # Convert to milliseconds
    }

    return jsonify(response)

@app.route('/tsp_hybrid', methods=['POST'])
def solve_tsp_hybrid():
    def parse_solution(sample):
        # Extract variable assignments from the sample
        variables = sample['sample']
        n = int(max(variables.keys(), key=lambda x: int(x.split('.')[1]))[2]) + 1

        # Initialize the solution matrix with null values
        solution = [[None] * n for _ in range(n)]

        # Populate the solution matrix based on variable assignments
        for var, value in variables.items():
            if value == 1 and var.startswith('x.'):
                i, j, _ = map(int, var.split('.')[1:])
                solution[i][j] = 1

        return {'solution': solution, 'status': 'success'}

    data = request.get_json()
    
    # Extract data from JSON
    n = data['n']  # Number of clients
    cost = np.array(data['cost'])  # Cost matrix
    xc = np.array(data['xc'])  # X coordinates
    yc = np.array(data['yc'])  # Y coordinates

    # Solve TSP using GPS class with LeapHybridCQMSampler
    tsp_solver = GPSHybrid(n, cost, xc, yc)
    solution = tsp_solver.solve()

    # Prepare response
    if solution:
        # Convert the solution samples to a list of dictionaries
        # print(solution)
        response = parse_solution(solution)
    else:
        response = {'status': 'error', 'message': 'No solution found.'}

    # Convert the response to JSON
    response_json = json.dumps(response)
    return response_json

if __name__ == '__main__':
    app.run(debug=True)
