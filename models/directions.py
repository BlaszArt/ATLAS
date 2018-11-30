from enum import Enum


class Directions(Enum):
    N = 0
    E = 1
    S = 2
    W = 3

    @classmethod
    def get_opposite_dir_name(cls, direction_name):
        opposites = {
            cls.N.name: cls.S.name,
            cls.S.name: cls.N.name,
            cls.W.name: cls.E.name,
            cls.E.name: cls.W.name,
        }
        return opposites[direction_name]

