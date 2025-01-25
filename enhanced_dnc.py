import sys
import copy
from itertools import combinations
import math
import time
from a1_utils import read_input_from_cli, distance, write_output_to_file,read_file_to_list, generate_random_input_file, sort_pairs
from brute_force import brute_force_closest_pair


def enhanced_divide_and_conquer_closest_pair(points: list[tuple[float, float]]) -> tuple[float, list[tuple[tuple[float, float], tuple[float, float]]]]:
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
    
    points.sort(key=lambda point: point[0])
    xSorted = points
    ySorted = sorted(points, key=lambda point: point[1])
    distance, pairs = enhanced_dnc_recursive(xSorted, ySorted)
    return distance, sort_pairs(pairs)

def enhanced_dnc_recursive(xSortedPoints, ySortedPoints):
    xSortedLength = len(xSortedPoints)
    if xSortedLength <= 1:
        return float('inf'), []

    splitIndex = (xSortedLength - 1) // 2
    x_m = xSortedPoints[splitIndex][0]
    leftXSortedPoints = xSortedPoints[:splitIndex]
    rightXSortedPoints = xSortedPoints[splitIndex + 1:]
    leftYSortedPoints = [point for point in ySortedPoints if point[0] <= x_m]
    rightYSortedPoints = [point for point in ySortedPoints if point[0] > x_m]

    leftMinDistance, leftClosestPoints = enhanced_dnc_recursive(leftXSortedPoints, leftYSortedPoints)
    rightMinDistance, rightClosestPoints = enhanced_dnc_recursive(rightXSortedPoints, rightYSortedPoints)

    if math.isclose(leftMinDistance, rightMinDistance):
        d = leftMinDistance
        closestPoints = leftClosestPoints + rightClosestPoints
    elif leftMinDistance < rightMinDistance:
        d = leftMinDistance
        closestPoints = leftClosestPoints
    else: # leftMinDistance > rightMinDistance
        d = rightMinDistance
        closestPoints = rightClosestPoints

    # Remove previously counted pairs contained in M strip to avoid double count
    toRemove = []
    for pointSet in closestPoints:
        if (abs(pointSet[0][0] - x_m) < d and abs(pointSet[1][0] - x_m) < d):
            toRemove += [pointSet]
    for pointSet in toRemove:
        closestPoints.remove(pointSet)

    M = [point for point in ySortedPoints if abs(point[0] - x_m) < d]
    d_m = d
    closestPointsInM = []

    for i, A in enumerate(M):
        # j = 0
        for B in M[i + 1:]:
            if (abs(B[1] - A[1]) > d):
                break
            else:
                # j += 1
                # if (j > 7):
                #     print("Inner merge loop executing more than 7 times!")
                current_d = computeDistance(A, B)
                if math.isclose(current_d, d_m):
                    closestPointsInM += [[A,B]]
                elif current_d < d_m:
                    closestPointsInM = [[A,B]]
                    d_m = current_d
    if math.isclose(d_m, d):
        closestPoints += closestPointsInM
    elif d_m < d:
        closestPoints = closestPointsInM
        d = d_m
    return d, closestPoints

def computeDistance(A, B):
    return math.sqrt(math.pow((A[0] - B[0]),2) + math.pow((A[1] - B[1]),2))

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
        # points = read_file_to_list("inputs/input10^5-trial1.txt")

        # Measure execution time
        start_time = time.time()
        min_dist, closest_pairs = enhanced_divide_and_conquer_closest_pair(points)
        end_time = time.time()

        print(f"Enhanced Divide & Conquer took {end_time - start_time:.6f} seconds")
        print(f"Minimum Distance: {min_dist}")
        print("Closest Pairs:")
        for pair in closest_pairs:
            print(pair)
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'enhanced_dnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)