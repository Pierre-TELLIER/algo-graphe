import copy
import random

from classes import *
from projet_drone import read_world_file, draw_graph
import math
import matplotlib.pyplot as plt


def set_drone_path_1(c: Config):
    first_index = 0
    path_len = math.ceil(c.get_nb_village() / c.get_nb_drones())
    for drone in c.drones:
        for i in range(first_index, first_index + path_len):
            drone.add_to_trajet(c.graph, c.villages[i % c.get_nb_village()])

        first_index += path_len


def set_drone_path_2(c: Config, objs: list[Objet]):
    if len(objs) <= c.get_nb_drones():
        # If there are fewer objects than drone, each drone will be responsible for 1 object
        for i in range(len(objs)):
            c.drones[i].add_to_trajet(c.graph, objs[i].start)
            c.drones[i].add_to_trajet(c.graph, objs[i].end)

    else:
        set_drone_path_1(c)


def move_all_drones_cpy(c: Config, t: int):
    config = copy.deepcopy(c)
    for i in range(t):
        for drone in config.drones:
            drone.step()
    return config


def get_obj_time_left(c: Config, obj: Objet, temps_restant):
    """
    :param c:
    :param obj:
    :param temps_restant: config.get_max_delay()
    :return:
    """
    # print(f"temps_restant: {temps_restant}, obj: {obj.start.nodeID} => [{obj.cur.nodeID}] => {obj.end.nodeID}")
    if temps_restant <= 0:
        return temps_restant

    if obj.cur.nodeID == obj.end.nodeID:
        return temps_restant

    score = 0
    for t in range(temps_restant):
        for drone in c.drones:
            if drone.trajet[drone.cur_pos] == obj.cur and drone.isOnVillage:
                temps = drone.distanceToNextVillage
                new_cfg = move_all_drones_cpy(c, temps)
                new_obj = copy.deepcopy(obj)
                new_obj.cur = drone.trajet[(drone.cur_pos + 1) % len(drone.trajet)]
                # print(f"drone picked up the object. time: {temps}, obj: {obj.cur.nodeID} => {new_obj.cur.nodeID}")
                new_score = get_obj_time_left(new_cfg, new_obj, temps_restant - temps)
                score = max(score, new_score)

            drone.step()
        temps_restant -= 1
    return score


def get_score(c: Config, objs: list[Objet]):
    return sum([c.get_max_delay() - get_obj_time_left(c, obj, c.get_max_delay()) for obj in objs])


if __name__ == "__main__":
    gameConfig = read_world_file(30, "file_test.txt")

    objets = [Objet(gameConfig.villages[random.randint(0, 13)], gameConfig.villages[random.randint(0, 13)]) for i in range(20)]



    mode = 2
    match mode:
        case 1:
            set_drone_path_1(gameConfig)
        case 2:
            set_drone_path_2(gameConfig, objets)

    """
    for drone in gameConfig.drones:
        print(drone.delay)
    """

    draw_graph(gameConfig)

    """
    for obj in objets:
        print(f"\n\ndelay: [{gameConfig.get_max_delay() - get_obj_time_left(gameConfig, obj, gameConfig.get_max_delay())}], max delay: {gameConfig.get_max_delay()}\n\n")
    """
    # print(gameConfig.get_max_delay())
    x = range(19)
    y = [get_score(gameConfig, objets[0 : x]) / x for x in range(1, 20) ]
    print(y)
    print(get_score(gameConfig, objets))
    plt.plot(x, y)
    plt.title("average duration")
    plt.ylabel("delay")
    plt.xlabel('number of object')
    plt.show()