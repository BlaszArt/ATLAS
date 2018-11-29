from spade.behaviour import CyclicBehaviour
import asyncio


class ChangeLights(CyclicBehaviour):
    def __init__(self, agent):
        super(ChangeLights, self).__init__()
        self.agent = agent

    async def on_start(self):
        pass

    async def run(self):
        cars_on_road = {road:sum([self.agent.crossroad.cars[street] for street in streets]) for road, streets in self.agent.crossroad.topology.items()}
        max_busy_road = max(cars_on_road, key=cars_on_road.get)
        lights_to_change = self.agent.crossroad.topology[max_busy_road]
        for street in self.agent.crossroad.lights:
            self.agent.crossroad.lights[street] = 1 if street in lights_to_change else 0
        await asyncio.sleep(30)
