# Generate a fully connected graph and write to csv

import csv
import random

def generate_graph_csv(num_vertices, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for src in range(num_vertices):
            for dst in range(num_vertices):
                if src != dst:  # Ensure vertices are not the same
                    weight = random.randint(1, 100)  # Generate random weight
                    writer.writerow([src, dst, weight])

# Example usage:
num_vertices = int(input("Enter n: "))
csv_file_path = 'graph3.csv'
generate_graph_csv(num_vertices, csv_file_path)
print(f"Generated graph with {num_vertices} vertices and saved to {csv_file_path}")
