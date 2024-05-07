

#placement des drones dans les villages 
import random

def position(villages, drones):
    positions = set() 
    for i in range(drones):
        position = random.choice(villages) 
        while position in positions:  # Vérifier si la position est déjà occupée
            position = random.choice(villages)
        positions.add(position) 
    return list(positions)


def test_position():
    villages = [1, 32, 41, 56]
    nombre_de_drones = 3
    positions_des_drones = position(villages, nombre_de_drones)
    print(positions_des_drones)


def calculer_degat_maximal(positions_des_drones, temps_actuel, villages_visites):
    degat_maximal = 0
    
    for village, dernier_passage in villages_visites.items():
        temps_attente = temps_actuel - dernier_passage
        degat_maximal = max(degat_maximal, temps_attente)
    
    return degat_maximal

def calculer_degat_total(positions_des_drones, temps_actuel, villages_visites, fuites_eau):
    degat_total = 0
    for village, dernier_passage in villages_visites.items():
        temps_attente = temps_actuel - dernier_passage
        degat_total += fuites_eau[village] * temps_attente
    
    return degat_total

def test_fuite():
    positions_des_drones = [(3, 4), (5, 6), (7, 8)]
    temps_actuel = 10
    villages_visites = {1: 5, 2: 8, 3: 12}
    fuites_eau = {1: 10, 2: 5, 3: 8}  # Quantité d'eau perdue dans chaque village en raison de la fuite

    degat_total = calculer_degat_total(positions_des_drones, temps_actuel, villages_visites, fuites_eau)
    print("Dégât total (impact des fuites d'eau):", degat_total)


def test_degat():
    positions_des_drones = [(3, 4), (5, 6), (7, 8)]
    temps_actuel = 10
    villages_visites = {1: 5, 2: 8, 3: 12} #( 1 id de village et 5 le moment ou le dernier drone a visité ce village )
    degat_maximal = calculer_degat_maximal(positions_des_drones, temps_actuel, villages_visites)
    print("Dégât maximal:", degat_maximal)

