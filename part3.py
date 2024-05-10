

#placement des drones dans les villages 
import random
import itertools
from classes import *
from projet_drone import *


def set_drone_position(config: Config):
    occupied_villages = set()
    for drone in config.drones:
        start_village = random.choice(config.villages)
        while start_village in occupied_villages:  # Vérifier si la position est déjà occupée
            start_village = random.choice(config.villages)
        occupied_villages.add(start_village)
        drone.add_to_trajet(start_village.village_id)


def test_position():
    config = read_world_file(30, "file_test.txt")
    set_drone_position(config)
    positions_occupe = []

    for drone in config.drones:
        assert len(drone.trajet) > 0
        assert drone.trajet[0] not in positions_occupe
        positions_occupe.append(drone.trajet[0])

    print("test position aléatoires => OK")




def calculer_degat_maximal(positions_des_drones, temps_actuel, villages_visites):
    degat_maximal = 0
    
    for village, dernier_passage in villages_visites.items():
        temps_attente = temps_actuel - dernier_passage
        degat_maximal = max(degat_maximal, temps_attente)
    
    return degat_maximal

def calculer_degat_total(positions_des_drones, temps_actuel, villages_visites, fuites_eau):
    degat_total = 0
    for village, dernier_passage in villages_visites.items():
        degat_total += fuites_eau[village] 
    
    return degat_total

#def trajet_optimal(position_inital, destination_final):
    

def test_fuite():
    positions_des_drones = [(3, 4), (5, 6), (7, 8)]
    temps_actuel = 10
    villages_visites = {1: 5, 2: 8, 3: 12}
    fuites_eau = {1: 10, 2: 5, 3: 8}  # Quantité d'eau perdue dans chaque village en raison de la fuite

    degat_total = calculer_degat_total(positions_des_drones, temps_actuel, villages_visites, fuites_eau)
    print("Dégât total (impact des fuites d'eau):", degat_total)

#test_fuite()


def test_degat():
    positions_des_drones = [(3, 4), (5, 6), (7, 8)]
    temps_actuel = 10
    villages_visites = {1: 5, 2: 8, 3: 12} #( 1 id de village et 5 le moment ou le dernier drone a visité ce village )
    degat_maximal = calculer_degat_maximal(positions_des_drones, temps_actuel, villages_visites)
    print("Dégât maximal:", degat_maximal)

#test_degat()

def calculer_temps_de_parcours(tournée, distances):
    temps = 0
    for i in range(len(tournée) - 1):
        village_actuel = tournée[i]
        village_suivant = tournée[i + 1]
        temps += distances[(village_actuel, village_suivant)]  
    return temps


#fonction pour le trajet optimal d'une drone


def trouver_trajet_optimal(villages, drones, distances):
    meilleure_tournée = None
    meilleur_temps = float('inf')
    
    permutations = itertools.permutations(villages)
    
    for permutation in permutations:
        temps_total = 0
        tournées = [permutation[i:i+drones] for i in range(0, len(permutation), drones)]
        
        for tournée in tournées:
            temps_tournée = calculer_temps_de_parcours(tournée, distances)
            temps_total += temps_tournée
        
        if temps_total < meilleur_temps:
            meilleure_tournée = tournées
            meilleur_temps = temps_total
    
    return meilleure_tournée, meilleur_temps

def test_trajetOptimal() :
    villages = [1, 2, 3, 4]  
    drones = 2  
    distances = {
        (1, 2): 10, (1, 3): 15, (1, 4): 20,
        (2, 1): 10, (2, 3): 35, (2, 4): 25,
        (3, 1): 15, (3, 2): 35, (3, 4): 30,
        (4, 1): 20, (4, 2): 25, (4, 3): 30
}  

    meilleure_tournée, meilleur_temps = trouver_trajet_optimal(villages, drones, distances)

    print("Meilleure tournée trouvée :", meilleure_tournée)
    #la meilleure tournée trouvée est [(1, 2), (3, 4)], ce qui signifie que deux drones sont utilisés. Le premier drone parcourt les villages 1 et 2 dans cet ordre, tandis que le deuxième drone parcourt les villages 3 et 4.
    print("Meilleur temps de parcours :", meilleur_temps)

#test_trajetOptimal()

#l'idée c'est de choisir les villages d'une facon aleatoire 
def generer_solution_initiale(villages, drones):
    # Générer une solution initiale aléatoire
    solution = []
    villages_copies = villages.copy()
    random.shuffle(villages_copies)
    for i in range(drones):
        solution.append(villages_copies[i::drones])
    return solution


def test_tr():
    villages = [1, 2, 3, 4]
    drones = 2
    meilleure_solution = generer_solution_initiale(villages, drones)
    print("Solution initiale aléatoire :", meilleure_solution)

# test_tr()

if __name__ == "__main__":
    test_position()

