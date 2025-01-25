from brute_force import brute_force_closest_pair  # Import your brute force function
from a1_utils import read_file_to_list
import numpy as np
import time

# Initialize output array for brute force runtime
output_brute_force = np.zeros((6, 11))

# Loop over test files
for k in range(1, 6):
    for i in range(1, 11):
        # Read the input points from the file
        points = read_file_to_list(f"input10^{k}-trial{i}.txt")
        print(f"Computing for input10^{k}-trial{i}.txt")

        # Test brute force implementation
        start_time_brute = time.time()
        min_dist_brute, closest_pairs_brute = brute_force_closest_pair(points)
        end_time_brute = time.time()

        # Record runtime
        output_brute_force[k][i] = end_time_brute - start_time_brute
        print(f"Brute Force: Completed input10^{k}-trial{i}.txt in {output_brute_force[k][i]:.10f} seconds.")

        # Save results to a CSV file
        np.savetxt("brute_force_runtime.csv", output_brute_force, "%.10f", delimiter=',', newline="\n")
