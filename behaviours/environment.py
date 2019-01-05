from spade.behaviour import PeriodicBehaviour

from behaviours.crossroads_communication import CrossroadsMessanger


class ChangeLights(PeriodicBehaviour):
    # static variable to now when try to change lights state
    A_LOT_OF_CARS = 5

    def how_busy_is_road(self, streets):
        return sum([self.agent.cars[street] for street in streets])

    def road_occupancy(self):
        return {road: self.how_busy_is_road(data['streets']) for road, data in self.agent.roads.items()}

    def green_for_max_busy_road(self):
        self.agent.directions_max_cars = self.get_roads_with_max_cars()

        for cars in self.agent.directions_max_cars.values():
            if cars >= ChangeLights.A_LOT_OF_CARS:
                self.agent.add_behaviour(CrossroadsMessanger.NegotiatingProtocolInitiator())
                break

        # to co bylo wczesniej, na potrzeby symulacji
        road_occupancy = self.road_occupancy()
        max_busy_road = max(road_occupancy, key=road_occupancy.get)

        for road in self.agent.lights:
            if road == max_busy_road:
                self.agent.lights[road] = 1
            self.agent.lights[road] = 0

            # lights_to_change = self.agent.roads[max_busy_road]['streets']
            # for street in self.agent.lights:
            #    self.agent.lights[street] = 1 if street in lights_to_change else 0

    # todo: powinna zwrocic zestaw: kierunek: najwieksza liczba samochodow, a zwraca te sama, niekiedy zrypana wartosc w obu kierunkach
    # np. dla samochodow na ulicach: N=5, S=3, E=1, W=10 powinno zwrocic: NS: 5, EW: 10
    def get_roads_with_max_cars(self):
        return {road: self.return_max_cars_on_road(data['streets']) for road, data in self.agent.roads.items()}

    def return_max_cars_on_road(self, streets):
        max_cars = 0
        for street in streets:
            if self.agent.cars[street] > max_cars:
                max_cars = self.agent.cars[street]
        return max_cars

    async def run(self):
        if len(self.agent.roads) > 0:
            self.green_for_max_busy_road()


class GetCars(PeriodicBehaviour):
    """
    Crossroad behaviour for getting data about cars on streets
    """

    async def run(self):

        for road, streets in self.agent.roads.items():
            for street in streets['streets']:
                self.agent.cars[street] = self.agent.sumo_api.get_cars_on_lane(street)
                # print(street + ':' + str(self.agent.cars[street]))
                # self.simulator(road, streets['streets'])

    def simulator(self, road, streets):
        for street in streets:
            if street not in self.agent.neighbours:
                self.agent.cars[street] += self.agent.cars_speed

            if self.agent.lights[road] and self.agent.cars[street] >= self.agent.cars_speed:
                self.agent.cars[street] -= self.agent.cars_speed
                # if Directions.get_opposite_dir_name(road) in self.agent.neighbours:
                #     self.agent.neighbours[Directions.get_opposite_dir_name(road)].cars[
                #         street] += self.agent.cars_speed


class GetLightsStatus(PeriodicBehaviour):
    """
    Crossroad behaviour for getting data about lights on streets
    """

    async def run(self):
        for road, lights in self.agent.lights.items():
            for lane in lights:
                self.agent.lights[road][lane] = self.agent.sumo_api.get_light_on_lane(lane)
                #print('lane {} - light : {}'.format(lane, self.agent.lights[road][lane]))
        # just for test change_light_duration method
        self.agent.sumo_api.change_light_duration(str(self.agent.jid), -1)
