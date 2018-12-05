from spade.behaviour import PeriodicBehaviour

from behaviours.crossroads_communication import CrossroadsMessanger
from models.directions import Directions


class ChangeLights(PeriodicBehaviour):
    # static variable to now when try to change lights state
    A_LOT_OF_CARS = 5

    def green_for_max_busy_road(self):
        self.agent.directions_max_cars = self.get_roads_with_max_cars()

        for cars in self.agent.directions_max_cars.values():
            if cars >= ChangeLights.A_LOT_OF_CARS:
                self.agent.add_behaviour(CrossroadsMessanger.NegotiatingProtocolInitiator())
                break

    #todo: powinna zwrocic zestaw: kierunek: najwieksza liczba samochodow, a zwraca te sama, niekiedy zrypana wartosc w obu kierunkach
    # np. dla samochodow na ulicach: N=5, S=3, E=1, W=10 powinno zwrocic: NS: 5, EW: 10
    def get_roads_with_max_cars(self):
        return {road: self.return_max_cars_on_road(data['streets']) for road, data in self.agent.crossroad.roads.items()}

    def return_max_cars_on_road(self, streets):
        max_cars = 0
        for street in streets:
            if self.agent.crossroad.cars[street] > max_cars:
                max_cars = self.agent.crossroad.cars[street]
        return max_cars

    async def run(self):
        if len(self.agent.crossroad.roads) > 0:
            self.green_for_max_busy_road()


class GetCars(PeriodicBehaviour):
    """
    Crossroad behaviour for getting data about cars on streets
    """

    async def run(self):
        for street in self.agent.crossroad.cars:
            self.simulator(street)

    def simulator(self, street):
        if street not in self.agent.neighbours:
            self.agent.crossroad.cars[street] += self.agent.cars_speed

        if self.agent.crossroad.lights[street] and self.agent.crossroad.cars[street] >= self.agent.cars_speed:
            self.agent.crossroad.cars[street] -= self.agent.cars_speed
            if Directions.get_opposite_dir_name(street) in self.agent.neighbours:
                self.agent.neighbours[Directions.get_opposite_dir_name(street)].crossroad.cars[
                    street] += self.agent.cars_speed
