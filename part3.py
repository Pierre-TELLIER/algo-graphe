

#placement des drones dans les villages 
import random
import itertools
from classes import *
from projet_drone import *



def set_drone_position(config: Config):
    occupied_villages = set()
    for drone in config.drones:
        start_village = random.choice(config.villages)
        while start_village in occupied_villages:  
            start_village = random.choice(config.villages)
        occupied_villages.add(start_village)
        drone.add_to_trajet(config.graph, start_village) 


def test_position():
    config = read_world_file(30, "file_test.txt")
    set_drone_position(config)
    positions_occupe = []

    for drone in config.drones:
        assert len(drone.trajet) > 0
        assert drone.trajet[0] not in positions_occupe
        positions_occupe.append(drone.trajet[0])

    print("test position aléatoires => OK")

def calculer_degats_optimal(config):
    g = config.graph
    delays = {}
    for village1 in config.villages:
        for village2 in config.villages:
            if village1 != village2:
                delays[(village1.nodeID, village2.nodeID)] = shortest_path_length(g, village1.nodeID, village2.nodeID)

    damages = {}
    for village in config.villages:
        damages[village.nodeID] = {}
        for time in range(config.n):
            damages[village.nodeID][time] = 0

    for village in config.villages:
        for time in range(config.n):
            for prev_village in config.villages:
                if prev_village != village:
                    damages[village.nodeID][time] = max(damages[village.nodeID][time], time * delays[(prev_village.nodeID, village.nodeID)])

    optimal_path = []
    for time in range(config.n):
        min_damage = float('inf')
        best_village = None
        for village in config.villages:
            if damages[village.nodeID][time] < min_damage:
                min_damage = damages[village.nodeID][time]
                best_village = village
        optimal_path.append((best_village, time))

    return optimal_path

def test_trajet_optimal():
    config = read_world_file(30, "file_test.txt")
    set_drone_position(config)
    trajet_optimal = calculer_degats_optimal(config)
    print("test trajet optimal => OK")

#my methode to decide the road for each drone is to be random .
def generate_random_path(config):
    random_path = []
    for time in range(config.n):
        path_at_time = []
        for drone in config.drones:
            random_village = random.choice(config.villages)
            path_at_time.append((random_village, time))
        random_path.append(path_at_time)
    return random_path


def test_generate_random_path():
    config = read_world_file(30, "file_test.txt")
    random_path = generate_random_path(config)
    print("test generate random path => OK")



if __name__ == "__main__":
    test_position()
    test_trajet_optimal()
    test_generate_random_path()

