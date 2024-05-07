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
                villages.append(Village(str( int(entity) + n*n), coordinates[0], coordinates[1]))
                G.add_node(int(entity) + n*n, pos=coordinates, cat="village")
            elif entity == 'D':  # C'est un drone
                drone_pos = tuple(map(int, data.strip('()').split(',')))
                drones.append(Drone(drone_pos[0], drone_pos[1]))
            elif entity == 'X':  # C'est un obstacle
                corners = data.split(';')
                corner1 = tuple(map(int, corners[0].strip(' ()').split(',')))
                corner2 = tuple(map(int, corners[1].strip(' ()').split(',')))
                obstacles.append(Obstacle(corner1[0], corner1[1], corner2[0], corner2[1]))
            elif entity == 'E':  # Chemin possible entre villages
                euclidian_path = False
                villages = data.strip('()').split(',')
                G.add_edge(int(villages[0]), int(villages[1]))

    if euclidian_path:
        for i in range(n):
            for j in range(n):
                cur = i + n*j
                G.add_node(cur, pos=(i, j), cat="path")
                if (i>0):
                    G.add_edge(cur-1, cur)
                if (j>0):
                    G.add_edge(cur-n, cur)

    return Config(G, drones, obstacles, villages, n)

# Utilisation de l'exemple
N = 30
gameConfig = read_world_file(N, "file_test.txt")



# output:
# {'John': 7.8, 'Mary': 9.0, Michael': 9.5}
def draw_graph(config):
    pos = nx.get_node_attributes(config.graph, 'pos')  # Obtient les positions des noeuds stockées dans les attributs 'pos'

    village_nodes = [ int(x.village_id) for x in config.villages]
    # Dessine les villages
    nx.draw_networkx_nodes(config.graph, pos, node_size=700, node_color='skyblue', label='Villages', nodelist=village_nodes)
    nx.draw_networkx_nodes(config.graph, pos, node_size=10, node_color='black', label='path', nodelist=[x for x in range(config.n ** 2)])
    # Dessine les arêtes
    nx.draw_networkx_edges(config.graph, pos, alpha=0.5, width=2)
    # Dessine les étiquettes des nœuds
    #nx.draw_networkx_labels(config.graph, pos, font_size=12, font_family='sans-serif')
    
    plt.title('Visualisation du Graphe des Villages et Drone')
    plt.xlabel('Position X')
    plt.ylabel('Position Y')
    plt.legend()
    plt.show()

# Supposons que vous avez déjà créé votre graphe 'graph' avec la fonction 'read_world_file'
draw_graph(gameConfig)
