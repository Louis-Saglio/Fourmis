from random import randint, choice


class Ville:
    def __init__(self):
        self.posistion = randint(0, 100), randint(0, 100)
        self.voisines = []


def create_map(nbr):
    villes = []
    for __ in range(nbr):
        villes.append(Ville())
    for ville in villes:
        ville.voisines.append(choice(villes))

