import ast
import math
import sys
from collections import defaultdict

class Route:
    def __init__(self, line):
        id, pickup, dropoff = line.split(' ')
        self.id = int(id)
        self.pickup = ast.literal_eval(pickup)
        self.dropoff = ast.literal_eval(dropoff)

class VRP:

    def __init__(self, filename: str):
        self.lines = []
        with open(filename) as file:
            self.lines = [line.rstrip() for line in file]
        self.lines = self.lines[1:]
    
    def euclidean_distance(self, start, end):
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    
    def time_to_route(self, start, route: Route):
        route_time = self.euclidean_distance(start, route.pickup)
        return route_time + self.euclidean_distance(route.pickup, route.dropoff)

    def vehicle_routing_problem(self):
        origin = Route('0 (0.0,0.0) (0.0,0.0)')
        prev_route = origin
        driver = 0
        drivers = defaultdict(list)
        curr_time = 0.0

        for line in self.lines:
            route = Route(line)  

            curr_time += self.time_to_route(prev_route.dropoff, route)
            dest_time = self.euclidean_distance(route.dropoff, origin.pickup)
            
            if curr_time + dest_time > 720.0:
                #print('***Trigger Hit***')
                #print('total time for trigger: ' + str(curr_time+dest_time))
                driver += 1
                curr_time = self.time_to_route(origin.dropoff, route)
            
            prev_route = route            
            drivers[driver].append(route.id)

            #print('Curr Route for driver ' + str(driver) + ': ' + str(drivers[driver]))
            #print('Curr Runtime: ' + str(curr_time))
            #print('Time to Destination from current Dropoff: ' + str(dest_time))

        for value in drivers.values():
            if value: print(value)

if __name__ == '__main__':
    filename = sys.argv[1]    
    vrp = VRP(filename)
    vrp.vehicle_routing_problem()