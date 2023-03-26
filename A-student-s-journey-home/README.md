# A-student-s-journey-home
This code is a simple implementation of a Graph data structure that simulates travelling between different locations represented as nodes on the graph. Each node has some attributes like name, waiting time for a bus or taxi, and routes to other nodes.

player class defines the attributes of player such as health points (hp), money and time taken. Node class defines the attributes of a location such as name, routes, player and waiting time for bus and taxi. Graph class is used to create a graph of locations and the routes between them.

The Graph class has two main methods: add_node and add_route. The add_node method is used to add a new location to the graph, and the add_route method is used to add a route between two existing locations on the graph. The player_arrive method is used to assign the player to the current node. The add_route method is used to add the route between two nodes with its attributes (destination, bus_speed, taxi_speed, distance, is_walking, bus_name)

The a_star function is used to search for the shortest path between a start and a goal node, with the given money and defined heuristic and cost functions. Also it use cost function to manage the money and health point of player and time taken to reach the destination.

Imported Libraries are :
deepcopy from copy
preprocessing from sklearn
numpy
The deepcopy is used to create a new object with a new memory address.
