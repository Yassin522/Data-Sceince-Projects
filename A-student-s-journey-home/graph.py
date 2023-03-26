from copy import deepcopy
from sklearn import preprocessing
import numpy as np


class player:
    def __init__(self, hp=0 , money=0):
        self.hp = hp
        self.money = money
        self.time = 0
class Node:
    def __init__(self, name, bus_watting_time , taxi_watting_time):
        self.name = name
        self.routes = []
        self.player= None
        self.bus_watting_time =bus_watting_time
        self.taxi_watting_time  = taxi_watting_time
    def player_arrive(self,hp,money):
        self.player = player(hp , money)

    def add_route(self, destination, bus_speed , taxi_speed , d , is_walking , bus_name):
        if is_walking:
            self.routes.append({destination:[bus_speed, taxi_speed, d, bus_name, 'foot']})
        else:
            self.routes.append({destination:[bus_speed, taxi_speed, d, bus_name, 'foot']})
            self.routes.append({destination:[bus_speed, taxi_speed, d, bus_name, 'bus']})
            self.routes.append({destination: [bus_speed, taxi_speed, d, bus_name, 'taxi']})


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name,bus_watting_time,taxi_watting_time):
        self.nodes[name] = Node(name,bus_watting_time,taxi_watting_time)
        self.nodes[name].player_arrive(0,0)
        return self.nodes[name]

    def add_route(self, source, destination,  bus_speed , taxi_speed , d , is_walking , bus_name):
        self.nodes[source].add_route(destination, bus_speed , taxi_speed , d , is_walking , bus_name)


def a_star(graph, start, goal, money, heuristic_function , cost_function):
    closed_set = set()
    open_set = {start.name}
    came_from = {}
    came_by = {}
    g_score = {start.name: 0}
    f_score = {start.name: g_score[start.name] + heuristic_function(start.name, goal.name , graph)}
    start.player.money=money
    start.player.hp = 100
    BN = None

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        if current == goal.name:
            return reconstruct_path(came_from,came_by, goal.name) , graph.nodes[current].player.time
        open_set.remove(current)
        closed_set.add(current)
        for i in graph.nodes[current].routes:
            key = list(i.keys())
            neighbor = key[0]
            value = list(i.values())
            d = value[0][2]
            bus_name = value[0][3]
            bus_speed = value[0][0]
            taxi_speed = value[0][1]
            mode  =value[0][4]
            d_money = graph.nodes[neighbor].player.money
            n_money = graph.nodes[current].player.money
            d_hp = graph.nodes[neighbor].player.hp
            n_hp = graph.nodes[current].player.hp
            d_time = graph.nodes[neighbor].player.time
            n_time= graph.nodes[current].player.time
            if mode == 'foot':
                tentative_g_score = g_score[current] + cost_function(graph , current , i)
                d_money = deepcopy(n_money)
                d_time = n_time + (d/5.5)
                d_hp = deepcopy(n_hp) - (d * 10)
            if mode == 'bus':
                tentative_g_score = g_score[current] + cost_function(graph , current , i)
                d_money = n_money - 400
                d_time = n_time + (d / bus_speed) + graph.nodes[current].bus_watting_time
                d_hp = deepcopy(n_hp) - (d * 5)
            if mode == 'taxi':
                tentative_g_score = g_score[current] + cost_function(graph , current , i)
                d_money = deepcopy(n_money) - (d*1000)
                d_time = n_time + (d / taxi_speed) + graph.nodes[current].taxi_watting_time
                d_hp = deepcopy(n_hp) + (d * 5)
                if  d_hp > 100:
                    d_hp = 100

            if neighbor in closed_set:
                continue

            if  d_hp <= 0 or  d_money< 0:
                continue
            tentative_f_score = tentative_g_score + heuristic_function(neighbor, goal.name, graph)

            if neighbor not in open_set:
                open_set.add(neighbor)
                tentative_is_better = True
            elif tentative_g_score < g_score[neighbor]:
                tentative_is_better = True
            else:
                tentative_is_better = False
            if tentative_is_better:
                graph.nodes[neighbor].player.money = d_money
                graph.nodes[neighbor].player.hp = d_hp
                graph.nodes[neighbor].player.time = d_time
                came_from[neighbor] = current
                came_by[neighbor] = mode
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_f_score
    return "Failure" ,0


def reconstruct_path(came_from,came_by, current):
    total_path = [current]
    while current in came_from:
        b = came_by[current]
        current = came_from[current]
        total_path.append([current , b])
        reverse_list=[]
        i= len(total_path)-1
        while i>=0:
            reverse_list.append(total_path[i])
            i=i-1
    return reverse_list


def time_heuristic(current, goal, graph):
    time = float("inf")
    for route in graph.nodes[current].routes:
        destination = list(route.keys())[0]
        speed, _, distance, _, mode = list(route.values())[0]
        if mode == "foot":
            t = distance / 5.5
        elif mode == "bus":
            t = distance / speed + graph.nodes[current].bus_watting_time
        elif mode == "taxi":
            t = distance / speed + graph.nodes[current].taxi_watting_time
        if t < time:
            time = t
    return time


