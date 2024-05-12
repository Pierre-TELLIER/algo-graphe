import heapq
import math
from classes import Config, Village, Obstacle, Drone, Node

def distance(node1, node2):
    return math.sqrt((node1.x - node2.x)*2 + (node2.y - node1.y)*2)

def heuristic(node, destination, config, time):
    dist = distance(node, destination)
    return dist  # Simple heuristic for demonstration

def a_star(config, start, goal):
    N = config.n
    grid = [[0] * N for _ in range(N)]
    
    # Setting up obstacles in the grid
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

def plan_path(self, g, start, goal):
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])
        path = self.a_star_path(g, start_node, goal_node)
        if path:
            return [(node.x, node.y) for node in path]
        else:
            return []

def update_trajectory(self, g, villages):
        new_trajet = []
        for i, village in enumerate(villages):
            if i == 0:
                new_trajet.append(village)
            else:
                path = self.plan_path(g, new_trajet[-1].pos, village.pos)
                for pos in path:
                    new_trajet.append(Village(pos[0], pos[1], 0))
                new_trajet.append(village)
        self.trajet = new_trajet
# Example configuration with the correct Drone instantiation
obstacles = [Obstacle(3, 3, 5, 5), Obstacle(24, 8, 26, 24)]
villages = [Village(1, 0, 0, 10), Village(2, 9, 9, 10)]
drones = [Drone(0, 0, [])]  # Provide an empty list for trajet
config = Config(None, drones, obstacles, villages, 10, True)

start = (0, 0)
goal = (9, 9)

path = a_star(config, start, goal)
print("Path from start to goal:", path)