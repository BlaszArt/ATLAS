from enum import Enum


class TrafficLightColors(Enum):
    GREEN = "Green",
    RED = "Red",
    YELLOW = "Yellow"

    @staticmethod
    def get_light_color(color_sumo_representation):
        return SUMO_COLORS_ENCODED.get(color_sumo_representation)


SUMO_COLORS_ENCODED = {"GGgg": 1, "rrrr": 0,
                       "yyyy": 0}
