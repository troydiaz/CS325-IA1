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
    
    # xSortedPoints = mergeSort(points, 0)
    # ySortedPoints = mergeSort(points, 1)
    xSortedPoints =  sorted(points, key=lambda pair: pair[0])
    ySortedPoints = sorted(points, key=lambda pair: pair[1])
    distance, pairs = enhanced_dnc_recursive(xSortedPoints, ySortedPoints, 0, len(points) - 1)

    return distance, pairs

def enhanced_dnc_recursive(xSortedPoints, ySortedPoints, low, high):
    if high - low <= 1:
        return computeDistance(xSortedPoints[low], xSortedPoints[high]), [[xSortedPoints[low], xSortedPoints[high]]]
    elif high - low == 2:
        mid = low + 1
        distancelowmid = computeDistance(xSortedPoints[low], xSortedPoints[mid])
        leftSortedOf3 = [[xSortedPoints[low], xSortedPoints[mid]]]
        minDistanceOf3 = distancelowmid

        distancelowhigh = computeDistance(xSortedPoints[low], xSortedPoints[high])
        if distancelowhigh < minDistanceOf3:
            leftSortedOf3 = [[xSortedPoints[low], xSortedPoints[high]]]
            minDistanceOf3 = distancelowhigh
        elif distancelowhigh == minDistanceOf3:
            leftSortedOf3.append([xSortedPoints[low], xSortedPoints[high]])
        
        distancemidhigh = computeDistance(xSortedPoints[mid], xSortedPoints[high])
        if distancemidhigh < minDistanceOf3:
            leftSortedOf3 = [[xSortedPoints[mid], xSortedPoints[high]]]
            minDistanceOf3 = distancemidhigh
        elif distancemidhigh == minDistanceOf3:
            leftSortedOf3.append([xSortedPoints[mid], xSortedPoints[high]])

        return minDistanceOf3, leftSortedOf3
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
    M = []
    for point in ySortedPoints:
        if point[0] < xSortedPoints[low][0] or point[0] > xSortedPoints[high][0]:
            break
        thePointX = point[0]
        delta = abs(point[0] - x_m)
        if abs(point[0] - x_m) < d:
            M.append(point)
    d_m = d
    closestPointsInM = []
    for i, pointA in enumerate(M):
        for pointB in M[i + 1:]:
            if (abs(pointB[1] - pointA[1]) >= d):
                break
            else:
                current_d = computeDistance(pointA, pointB)
                if current_d < d_m:
                    closestPointsInM = [[pointA,pointB]]
                    d_m = current_d
                elif current_d == d_m:
                    closestPointsInM.append([pointA,pointB])
    if d_m < d:
        closestPoints = closestPointsInM
        d = d_m
    elif d_m == d:
        for pointSet in closestPointsInM:
            closestPoints.append(pointSet)
    if len(closestPoints) > 0:
        closestPointsSorted = sort_pairs(closestPoints)
    else:
        closestPointsSorted = closestPoints
    return d, closestPointsSorted

def mergeSort(points, sortingCoordinate):
    mergeArray = copy.deepcopy(points)
    mergeSortHelper(points, mergeArray, sortingCoordinate, 0, len(points) - 1)
    return mergeArray

def mergeSortHelper(points, mergeArray, sortingCoordinate, low, high):
    if high - low <= 0:
        return
    mid = math.floor((high + low) / 2)
    mergeSortHelper(points, mergeArray, sortingCoordinate, low, mid)
    mergeSortHelper(points, mergeArray, sortingCoordinate, mid + 1, high)
    merge(points, mergeArray, sortingCoordinate, low, mid, high)
    return

def merge(points, mergeArray, sortingCoordinate, low, mid, high):
    i = low
    j = mid + 1
    k = low
    while i <= mid and j <= high:
        if points[i][sortingCoordinate] <= points[j][sortingCoordinate]:
            mergeArray[k] = points[i]
            i += 1
        else:
            mergeArray[k] = points[j]
            j += 1
        k += 1
    while i <= mid:
        mergeArray[k] = points[i]
        i += 1
        k += 1
    while j <= high:
        mergeArray[k] = points[j]
        j += 1
        k += 1
    k = low
    while k <= high:
        points[k] = mergeArray[k]
        k += 1
    return

def computeDistance(pointA, pointB):
    return math.sqrt(math.pow((pointA[0] - pointB[0]),2) + math.pow((pointA[1] - pointB[1]),2))

if __name__ == "__main__":
    try:
        # points = read_input_from_cli()
        points = read_file_to_list("input102.txt")

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