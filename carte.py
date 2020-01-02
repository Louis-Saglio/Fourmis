class Case:

    def __init__(self, value, owning_map, coordinates):
        self.value = value
        self.owning_map = owning_map
        self.coordinates = coordinates
        self.border = self.get_border_type()
        self.pawn = None
        self.data = {}

    def __str__(self):
        if self.pawn:
            return str(self.pawn.look)
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def get_border_type(self):
        l, h = self.coordinates
        return {
            "is_top": h == 0 or False,
            "is_left": l == 0 or False,
            "is_bottom": h == self.owning_map.height - 1 or False,
            "is_right": l == self.owning_map.width - 1 or False
        }

    def is_border_position(self):
        return len([None for value in self.border.values() if value]) != 0

    def get_case_by_vector(self, *coor):
        position = self.coordinates[0] + coor[0], self.coordinates[1] + coor[1]
        if position in self.owning_map:
            return self.owning_map[position]
        return None

    def get_connected(self):
        rep = set([self.get_case_by_vector(*vector) for vector in self.owning_map.directions.values()])
        if None in rep:
            rep.remove(None)
        return rep


class Map:

    def __init__(self, width, height, filling='M', border='B'):
        self.width = width
        self.height = height
        self.border_type = border
        self.filling_type = filling
        self.map = self.create_map()
        self.directions = {"up": (0, -1), "down": (0, 1), "right": (1, 0), "left": (-1, 0)}

    def __iter__(self):
        iterator = []
        for h in range(self.height):
            for l in range(self.width):
                iterator.append(self[l, h])
        return iter(iterator)

    def __getitem__(self, pos):
        l, h = pos
        return self.map[l][h]

    def __setitem__(self, key, value):
        index1, index2 = key
        self.map[index1][index2] = Case(value, self, key)

    def __str__(self):
        rep = ''
        for case in self:
            rep += str(case) + ' ' + ('\n' if case.border["is_right"] else '')
        return rep

    def __repr__(self):
        return str(self).replace('\n', '\\n ')

    def __contains__(self, item):
        if isinstance(item, tuple):
            return 0 <= item[0] < self.width and 0 <= item[1] < self.height
        elif isinstance(item, Case):
            return self[item.coordinates] is item
        elif isinstance(item, Pawn):
            return item.case in self
        else:
            raise NotImplementedError

    def create_map(self):
        return [[Case(self.filling_type, self, (l, h)) for h in range(self.height)] for l in range(self.width)]

    def create_border(self):
        for case in self:
            if case.is_border_position():
                    case.value = self.border_type


class Pawn:

    def __init__(self, owning_map: Map, case: Case, look):
        self.look = look
        self.owning_map = owning_map
        self._case = case
        self.case = case

    def __str__(self):
        return str(self.look)

    @property
    def case(self):
        return self._case

    @case.setter
    def case(self, new_case: Case):
        self._case.pawn = None
        self._case = self.owning_map[new_case.coordinates]
        self._case.pawn = self

    def move(self, direction):
        vector = self.owning_map.directions[direction]
        self.case = self._case.get_case_by_vector(*vector)


if __name__ == '__main__':
    from time import time
    x, y, a, b = 10, 6, 2, 3
    debut = time()
    test = Map(x, y)
    test.create_border()
    # test[a, b] = "P"
    pawn = Pawn(test, test[6, 3], "O")
    pawn.move("up")
    pawn.move("left")
    pawn.move("down")
    pawn.move("right")
    pawn.move("right")
    pawn.move("up")
    assert test[2, 2].get_case_by_vector(1, 1) is test[3, 3]
    assert test[0, 2] in test
    assert (0, 5) in test
    assert pawn in test
    # Si la séquence de pawn.move est modifié, ce test doit être déplacé
    assert pawn.case.coordinates == (7, 2)
    assert (2, 6) not in test
    assert (2, 10) not in test
    print(test)
    print("Tests executés en", round(time()-debut, 3), "seconde(s) avec succès.")
