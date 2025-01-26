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
    
    points.sort(key=lambda point: point[1])
    ySorted = points
    distance, pairs = enhanced_dnc_recursive(ySorted)
    return distance, sort_pairs(pairs)

def enhanced_dnc_recursive(points):
    numberOfPoints = len(points)
    if numberOfPoints <= 1:
        return float('inf'), []

    x_median = getMedianX(points)
    leftPoints  = [point for point in points if point[0] <= x_median]
    rightPoints = [point for point in points if point[0] > x_median]

    # Could have all points less than or equal to the median - therefore not possible to divide anymore. To avoid infinite recursion:
    if len(leftPoints) == numberOfPoints or len(rightPoints) == numberOfPoints:
        print(f"Calling brute force on {numberOfPoints}")
        return brute_force_unsorted(points)

    leftMinDistance, leftClosestPoints = enhanced_dnc_recursive(leftPoints)
    rightMinDistance, rightClosestPoints = enhanced_dnc_recursive(rightPoints)

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
        if (abs(pointSet[0][0] - x_median) < d and abs(pointSet[1][0] - x_median) < d):
            toRemove += [pointSet]
    for pointSet in toRemove:
        closestPoints.remove(pointSet)

    M = [point for point in points if abs(point[0] - x_median) < d]
    d_m = d
    closestPointsInM = []

    for i, A in enumerate(M):
        for B in M[i + 1:]:
            if (abs(B[1] - A[1]) > d):
                break
            else:
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

def getMedianX(array):
    if len(array) == 1:
        return A[0][0]
    elif len(array) == 2:
        return (array[0][0] + array[1][0]) / 2
    medianIndex = len(array) // 2
    A = copy.deepcopy(array)
    return Select(A, medianIndex)

def Select(A, k):
    if len(A) == 1:
        return A[0][0]
    v = len(A) // 2
    r = partition(A, v)

    if r == k:
        return A[r][0]
    elif r > k:
        return Select(A[:r], k)
    else:
        return Select(A[r + 1:], k - r - 1)

def partition(A, pivotIndex):
    lengthA = len(A)
    if lengthA <= 1:
        return 0
    i = 1
    j = lengthA - 1
    if pivotIndex != 0:
        A[0], A[pivotIndex] = A[pivotIndex], A[0]
    pivot = A[0][0]
    while (i <= j):
        while i <= j and A[i][0] <= pivot :
            i += 1
        while i <= j and A[j][0] > pivot:
            j -= 1
        if (i < j):
            A[i], A[j] = A[j], A[i]
    if j != 0:
        A[j], A[0] = A[0], A[j]
    return j

def brute_force_unsorted(points):
    min_dist = float('inf')
    closest_pairs = []
    dist = 0.0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]

            dist = computeDistance(points[i], points[j])

            if dist < min_dist:
                min_dist = dist
                closest_pairs = [[p1, p2]]
            elif dist == min_dist:
                closest_pairs.append([p1, p2])

    return min_dist, closest_pairs

if __name__ == "__main__":
    try:
        # points = read_input_from_cli()
        points = read_file_to_list("inputs/input10^5-trial1.txt")
        # points = read_file_to_list("input1.txt")

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