from networkx import *

class Config:
    def __init__(self, graph, drones, obstacle, villages: list, n, full: bool):
        self.graph = graph
        self.drones = drones
        self.obstacle = obstacle
        self.villages = villages
        self.n = n
        self.full = full

    def get_blocked_nodes(self):
        r = []
        for o in self.obstacle:
            for x in range(o.x1, o.x2):
                for y in range(o.y1, o.y2):
                    r.append(x + self.n*y)
        return r


class Village:
    def __init__(self, village_id, x, y, n):
        self.village_id = village_id
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.nodeID = self.x + n * self.y
        self.derniere_visite = 0


    def set_derniere_visite(self, x):
        self.derniere_visite = x

    def get_derniere_visite(self):
        return self.derniere_visite


class Obstacle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Drone:
    """
    the current position is the last reached village, or the village the drone is currently on.
    delay is a list of times between each drone stop.
    delay[i] is the number of seconds between the village i-1 and the village i
    """
    def __init__(self, x, y, trajet):
        self.x = x
        self.y = y
        self.trajet = trajet
        self.cur_pos = 0
        self.isOnVillage = True
        self.delay = []
        self.distanceToNextVillage = 0

    def get_position(self):
        return self.trajet[self.cur_pos] if self.distanceToNextVillage == 0 else -1

    def step(self):
        """
        make a step and returns the new position.
        :return:
        """
        self.isOnVillage = False
        if self.distanceToNextVillage > 0:
            self.distanceToNextVillage -= 1
        if self.distanceToNextVillage == 0:
            self.cur_pos += 1
            self.distanceToNextVillage = self.delay[self.cur_pos]
            self.cur_pos %= len(self.trajet)
            self.isOnVillage = True
        return self.trajet[self.cur_pos]

    def add_to_trajet(self, g, v: Village):
        self.delay[len(self.delay)-1] = shortest_path_length(g, self.trajet[0].nodeID, v.nodeID)
        self.trajet.append(v)
        self.delay.append(shortest_path_length(g, self.trajet[-1].nodeID, v.nodeID))
