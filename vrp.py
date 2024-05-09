import ast
import math
import sys
import heapq
from collections import defaultdict

class Point:
    def __init__(self, line):
        id, pickup, dropoff = line.split(' ')
        self.id = int(id)
        self.pickup = ast.literal_eval(pickup)
        self.dropoff = ast.literal_eval(dropoff)

class VRP:

    def __init__(self, filename: str):
        content = open(filename).readlines()[1:]
        self.points = {}
        for line in content:
            point = Point(line.rstrip())
            self.points[point.id] = point
    
    def euclidean_distance(self, start, end):
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    
    def time_to_route(self, start, route: Point):
        route_time = self.euclidean_distance(start, route.pickup)
        return route_time + self.euclidean_distance(route.pickup, route.dropoff)
    
    def next_nearest_point(self, curr_location):
        min_heap = []
        for id in self.points.keys():
            min_heap.append((self.euclidean_distance(curr_location, self.points[id].pickup), id))
        heapq.heapify(min_heap)
        return heapq.heappop(min_heap)[1]

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
                #print('***Trigger Hit***')
                #print('total time for trigger: ' + str(curr_time+dest_time))
                driver += 1
                prev_route = origin
                curr_time = 0.0
            else:
                prev_route = dest 
                del self.points[next_point]
                drivers[driver].append(dest.id)

            #print('Curr Route for driver ' + str(driver) + ': ' + str(drivers[driver]))
            #print('Curr Runtime: ' + str(curr_time))
            #print('Time to Destination from current Dropoff: ' + str(dest_time))

        for value in drivers.values():
            if value: print(value)

if __name__ == '__main__':
    filename = sys.argv[1]    
    vrp = VRP(filename)
    vrp.routes()