from spade.behaviour import CyclicBehaviour
from models.directions import Directions
import asyncio


class GetCars(CyclicBehaviour):
    """
    Crossroad behaviour for getting data about cars on streets
    """
    async def run(self):
        for street in self.agent.crossroad.cars:
            self.simulator(street)
        await asyncio.sleep(5)

    def simulator(self, street):
        if street not in self.agent.neighbours:
            self.agent.crossroad.cars[street] += self.cars_speed

        if self.agent.crossroad.lights[street] and self.agent.crossroad.cars[street] >= self.cars_speed:
            self.agent.crossroad.cars[street] -= self.cars_speed
            if Directions.get_opposite_dir_name(street) in self.agent.neighbours:
                self.agent.neighbours[Directions.get_opposite_dir_name(street)].crossroad.cars[street] += self.cars_speed
