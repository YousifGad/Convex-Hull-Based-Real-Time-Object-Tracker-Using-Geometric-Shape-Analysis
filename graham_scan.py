"""
This code implements the Graham Scan algorithm to compute the convex hull
of a set of 2D points. It was built as part of exploration of computational
geometry while working on the Convex Hull Object Tracker.
"""

# Input: A set of random 2D points (x, y)
# Output: Plot those points, draw the convex hull around them

import matplotlib.pyplot as plt
import random
import math

def random_points(n, min_i=0, max_i=100):
    points = [(random.randint(min_i,max_i),random.randint(min_i,max_i)) for i in range(n)]
    return points


def get_pivot(points):
    points_y = [point[1] for point in points]
    pivot_y = min(points_y)
    z = []
    for point in points:
        if point[1] == pivot_y:
            z.append(point[0])
    pivot_x = min(z)
    return (pivot_x, pivot_y)


def sort_by_angle(points, pivot):
    def polar_angle(p):
        return math.atan2(p[1] - pivot[1], p[0] - pivot[0])
    
    points_without_pivot = [p for p in points if p != pivot]
    return sorted(points_without_pivot, key=polar_angle)

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def graham_scan(points):
    pivot = get_pivot(points)
    sorted_points = sort_by_angle(points, pivot)

    hull = [pivot, sorted_points[0]]

    for point in sorted_points[1:]:
        while len(hull) >= 2 and cross(hull[-2],hull[-1], point) <= 0:
            hull.pop()
        hull.append(point)
    return hull



test_points = random_points(50) 
hull = graham_scan(test_points)

x_vals = [point[0] for point in test_points]
y_vals = [point[1] for point in test_points]

hull_x = [point[0] for point in hull] + [hull[0][0]]
hull_y = [point[1] for point in hull] + [hull[0][1]]

plt.scatter(x_vals, y_vals)
plt.plot(hull_x, hull_y, "r--", linewidth=2)
plt.title("Convex Hull using Graham Scan")
plt.grid(True)
plt.show()
