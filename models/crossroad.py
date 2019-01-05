import json
import datetime


class Crossroad:
    def __init__(self):
        self.cars = {}
        self.lights = {}
        self.roads = {}

    def get_status(self):
        status = {"timestamp": str(datetime.datetime.now()), "cars": self.cars, "lights": self.lights}
        return json.dumps(status)

    def get_roads_with_max_cars(self):
        return {road: self.return_max_cars_on_road(data['streets']) for road, data in self.roads.items()}

    def return_max_cars(self):
        return max(self.cars.values())

    def return_max_cars_on_road(self, streets):
        max_cars = 0
        for street in streets:
            if self.cars[street] > max_cars:
                max_cars = self.cars[street]
        return max_cars

    def got_i_lights(self):
            return bool(self.lights)

    def get_actual_green_lights_direction(self):
        for direction in self.lights:
            for lane, light in self.lights[direction].items():
                if light == 1:
                    return direction
