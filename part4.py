#Algorithme proposee A* avec heurestique multiples

import heapq

# Importation des classes de votre fichier (imaginaire pour cet exemple)
from classes import Config, Village, Obstacle, Drone

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0
    
    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Utilise la distance de Manhattan comme heuristique
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star(config, start, goal):
    N = config.n
    grid = [[0] * N for _ in range(N)]
    
    # Mark obstacles in the grid from config
    for o in config.obstacle:
        for x in range(o.x1, o.x2 + 1):
            for y in range(o.y1, o.y2 + 1):
                if 0 <= x < N and 0 <= y < N:
                    grid[x][y] = 1

    open_heap = []
    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])
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
                neighbor = nodes.get((nx, ny), Node(nx, ny))
                
                if (nx, ny) in closed_set:
                    continue
                
                tentative_g_score = current.g + 1
                
                if neighbor not in open_heap or tentative_g_score < neighbor.g:
                    neighbor.g = tentative_g_score
                    neighbor.h = heuristic(neighbor, goal_node)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current
                    
                    if neighbor not in open_heap:
                        heapq.heappush(open_heap, neighbor)
                        nodes[(nx, ny)] = neighbor
    
    return []

# Example configuration
obstacles = [Obstacle(3, 3, 5, 5)]
villages = [Village(1, 0, 0), Village(2, 9, 9)]
drones = [Drone(0, 0)]
config = Config(None, drones, obstacles, villages, 10, True)

start = (0, 0)
goal = (9, 9)

path = a_star(config, start, goal)
print("Path from start to goal:", path)
