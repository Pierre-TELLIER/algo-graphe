import networkx as nx
import matplotlib.pyplot as plt

from classes import *


def read_world_file(n, file_name):
    G = nx.Graph()
    obstacles = []
    villages = []
    drones = []
    euclidian_path = True
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            entity = parts[0]
            data = parts[1].strip()

            if entity.isdigit():  # C'est un village
                coordinates = tuple(map(int, data.strip('()').split(',')))
                villages.append(Village(entity, coordinates[0], coordinates[1], n))
                G.add_node(coordinates[0] + n * coordinates[1], pos=coordinates, cat="village", label=entity)
            elif entity == 'D':  # C'est un drone
                drone_pos = tuple(map(int, data.strip('()').split(',')))
                drones.append(Drone(drone_pos[0], drone_pos[1], []))
            elif entity == 'X':  # C'est un obstacle
                corners = data.split(';')
                corner1 = tuple(map(int, corners[0].strip(' ()').split(',')))
                corner2 = tuple(map(int, corners[1].strip(' ()').split(',')))
                obstacles.append(Obstacle(corner1[0], corner1[1], corner2[0], corner2[1]))
            elif entity == 'E':  # Chemin possible entre villages
                euclidian_path = False
                v = data.strip('()').split(',')
                for tmp_v in villages:
                    if tmp_v.village_id == v[0]:
                        v1 = tmp_v
                    if tmp_v.village_id == v[1]:
                        v2 = tmp_v
                G.add_edge(v1.nodeID, v2.nodeID)

    tmp_conf = Config(G, drones, obstacles, villages, n, euclidian_path)

    if euclidian_path:
        blocked = tmp_conf.get_blocked_nodes()
        for i in range(n):
            for j in range(n):
                cur = i + n * j
                try:
                    G.nodes[cur]
                except KeyError:
                    G.add_node(cur, pos=(i, j), cat="path")
                if cur in blocked:
                    continue
                if i > 0 and cur - 1 not in blocked:
                    G.add_edge(cur - 1, cur, weight=1)
                if j > 0 and cur - n not in blocked:
                    G.add_edge(cur - n, cur, weight=1)

    return Config(G, drones, obstacles, villages, n, euclidian_path)


# Utilisation de l'exemple



def draw_graph(config):
    pos = nx.get_node_attributes(config.graph, 'pos')
    label = nx.get_node_attributes(config.graph, 'label')
    # Obtient les positions des noeuds stockées dans les attributs 'pos'
    if config.full:
        village_nodes = [int(x.x + config.n * x.y) for x in config.villages]
        blocked_nods = config.get_blocked_nodes
        # Dessine les villages
        nx.draw_networkx_nodes(config.graph, pos, node_size=700, node_color='skyblue', label='Villages',
                               nodelist=village_nodes)
        nx.draw_networkx_nodes(config.graph, pos, node_size=10, node_color='black', label='path',
                               nodelist=[x for x in range(config.n ** 2) if
                                         x not in village_nodes and x not in blocked_nods()])

        nx.draw_networkx_nodes(config.graph, pos, node_size=10, node_color='red', label='obstacle',
                               nodelist=blocked_nods())
        nx.draw_networkx_labels(config.graph, pos, label)
    else:
        nx.draw_networkx_nodes(config.graph, pos, node_size=700, node_color='skyblue',
                               nodelist=[v.nodeID for v in config.villages], label="villages")
        nx.draw_networkx_labels(config.graph, pos, label)
    # Dessine les arêtes

    drone_path = []
    colors = ["blue", "red", "green", "yellow", "purple", "orange"]
    for i in range(len(config.drones)):
        drone_path_tmp = []
        array = []
        for j in range(len(config.drones[i].trajet)):
            array += shortest_path(config.graph, config.drones[i].trajet[j].nodeID, config.drones[i].trajet[(j+1) % len(config.drones[i].trajet)].nodeID)

        drone_path_tmp = [(array[i], array[i+1 % len(array) ])for i in range(len(array) - 1)]
        drone_path += drone_path_tmp
        nx.draw_networkx_edges(config.graph, pos, alpha=1, width=2, edgelist=drone_path_tmp, edge_color=colors[i%6])
    nx.draw_networkx_edges(config.graph, pos, alpha=0.5, width=1, nodelist=[x for x in config.graph.edges() if x not in drone_path])
    # Dessine les étiquettes des nœuds
    # nx.draw_networkx_labels(config.graph, pos, font_size=12, font_family='sans-serif')

    plt.title('Visualisation du Graphe des Villages et Drone')
    plt.xlabel('Position X')
    plt.ylabel('Position Y')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    N = 30
    gameConfig = read_world_file(N, "file_test.txt")
    draw_graph(gameConfig)
