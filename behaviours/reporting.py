from spade.behaviour import CyclicBehaviour
import asyncio
import datetime


class ReportSituation(CyclicBehaviour):
    """
    Manager behaviour for raporting situation in system based on subscribed data
    """
    async def run(self):
        print()
        print(f" --------- [{datetime.datetime.now()}] ----------")

        for agent, data in self.agent.presence.get_contacts().items():
            print(f"[{agent}] {data}")

        await asyncio.sleep(5)
