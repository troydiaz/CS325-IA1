import sys
from itertools import combinations
import math
from a1_utils import read_input_from_cli, distance, write_output_to_file, generate_random_input_file

for k in range(6, 9):
    for i in range(1, 11):
        generate_random_input_file(n=pow(10, k), output_file=f"inputs/input10^{k}-trial{i}.txt", seed=(i * k))
