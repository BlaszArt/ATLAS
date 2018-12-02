from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio
import datetime


class SendReportForSubscribers(CyclicBehaviour):
    """
    Crossroad behaviour for sending report to subscribers
    """
    async def run(self):
        for agent in self.agent.presence.get_contacts():
            # send report
            msg = Message(to=str(agent))
            msg.set_metadata("performative", "inform")
            msg.body = self.agent.crossroad.get_status()
            try:
                await self.send(msg)
            except Exception:
                pass
        await asyncio.sleep(1)


class ReceiveReport(CyclicBehaviour):
    """
    Manager behaviour for receiving report
    """
    async def run(self):
        msg = await self.receive()
        if msg:
            self.agent.reports[msg.sender] = msg.body
        await asyncio.sleep(1)


class ReportSituation(PeriodicBehaviour):
    """
    Manager behaviour for raporting situation in system based on subscribed data
    """
    async def run(self):
        print()
        print(f" --------- [{datetime.datetime.now()}] ----------")

        for agent, report in self.agent.reports.items():
            print(f"[{agent}] {report}")
        print(" -------------------------------------------------")
        await asyncio.sleep(5)
