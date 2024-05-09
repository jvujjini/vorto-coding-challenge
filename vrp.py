import ast
import math
import sys
import heapq
from collections import defaultdict

'''
Model to wrap each point in the map
'''
class Point:
    def __init__(self, line):
        id, pickup, dropoff = line.split(' ')
        self.id = int(id)
        self.pickup = ast.literal_eval(pickup)
        self.dropoff = ast.literal_eval(dropoff)

class VRP:

    '''
    Initializes the input to add the points in a dictionary
    '''
    def __init__(self, filename: str):
        content = open(filename).readlines()[1:]
        self.points = {}
        for line in content:
            point = Point(line.rstrip())
            self.points[point.id] = point
    
    '''
    Distance between start and end points
    '''
    def euclidean_distance(self, start, end):
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    
    '''
    Time to dropoff the next package from the current location
    '''
    def time_to_route(self, start, route: Point):
        route_time = self.euclidean_distance(start, route.pickup)
        return route_time + self.euclidean_distance(route.pickup, route.dropoff)
    
    '''
    Method to get the next nearest point from the latest dropoff location or origin
    '''
    def next_nearest_point(self, curr_location):
        min_heap = []
        for id in self.points.keys():
            min_heap.append((self.euclidean_distance(curr_location, self.points[id].pickup), id))
        heapq.heapify(min_heap)
        return heapq.heappop(min_heap)[1]
    
    '''
    Method to return the routes for each driver 
    '''
    def routes(self):
        origin = Point('0 (0.0,0.0) (0.0,0.0)')
        prev_route = origin
        driver = 0
        drivers = defaultdict(list)
        curr_time = 0.0

        while len(self.points.keys()) > 0:
            next_point = self.next_nearest_point(prev_route.dropoff)
            dest = self.points[next_point]

            curr_time += self.time_to_route(prev_route.dropoff, dest)
            dest_time = self.euclidean_distance(dest.dropoff, origin.pickup)

            if curr_time + dest_time > 720.0:
                driver += 1
                prev_route = origin
                curr_time = 0.0
            else:
                prev_route = dest 
                del self.points[next_point]
                drivers[driver].append(dest.id)

        for value in drivers.values():
            if value: print(value)

if __name__ == '__main__':
    filename = sys.argv[1]    
    vrp = VRP(filename)
    vrp.routes()