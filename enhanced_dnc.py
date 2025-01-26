import sys
import copy
from itertools import combinations
import math
import time
import random
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

    x_median, leftPoints, rightPoints = getMedian(points)

    # Could have all points less than or equal to the median - therefore not possible to divide anymore. To avoid infinite recursion:
    if len(leftPoints) == numberOfPoints or len(rightPoints) == numberOfPoints:
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

def getMedian(A):
    if len(A) == 1:
        return A[0][0], A, []
    elif len(A) == 2:
        return (A[0][0] + A[1][0]) / 2, A[0], A[1]
    medianIndex = len(A) // 2
    return Select(A, medianIndex)

def Select(A, k):
    if len(A) == 1:
        return A[0][0], A, []
    v = random.randint(0, len(A) - 1)
    v = 0
    n = len(A)
    nDiv5 = n // 5
    if nDiv5 == 0:
        v = 0
    else:
        M = [[] for l in range (0, nDiv5)]
        for i in range(0, nDiv5):
            if i == nDiv5:
                count = n % 5
            else:
                count = 5
            for j in range(0, count):
                M[i].append(A[i * 5 + j][0])
        MM = SelectMedian(M, n // 10)
        for i in range(0, n):
            if A[i][0] == MM:
                v = i
                break
    r, pivot = partitionStable(A, v)

    if r == k:
        return A[pivot][0], A[:r], A[r:]
    elif r > k:
        return Select(A[:r], k)
    else:
        return Select(A[r + 1:], k - r - 1)

def partitionStable(A, pivotIndex):
    i = 0
    j = len(A) - 1
    pivot = A[pivotIndex]
    B = [[] for i in range(len(A))]
    n = len(A)
    for k in range(0, n):
        if k == pivotIndex:
            pivotPlaceB = j
        if A[k][0] < pivot[0]:
            B[i] = A[k]
            i += 1
        else:
            B[j] = A[k]
            j -= 1
    for k in range(0, i):
        A[k] = B[k]
    h = 0
    for k in range(n - 1, i - 1, -1):
        A[i + h] = B[k]
        h += 1
    distanceFromI = n - 1 - pivotPlaceB
    return i, i + distanceFromI

def SelectMedian(A, k):
    if len(A) == 1:
        return 0
    v = random.randint(0, len(A) - 1)
    r = partition(A, v)
    if r == k:
        return A[r]
    elif r > k:
        return SelectMedian(A[:r], k)
    else:
        return SelectMedian(A[r + 1:], k - r - 1)    

def partition(A, pivotIndex):
    lengthA = len(A)
    if lengthA <= 1:
        return 0
    i = 1
    j = lengthA - 1
    if pivotIndex != 0:
        A[0], A[pivotIndex] = A[pivotIndex], A[0]
    pivot = A[0]
    while (i <= j):
        while i <= j and A[i] <= pivot :
            i += 1
        while i <= j and A[j] > pivot:
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
        points = read_input_from_cli()
        # points = read_file_to_list("inputs/input10^5-trial1.txt")
        # points = read_file_to_list("input3.txt")

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