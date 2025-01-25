import sys
from itertools import combinations
import math
import time
import copy
from a1_utils import read_input_from_cli, distance, write_output_to_file, read_file_to_list, sort_pairs

def divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
    """
    Recursively find the closest pair of points using a divide-and-conquer approach.
    
    Args:
        points (list[tuple[float, float]]): A list of 2D points where 
                                            each point is represented as a tuple (x, y).
                                            
    Returns:
        tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
            - The minimum distance between the closest pair(s) of points.
            - A list of tuples representing the closest point pairs, where each pair is a 
              tuple of two points ((x1, y1), (x2, y2)).
    """

    """
    """
    # TO COMPLETE 


    def recursive_closest_pair(sorted_points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
        
        # Base case: If there's only one point, no pair exists
        if len(sorted_points) <= 1:
            return float('inf'), []
        
        # Divide: Split the sorted points into two halves
        mid = len(sorted_points) // 2
        left_points = sorted_points[:mid]
        right_points = sorted_points[mid:]
        midpoint_x = sorted_points[mid][0] # x-coordinate of the dividing line
        
        # Recursive calls for left and right halves
        d1, pairs1 = recursive_closest_pair(left_points)
        d2, pairs2 = recursive_closest_pair(right_points)
        
        # Combine results from both halves
        if d1 < d2:
            d = d1
            pairs = pairs1
        elif d1 > d2:
            d = d2
            pairs = pairs2
        elif math.isclose(d1, d2):
            d = d1
            pairs = pairs1
            for point in pairs2:
                pairs.append(point)
        
        # Collect points within distance d of the midpoint into strip
        strip = [p for p in sorted_points if abs(p[0] - midpoint_x) < d]

        # Remove closest pairs within M-strip to avoid double-count
        pairsCopy = copy.deepcopy(pairs)
        for pair in pairs:
            if math.isclose(pair[0][0], midpoint_x) and math.isclose(pair[1][0],midpoint_x):
                pairsCopy.remove(pair)
            elif (abs(pair[0][0] - midpoint_x) < d and abs(pair[1][0] - midpoint_x) < d):
                pairsCopy.remove(pair)   
        pairs = pairsCopy  
        
        # Sort the strips by y-coordinates from scratch (Naive Approach)
        strip.sort(key=lambda p: p[1])
        
        # Merge step to find closest pairs across the dividing line
        d_strip, pairs_strip = merge_strip(strip, d)
        
        # Return the smallest distance and corresponding pairs
        if math.isclose(d_strip, d):
            return d, pairs + pairs_strip
        elif d_strip < d:
            return d_strip, pairs_strip
        else:
            return d, pairs
    
    # To find the closest pairs of points within a strip using a naive approach. The strip contains points within distance d of the dividing line. 
    def merge_strip(strip: list[tuple[float, float]], d: float) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
        
        min_dist = d
        closest_pairs = []

        # Compare each pair of points in the strip
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if abs(strip[j][1] - strip[i][1]) > min_dist:
                    break
                d_ij = distance(strip[i], strip[j])
                if math.isclose(d_ij, min_dist):
                    closest_pairs.append((strip[i], strip[j]))
                elif d_ij < min_dist:
                    min_dist = d_ij
                    closest_pairs = [(strip[i], strip[j])]
                    
        return min_dist, closest_pairs
    
    # Sort points by x-coordinate as the first step
    sorted_points = sorted(points, key=lambda p: p[0])

    # Recursive calls will re-sort parts of the data as needed (Naive Approach)
    distanceOutput, pairs = recursive_closest_pair(sorted_points)
    return distanceOutput, sort_pairs(pairs)
    # return distance, pairs



if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        # points = read_file_to_list("input1.txt")
        start_time = time.time()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)
        end_time = time.time()
        
        print(f"Naive Divide & Conquer took {end_time - start_time:.6f} seconds")
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'dnc_output.txt')
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
