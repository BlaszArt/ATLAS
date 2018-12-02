import json


class Crossroad:
    def __init__(self):
        self.cars = {}
        self.lights = {}
        self.roads = {}

    def get_status(self):
        status = {"cars": self.cars, "lights": self.lights}
        return json.dumps(status)