def money_heuristic(current, goal, graph):

    cost = float("inf")
    for route in graph.nodes[current].routes:
        destination = list(route.keys())[0]
        _, _, distance, _, mode = list(route.values())[0]
        if mode == "foot":
            c = 0
        elif mode == "bus":
            c = 400
        elif mode == "taxi":
            c = distance * 1000
        if c < cost:
            cost = c
    return cost


def effort_heuristic(current, goal, graph):
    effort = float("inf")
    for route in graph.nodes[current].routes:
        destination = list(route.keys())[0]
        _, _, distance, _, mode = list(route.values())[0]
        if mode == "foot":
            e = distance * 10
        elif mode == "bus":
            e = distance * 5
        elif mode == "taxi":
            e = - distance * 5
        if e < effort:
            effort = e
    return effort

def time_cost(graph ,node , next_node):
    value = list(next_node.values())
    bus_speed = value[0][0]
    taxi_speed = value[0][1]
    d = value[0][2]
    mode = value[0][4]
    if mode == 'foot':
        time = (d/5.5)
    elif mode == 'bus':
        time = (d / bus_speed) + graph.nodes[node].bus_watting_time
    elif mode == 'taxi':
        time = (d / taxi_speed) + graph.nodes[node].taxi_watting_time
    return time

def effort_cost(graph , node , next_node):
    key = list(next_node.keys())
    value = list(next_node.values())
    d = value[0][2]
    mode = value[0][4]
    if mode == 'foot':
        effort =  d * 10
    elif mode == 'bus':
        effort = d * 5
    elif mode == 'taxi':
        effort = -(d * 5)
    return effort

def money_cost(graph , node , next_node):
    value = list(next_node.values())
    d = value[0][2]
    mode = value[0][4]
    if mode == 'foot':
        new_money = 0
    elif mode == 'bus':
        new_money = 400
    elif mode == 'taxi':
        new_money = d * 1000
    return new_money

def All_cost(graph , node , next_node):
    arr = np.array([money_cost(graph , node , next_node) , effort_cost(graph , node , next_node) , time_cost(graph,node , next_node)])
    All = preprocessing.normalize([arr])
    return All.sum()

graph = Graph()

A=graph.add_node("A", 0 , 0)
B=graph.add_node("B", 0 , 0)
C=graph.add_node("C", 1, 0.5)
D=graph.add_node("D", 1, 0)
E=graph.add_node("E", 0 , 0)
F=graph.add_node("F", 0.5 , 0)

graph.add_route("A", "B", 10, 100, 5, False,'M')
graph.add_route("A", "C", 15, 150, 10, False , 'M')
graph.add_route("B", "D", 5, 500, 3, False , 'C')
graph.add_route("B", "E", 5, 500, 3, False , 'H')
graph.add_route("C", "E", 20, 200, 15, False , 'S')
graph.add_route("D", "F", 8, 8, 5, False , 'H')
graph.add_route("E", "F", 10, 10, 5, False , 'H')


shortest_path,Time = a_star(graph, A, F, 20000 , effort_heuristic , effort_cost)
"""
[['A', 'foot'], ['B', 'foot'], ['D', 'taxi'], 'F']
money:  15000
hp:  45
time:  2.0795454545454546
"""

# shortest_path,Time = a_star(graph, A, F, 20000 , time_heuristic , money_cost)
"""
[['A', 'foot'], ['B', 'foot'], ['E', 'taxi'], 'F']
money:  15000
hp:  45
time:  1.9545454545454546
"""

# shortest_path,Time = a_star(graph, A, F, 20000 , money_heuristic , effort_cost)
"""
[['A', 'taxi'], ['B', 'taxi'], ['E', 'taxi'], 'F']
money:  7000
hp:  100
time:  0.556
"""

# shortest_path,Time = a_star(graph, A, F, 2000 , time_heuristic , effort_cost)
"""
[['A', 'bus'], ['B', 'bus'], ['E', 'bus'], 'F']
money:  800
hp:  35
time:  1.6
"""

# shortest_path,Time = a_star(graph, A, F, 800 , money_heuristic , effort_cost)
"""
[['A', 'bus'], ['B', 'bus'], ['D', 'foot'], 'F']
money:  0
hp:  10
time:  2.0090909090909093
"""

# shortest_path,Time = a_star(graph, A, F, 20000 , effort_heuristic , time_cost)
"""
[['A', 'taxi'], ['B', 'taxi'], ['D', 'taxi'], 'F']
money:  7000
hp:  100
time:  0.681
"""

# shortest_path,Time = a_star(graph, A, F, 20000 , money_heuristic , time_cost)
"""
[['A', 'taxi'], ['B', 'taxi'], ['E', 'bus'], 'F']
money:  11600
hp:  75
time:  0.556
"""
print(shortest_path)
if shortest_path != 'Failure':
    print("money: ", F.player.money)
    print("hp: ", F.player.hp)
    print("time: ", Time)
