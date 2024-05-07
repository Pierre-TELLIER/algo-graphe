class Config:
    def __init__(self, graph, drones, obstacle, villages: list, n):
        self.graph = graph
        self.drones = drones
        self.obstacle = obstacle
        self.villages = villages
        self.n = n


class Village:
    def __init__(self, village_id, x, y):
        self.village_id = village_id
        self.x = x
        self.y = y


class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
