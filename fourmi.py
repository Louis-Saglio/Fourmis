from math import log
from pprint import pprint
from random import choice

from os import system

from carte import *


def get_pheromone_value(nbr):
    return log(nbr)


class Terrain(Map):

    def __init__(self, width, height, filling='M', border='B'):
        super().__init__(width, height, filling, border)
        for case in self:
            case.data["pheromone"] = 1

    def evapore_pheromone(self):
        for case in self:
            if case.data["pheromone"] > 1:
                case.data["pheromone"] -= 0.01


class Fourmiliaire(list):

    def __init__(self, case: Case):
        super().__init__()
        self.case = case

    def __call__(self, *args, **kwargs):
        for fourmi in self:
            fourmi()
            self.case.owning_map.evapore_pheromone()

    def auto_fill(self, nbr):
        for _ in range(nbr):
            Fourmi(self, "H")

    def give_objectif(self, obj: Case):
        for fourmi in self:
            fourmi.objectifs.append(obj)


# noinspection PyShadowingNames
class Fourmi(Pawn):

    def __init__(self, fourmiliaire: Fourmiliaire, look):
        super().__init__(fourmiliaire.case.owning_map, fourmiliaire.case, look)
        fourmiliaire.append(self)
        self.history = [fourmiliaire.case]
        self.ordre = "Find"
        self.objectifs = []

    def __call__(self, *args, **kwargs):
        if self.ordre == "Find":
            direction = self.advance()
        elif self.ordre == "Back":
            direction = self.go_back()
        else:
            raise NotImplementedError
        self.move(direction)

    def move(self, direction):
        if isinstance(direction, Case):
            self.case = direction
            self.history.append(direction)
        elif direction is None:
            pass
        else:
            raise NotImplementedError
        self.manage_orders()
        self.analyse_case()

    def manage_orders(self):
        if self.ordre == "Find":
            self.history.append(self.case)
        elif self.ordre == "Back":
            self.case.data["pheromone"] += 1
        else:
            raise NotImplementedError

    def analyse_case(self):
        if self.case in self.objectifs:
            self.ordre = "Back"
            self.history.pop(-1)

    def advance(self):
        rep = []
        for case_voisine in self.case.get_connected():
            val = (log(case_voisine.data["pheromone"] + 1)) * 100
            if not case_voisine.pawn and case_voisine is not self.history[-1]:
                for _ in range(int(val)):
                    rep.append(case_voisine)
        if rep:
            return choice(rep)
        return None

    def go_back(self):
        return self.history.pop(-1)


if __name__ == '__main__':
    terrain = Terrain(16, 10, filling=' ')
    terrain.create_border()
    fourmiliaire = Fourmiliaire(terrain[0, 0])
    fourmiliaire.auto_fill(150)
    fourmiliaire.give_objectif(terrain[15, 3])

    nbr = 1000
    pct = 0
    char = choice("#|>_-}*")
    for i in range(nbr):
        if i % round(nbr / 100) == 0:
            pct += 1
            system("cls")
            print((char * pct).ljust(101), pct, "%")
        fourmiliaire()
    maxi = max(list(terrain), key=lambda c: c.data["pheromone"])
    maxi.value = "M"
    pprint(maxi.__dict__)
    pprint(maxi.pawn.__dict__)
    # print([case.data["pheromone"] for case in list(terrain)])
    for case in terrain:
        if case.data["pheromone"] > 1:
            case.value = "O"
    # print([id(case) for case in fourmiliaire[0].history])
    print(terrain)
    
