
def minimiser_degats(villages, drones, obstacles, fuites_eau):

    meilleure_tournée = None
    meilleur_temps = float('inf')
    degat_min = float('inf')
    positions_des_drones = [drone.get_position() for drone in drones]
    
    permutations = itertools.permutations(villages)
    
    for permutation in permutations:
        temps_total = 0
        tournées = [permutation[i:i+drones] for i in range(0, len(permutation), drones)]
        
        for tournée in tournées:
            temps_tournée = calculer_temps_de_parcours(tournée, distances)
            temps_total += temps_tournée
            villages_visites = [village in villages if village.get_derniere_visite() != 0]
            degat = calculer_degat_total(positions_des_drones, temps_total, villages_visites, fuites_eau)
        
        if temps_total < meilleur_temps and degat < degat_min:
            meilleure_tournée = tournées
            meilleur_temps = temps_total
    
    return meilleure_tournée, meilleur_temps

#comment obtenir les fuites deau ???? privilégier meilleur temps pour degat min ??? 