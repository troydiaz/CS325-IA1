import sys
from itertools import combinations
import math
import random
import time
from a1_utils import read_input_from_cli, distance, write_output_to_file, generate_random_input_file, sort_pairs, read_file_to_list

def brute_force_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Find the closest pair of points using brute force.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points, where each point is represented 
                                            as a tuple of coordinates (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The updated minimum distance (float) between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """

    """
    Brute Force Approach
    1) Calculate distrance between all pairs.
    2) Store minimum distance and each pair that has that distance.

    O(n^2) complexity

    Psuedo code design

    1) Set min_distance to be inf.
    2) Initialize an empty list for pairs we're interested in
    3) For each pair, compare distance. If distance is less than min_distance,
    store distance and add that pair to the list.
    4) If distance is the same for the next pair, add to the list.
    5) Sort list of closest pairs.
    6) Return the minimum distance and pair list.
    """
    min_dist = float('inf')
    closest_pairs = []
    dist = 0.0

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]

            dist = distance(points[i], points[j])

            if dist < min_dist:
                min_dist = dist
                closest_pairs = [tuple(sorted([p1, p2]))]
            elif dist == min_dist:
                closest_pairs.append(tuple(sorted([p1, p2])))

    closest_pairs = sort_pairs(closest_pairs)

    return min_dist, closest_pairs


if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        
        generate_random_input_file(n = 1000, output_file = "input1000.txt", seed = 42)
        print("Generated 1000 random points in brute_f")

        points = read_file_to_list("input1000.txt")
        print("Read 1000 points from input1000.txt")

        start_time= time.time()
        min_dist, closest_pairs = brute_force_closest_pair(points)
        end_time = time.time()

        print(f"Brute force took {end_time - start_time: 0.6f} seconds")
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'bruteforce_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

