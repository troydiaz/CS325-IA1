import sys
from itertools import combinations
import math
import time
from a1_utils import read_input_from_cli, distance, write_output_to_file

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

    """
    Pseudocode Design
    1. DivideandConquerClosestPair(points)
        1.1 Sort points by x-coordinate
        1.2 Return the result of calling RecursiveClosestPair(points)
    2. RecursiveClosestPair(points)
        2.1 Divide points into two halves: left and right
        2.2 Compute the midpoint x-coordinate for dividing the points
        2.3 Recursively call RecursiveClosestPair(left) to get d1 and pairs1
        2.4 Recursively call RecursiveClosestPair(right) to get d2 and pairs2
        2.5 Set d to the smaller of d1 and d2
        2.6 Collect all points within distance d of the midpoint into a list called strip
        2.7 Call MergeStep(strip, d) to get d_strip and pairs_strip
        2.8 If d_strip < d:
            Return d_strip and pairs_strip
        2.9 If d_strip == d:
            Return d and the combined pairs from pairs1, pairs2, and pairs_strip
        2.10 Else:
            Return d and the combined pairs from pairs1 and pairs2
    3. MergeStrip(strip, d)
        3.1 Sort strip by y-coordinate
        3.2 Set min_distance to d
        3.3 Initialize an empty list closest_pairs to store the closest pairs
        3.4 For each point p in strip:
            For each point q after p in strip:
                If (q.y - p.y) >= min_distance, break
                Compute the distance d_ij between p and q
                If d_ij < min_distance:
                    Update min_distance to d_ij
                    Replace closest_pairs with [(p,q)]
                If d_ij == min_distance:
                    Add (p,q) to closest_pairs
        3.5 Return min_distance and closest_pairs
    """
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
        d = min(d1, d2)
        pairs = pairs1 + pairs2
        
        # Collect points within distance d of the midpoint into strip
        strip = [p for p in sorted_points if abs(p[0] - midpoint_x) < d]
        
        # Sort the strips by y-coordinates from scratch (Naive Approach)
        strip.sort(key=lambda p: p[1])
        
        # Merge step to find closest pairs across the dividing line
        d_strip, pairs_strip = merge_strip(strip, d)
        
        # Return the smallest distance and corresponding pairs
        if d_strip < d:
            return d_strip, pairs_strip
        elif d_strip == d:
            return d, pairs + pairs_strip
        else:
            return d, pairs
    
    # To find the closest pairs of points within a strip using a naive approach. The strip contains points within distance d of the dividing line. 
    def merge_strip(strip: list[tuple[float, float]], d: float) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
        
        min_dist = d
        closest_pairs = []

        # Compare each pair of points in the strip
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j][1] - strip[i][1]) >= min_dist:
                    break
                d_ij = distance(strip[i], strip[j])
                if d_ij < min_dist:
                    min_dist = d_ij
                    closest_pairs = [(strip[i], strip[j])]
                elif d_ij == min_dist:
                    closest_pairs.append((strip[i], strip[j]))

        return min_dist, closest_pairs
    
    # Sort points by x-coordinate as the first step
    sorted_points = sorted(points, key=lambda p: p[0])

    # Recursive calls will re-sort parts of the data as needed (Naive Approach)
    return recursive_closest_pair(sorted_points)

    # return distance, pairs



if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        start_time = time.time()
        min_dist, closest_pairs = divide_and_conquer_closest_pair(points)
        end_time = time.time()
        
        print(f"Naive Divide & Conquer took {end_time - start_time:.6f} seconds")
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'ddnc_output.txt')
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
