
class Cell:
    def __init__(self) -> None:
        self._resident = list()

class SpatialStructure:
    def __init__(self, limit_min, limit_max, nb_division) -> None:
        self._limit_min = limit_min
        self._limit_max = limit_max
        self._nb_division = nb_division
        self.cell= list()