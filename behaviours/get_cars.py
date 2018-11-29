from spade.behaviour import CyclicBehaviour
import asyncio


class GetCars(CyclicBehaviour):
    def __init__(self, agent):
        super(GetCars, self).__init__()
        self.agent = agent

    async def on_start(self):
        pass

    async def run(self):
        for street in self.agent.crossroad.cars:
            if self.agent.crossroad.lights[street] and self.agent.crossroad.cars[street] > 0:
                self.agent.crossroad.cars[street] -= 1
            else:
                self.agent.crossroad.cars[street] += 1
        await asyncio.sleep(5)
