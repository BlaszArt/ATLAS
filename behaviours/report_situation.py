from spade.behaviour import CyclicBehaviour
import asyncio
import datetime


class ReportSituation(CyclicBehaviour):
    def __init__(self, agents):
        super(ReportSituation, self).__init__()
        self.agents = agents

    async def on_start(self):
        pass

    async def run(self):
        if len(self.agents) > 1:
            print()
            print(' --------- summary ----------')
        else:
            print()

        for agent in self.agents:
            print()
            print(datetime.datetime.now())
            print(agent.jid)
            print('Lights: ' + str(agent.crossroad.lights))
            print('Cars: ' + str(agent.crossroad.cars))

        if len(self.agents) > 1:
            print()
            print(' --------- end of summary ----------')
            print()
        await asyncio.sleep(5)
