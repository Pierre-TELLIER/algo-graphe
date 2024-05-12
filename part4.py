import heapq
import math
from part3 import  calculer_degats_optimal
from classes import *



"""
heuristique prenant en compte les dégats de fuite d'eau mais ne fonctionnant pas dans le contexte

def heuristic_degats(node, destination, config):
    dist = distance(node, destination)
    degats =  calculer_degats_optimal(config)
    heuristic_value = dist * (1 + degats)
    return heuristic_value
"""

def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node2.y - node1.y) ** 2)


def heuristic(node, destination, config, time):
    dist = distance(node, destination)
    return dist  



def a_star(config, start, goal):
    N = config.n
    grid = [[0] * N for _ in range(N)]
    
    for o in config.obstacle:
        for x in range(o.x1, o.x2 + 1):
            for y in range(o.y1, o.y2 + 1):
                if 0 <= x < N and 0 <= y < N:
                    grid[x][y] = 1

    open_heap = []
    start_node = Node(start[0], start[1], None)
    goal_node = Node(goal[0], goal[1], None)
    heapq.heappush(open_heap, start_node)

    closed_set = set()
    nodes = {(start[0], start[1]): start_node}

    while open_heap:
        current = heapq.heappop(open_heap)
        if (current.x, current.y) == (goal_node.x, goal_node.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add((current.x, current.y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current.x + dx, current.y + dy
            if 0 <= nx < N and 0 <= ny < N and grid[nx][ny] != 1:
                neighbor = nodes.get((nx, ny), Node(nx, ny, None))
                if (nx, ny) in closed_set:
                    continue

                tentative_g_score = current.g + 1
                if neighbor not in open_heap or tentative_g_score < neighbor.g:
                    neighbor.g = tentative_g_score
                    neighbor.h = heuristic(neighbor, goal_node, config, current.g)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current

                    if neighbor not in open_heap:
                        heapq.heappush(open_heap, neighbor)
                        nodes[(nx, ny)] = neighbor

    return []

obstacles = [Obstacle(3, 3, 5, 5), Obstacle(24, 8, 26, 24)]
villages = [Village(1, 0, 0, 10), Village(2, 9, 9, 10)]
drones = [Drone(0, 0, [])] 
config = Config(None, drones, obstacles, villages, 10, True)

start = (0, 0)
goal = (9, 9)

path = a_star(config, start, goal)
print("Path from start to goal:", path)

"""
Fonctions mentionnées sur le rapport comme ne fonctionnant pas leur objectif étant de calculer pour chaque drône le trajet optimal au niveau de la minimisation des degats 
de fuite d'eau et de l'acheminement messages-objets


class Drone(Drone):
    def plan_path(self, config, start, goal):
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        self.trajet = a_star(config, trajet[0], trajet[len(trajet) - 1])
        if trajet:
            return [(node.x, node.y) for node in trajet]
        else:
            return []
    
    def update_trajectory(self, config, villages):
        new_trajet = []
        for i, village in enumerate(villages):
            if i == 0:
                new_trajet.append(village)
            else:
                trajet = self.plan_path(config, new_trajet[-1].pos, village.pos)
                for pos in path:
                    new_trajet.append(Village(pos[0], pos[1], 0))
                new_trajet.append(village)
        self.trajet = new_trajet 
    



Test destiné à tester les fonctions plan_path et update_trajectory
N = 100  

coordonnees_villages = [
    (1, 10, 10),
    (2, 10, 22),
    (3, 20, 14),
    (4, 20, 18),
    (5, 30, 14),
    (6, 30, 18),
    (7, 40, 10),
    (8, 40, 22) ]


villages = []

for village_id, x, y in coordonnees_villages:
    village = Village(village_id, x, y, N) 
    villages.append(village)


distances = {
        (1, 2): 10, (1, 3): 15, (1, 4): 20,
        (2, 1): 10, (2, 3): 35, (2, 4): 25,
        (3, 1): 15, (3, 2): 35, (3, 4): 30,
        (4, 1): 20, (4, 2): 25, (4, 3): 30 }


drones = []

drone1 = Drone(3, 4, None)
drones.append(drone1)
drone2 = Drone(1, 3, None)
drones.append(drone2)

obstacles = []

obstacle1 = Obstacle(3, 3, 5, 5) 
obstacles.append(obstacle1)

obstacle2 = Obstacle(24, 8, 26, 24) 
obstacles.append(obstacle2)

config = Config(None, drones, obstacles, villages, 100, True)

for drone in drones:
    drone.update_trajectory(config, villages)

print("trajet du drone 1", drones[0].trajet)
print("trajet du drone 2", drones[1].trajet)
"""