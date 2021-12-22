import sys
import heapq
import math

TRAIN_COLOURS = ['red', 'green']

class Station:

    def __init__(self, colour):
        '''
        Class for saving information about a station of the network (node). 
        Contains two types of attributes:
        1. Attrs about the structure of the metro network:
        - colour of the station
        - connections to another stations

        2. Attrs necesary for the Dijkstra algorithm:
        - distance to starting node
        - parent node, for tracking backards the route to the starting node
        - checked, to avoid checking twice the same node.
        '''
        self.colour = colour
        self.connections = []

        self.distance = math.inf
        self.parent =  None
        self.checked = False


class ModifiedDijkstra:
    
    def __init__(self):
        '''
        Two principal data structures for the algorithm:
        - self.stations: With format {node_name: node_obj (type Station), ...}
        - self.queue: Priority queue of nodes to review, with format [(node_priority, node_name), ...]
        '''

        self.stations = dict()
        self.queue = []


    def read_file(self, path):
        '''
        Reads a the .txt file at the indicated path, containing the structure of 
        the Metro network. Saves the information of each node (in objects type Station) and its conections 
        in the dict self.stations. 
        '''

        with open(path, 'r') as f:

            line = f.readline().strip()
            while line:
                name, colour = line.split(',')
                self.stations[name] = Station(colour)
                
                line = f.readline().strip()

            line = f.readline().strip()
            while line:
                first_station_name, second_station_name = line.split(',')
                self.stations[first_station_name].connections.append(second_station_name)
                self.stations[second_station_name].connections.append(first_station_name)

                line = f.readline().strip()


    def train_stops(self, train_colour, station_colour) -> bool:
        '''
        Given the colour of the train and of the station, returns a bool
        indicating wether the train stops or not in that station.
        '''

        return (train_colour == station_colour) or (station_colour not in TRAIN_COLOURS) or (train_colour not in TRAIN_COLOURS)


    def track_route(self, starting_station_name, final_station_name, train_colour):
        '''
        Given the starting and final station names, tracks the route from one to the another
        using the parent attribute from the Dijkstra algorithm. Returns a string indicating 
        the route in the format 'A->B->C->....->F'.
        '''

        route = []
        current_station_name = final_station_name
        current_station = self.stations[current_station_name]

        route.append(current_station_name)

        while current_station_name != starting_station_name:
            
            current_station_name = current_station.parent
            
            assert current_station_name is not None
            
            current_station = self.stations[current_station_name]
            
            if self.train_stops(train_colour, current_station.colour):
                route.append(current_station_name)

        route.reverse()
        return '->'.join(route)
        

    def find_shortest_path(self, starting_station_name, final_station_name, train_colour='') -> str:
        '''
        Finds the shortest path between two stations, given the starting and final stations 
        names and the train colour. Returns the route in the same format of the method 
        track_route(). 
        '''

        # Check if we're already there
        if starting_station_name == final_station_name:
            return starting_station_name

        # Check if it's possible to reach the final station because of the colours
        if not self.train_stops(train_colour, self.stations[final_station_name].colour):
            return f"It's not possible to reach {final_station_name} on a train of colour {train_colour}!"

        # Initialize the algorithm
        self.stations[starting_station_name].distance = 0
        heapq.heappush(self.queue, (self.stations[starting_station_name].distance, starting_station_name))
        
        assert len(self.queue) == 1

        # Loop while there are stations to review
        while self.queue:
            current_station_distance, current_station_name = heapq.heappop(self.queue)
            
            self.stations[current_station_name].checked = True

            for connected_station_name in self.stations[current_station_name].connections:
                connected_station = self.stations[connected_station_name]

                if not connected_station.checked:
                    
                    # If the train stops, sum 1 to distance (number of stations to travel). If not, don't sum. 
                    if self.train_stops(train_colour, connected_station.colour):
                        weight = 1
                        
                    else: 
                        weight = 0
                    
                    if current_station_distance + weight < connected_station.distance:
                        connected_station.distance = current_station_distance + weight
                        connected_station.parent = current_station_name
                        
                        self.stations[connected_station_name] = connected_station

                        # If we reached the final station, backtrack the route and return. 
                        if connected_station_name == final_station_name:
                            return self.track_route(starting_station_name, final_station_name, train_colour)

                        heapq.heappush(self.queue, (connected_station.distance, connected_station_name))

        return f"There are no routes between {starting_station_name} and {final_station_name}!"



if __name__ == '__main__':

    if (4 <= len(sys.argv) <= 5):

        modified_dijkstra = ModifiedDijkstra()
        modified_dijkstra.read_file(sys.argv[1])
        
        if len(sys.argv) == 4:
            print(modified_dijkstra.find_shortest_path(sys.argv[2], sys.argv[3]))

        elif len(sys.argv) == 5:
            print(modified_dijkstra.find_shortest_path(sys.argv[2], sys.argv[3], sys.argv[4]))

    elif len(sys.argv) < 4:
        print('Arguments missing!')

    elif len(sys.argv) > 5:
        print('Too many arguments!')
    