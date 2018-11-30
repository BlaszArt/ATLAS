from spade.behaviour import CyclicBehaviour
import asyncio

from models.directions import Directions


class GetCars(CyclicBehaviour):
    def __init__(self, agent, cars_speed):
        super(GetCars, self).__init__()
        self.agent = agent
        self.cars_speed = cars_speed

    async def on_start(self):
        pass

    async def run(self):
        for street in self.agent.crossroad.cars:
            if street not in self.agent.neighbours:
                self.agent.crossroad.cars[street] += self.cars_speed

            if self.agent.crossroad.lights[street] and self.agent.crossroad.cars[street] >= self.cars_speed:
                self.agent.crossroad.cars[street] -= self.cars_speed
                if Directions.get_opposite_dir_name(street) in self.agent.neighbours:
                    self.agent.neighbours[Directions.get_opposite_dir_name(street)].crossroad.cars[street] += self.cars_speed

        await asyncio.sleep(5)
