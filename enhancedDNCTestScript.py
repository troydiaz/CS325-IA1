from enhanced_dnc import enhanced_divide_and_conquer_closest_pair
from a1_utils import read_file_to_list
import numpy as np
import time

output = np.zeros((7, 11))
for k in range(6, 7):
    for i in range(1, 2):
        points = read_file_to_list(f"input10^{k}-trial{i}.txt")
        print(f"Computing for input10^{k}-trial{i}.txt")
        start_time = time.time()
        min_dist, closest_pairs = enhanced_divide_and_conquer_closest_pair(points)
        end_time = time.time()
        print(f"Completed input10^{k}-trial{i}.txt. Writing time to file")
        output[k][i] = end_time - start_time
        np.savetxt("enhanced_dnc_runtime.csv", output, "%.10f", delimiter=',', newline="\n")