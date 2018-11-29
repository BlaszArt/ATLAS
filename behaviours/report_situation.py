from spade.behaviour import CyclicBehaviour
import asyncio
import datetime


class ReportSituation(CyclicBehaviour):
    def __init__(self, agent):
        super(ReportSituation, self).__init__()
        self.agent = agent

    async def on_start(self):
        pass

    async def run(self):
        print()
        print(datetime.datetime.now())
        print('Lights: ' + str(self.agent.crossroad.lights))
        print('Cars: ' + str(self.agent.crossroad.cars))
        await asyncio.sleep(5)
