from enum import Enum


class Directions(Enum):
    vertical = 'vertical'
    horizontal = 'horizontal'

    @classmethod
    def get_opposite_dir_name(cls, direction_name):
        opposites = {
            cls.vertical.name: cls.horizontal.name,
            cls.horizontal.name: cls.vertical.name
        }
        return opposites[direction_name]
