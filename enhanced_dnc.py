import sys
import copy
from itertools import combinations
import math
import time
from a1_utils import read_input_from_cli, distance, write_output_to_file,read_file_to_list, generate_random_input, sort_pairs


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
    
    xSortedPoints =  sorted(points, key=lambda pair: pair[0])
    ySortedPoints = sorted(points, key=lambda pair: pair[1])
    distance, pairs = enhanced_dnc_recursive(xSortedPoints, ySortedPoints, 0, len(points) - 1)
    return distance, sort_pairs(pairs)

def enhanced_dnc_recursive(xSortedPoints, ySortedPoints, low, high):
    if high - low <= 1:
        return computeDistance(xSortedPoints[low], xSortedPoints[high]), [[xSortedPoints[low], xSortedPoints[high]]]
    elif high - low == 2:
        mid = low + 1
        distanceLowMid = computeDistance(xSortedPoints[low], xSortedPoints[mid])
        closestOf3 = [[xSortedPoints[low], xSortedPoints[mid]]]
        minDistanceOf3 = distanceLowMid

        distanceLowHigh = computeDistance(xSortedPoints[low], xSortedPoints[high])
        if math.isclose(distanceLowHigh, minDistanceOf3):
            closestOf3.append([xSortedPoints[low], xSortedPoints[high]])
        elif distanceLowHigh < minDistanceOf3:
            closestOf3 = [[xSortedPoints[low], xSortedPoints[high]]]
            minDistanceOf3 = distanceLowHigh

        distanceMidHigh = computeDistance(xSortedPoints[mid], xSortedPoints[high])
        if math.isclose(distanceMidHigh, minDistanceOf3):
            closestOf3.append([xSortedPoints[mid], xSortedPoints[high]])
        elif distanceMidHigh < minDistanceOf3:
            closestOf3 = [[xSortedPoints[mid], xSortedPoints[high]]]
            minDistanceOf3 = distanceMidHigh
       
        return minDistanceOf3, closestOf3

    splitIndex = math.floor((high + low) / 2)
    x_m = xSortedPoints[splitIndex][0]
    leftMinDistance, leftSortedPoints = enhanced_dnc_recursive(xSortedPoints, ySortedPoints, low, splitIndex)
    rightMinDistance, rightSortedPoints = enhanced_dnc_recursive(xSortedPoints, ySortedPoints, splitIndex + 1, high)
    if leftMinDistance < rightMinDistance:
        d = leftMinDistance
        closestPoints = leftSortedPoints
    elif leftMinDistance > rightMinDistance:
        d = rightMinDistance
        closestPoints = rightSortedPoints
    elif leftMinDistance == rightMinDistance:
        d = leftMinDistance
        closestPoints = leftSortedPoints
        for point in rightSortedPoints:
            closestPoints.append(point)

    for pointSet in closestPoints:
        if pointSet[0][0] == x_m and pointSet[1][0] == x_m:
            closestPoints.remove(pointSet)
    M = []
    for point in ySortedPoints:
        if point[0] < xSortedPoints[low][0] or point[0] > xSortedPoints[high][0]:
            continue
        delta = abs(point[0] - x_m)
        if abs(point[0] - x_m) < d:
            M.append(point)
    d_m = d
    closestPointsInM = []
    for i, A in enumerate(M):
        for B in M[i + 1:]:
            if (abs(B[1] - A[1]) > d):
                break
            else:
                current_d = computeDistance(A, B)
                if math.isclose(current_d, d_m):
                    closestPointsInM.append([A,B])
                elif current_d < d_m:
                    closestPointsInM = [[A,B]]
                    d_m = current_d
    if math.isclose(d_m, d):
        for pointSet in closestPointsInM:
            closestPoints.append(pointSet)
    elif d_m < d:
        closestPoints = closestPointsInM
        d = d_m
    return d, closestPoints

def computeDistance(A, B):
    return math.sqrt(math.pow((A[0] - B[0]),2) + math.pow((A[1] - B[1]),2))

if __name__ == "__main__":
    try:
        points = read_input_from_cli()
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
        write_output_to_file(distance=min_dist, points=closest_pairs, output_file= 'enhance_ddnc_output.txt')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)