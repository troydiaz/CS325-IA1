from divide_conquer import divide_and_conquer_closest_pair  # Import your divide-and-conquer function
from a1_utils import read_file_to_list
import numpy as np
import time

# Initialize output array for divide-and-conquer runtime
output_divide_and_conquer = np.zeros((6, 11))

# Loop over test files
for k in range(1, 6):
    for i in range(1, 11):
        # Read the input points from the file
        points = read_file_to_list(f"inputs/input10^{k}-trial{i}.txt")
        print(f"Computing for input10^{k}-trial{i}.txt")

        # Test divide-and-conquer implementation
        start_time_dnc = time.time()
        min_dist_dnc, closest_pairs_dnc = divide_and_conquer_closest_pair(points)
        end_time_dnc = time.time()

        # Record runtime
        output_divide_and_conquer[k][i] = end_time_dnc - start_time_dnc
        print(f"Divide and Conquer: Completed input10^{k}-trial{i}.txt in {output_divide_and_conquer[k][i]:.10f} seconds.")

        # Save results to a CSV file
        np.savetxt("divide_and_conquer_runtime.csv", output_divide_and_conquer, "%.10f", delimiter=',', newline="\n")
