import networkx as nx
import matplotlib.pyplot as plt

def read_world_file(n, file_name):
    G = nx.Graph()
    obstacles = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            entity = parts[0]
            data = parts[1].strip()
            if entity.isdigit():  # C'est un village
                coordinates = tuple(map(int, data.strip('()').split(',')))
                G.add_node(int(entity), pos=coordinates)
            elif entity == 'D':  # C'est un drone
                drone_pos = tuple(map(int, data.strip('()').split(',')))
                G.add_node('D', pos=drone_pos)  # Ajouter le drone comme un noeud peut être optionnel
            elif entity == 'X':  # C'est un obstacle
                corners = data.split(';')
                corner1 = tuple(map(int, corners[0].strip(' ()').split(',')))
                corner2 = tuple(map(int, corners[1].strip(' ()').split(',')))
                obstacles.append((corner1, corner2))
            elif entity == 'E':  # Chemin possible entre villages
                villages = data.strip('()').split(',')
                G.add_edge(int(villages[0]), int(villages[1]))

    return G, obstacles

# Utilisation de l'exemple
N = 30
graph, obstacles = read_world_file(N, 'file_test.txt')
print(graph)
print(obstacles)



def draw_graph(G):
    pos = nx.get_node_attributes(G, 'pos')  # Obtient les positions des noeuds stockées dans les attributs 'pos'
    # Dessine les nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', label='Villages et Drone')
    # Dessine les arêtes
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=2)
    # Dessine les étiquettes des nœuds
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    
    plt.title('Visualisation du Graphe des Villages et Drone')
    plt.xlabel('Position X')
    plt.ylabel('Position Y')
    plt.legend()
    plt.show()

# Supposons que vous avez déjà créé votre graphe 'graph' avec la fonction 'read_world_file'
graph, obstacles = read_world_file(N, 'file_test.txt')  # Assurez-vous d'avoir la bonne valeur de N et le bon chemin du fichier
draw_graph(graph)
