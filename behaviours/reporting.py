from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio
import datetime


class SendReportToManager(PeriodicBehaviour):
    """
    Crossroad behaviour for sending report to subscribers
    """
    async def on_start(self):
        await asyncio.sleep(10)

    async def run(self):
        # send report

        msg = Message(to=self.agent.manager_jid)
        msg.set_metadata("performative", "inform")
        msg.body = self.agent.crossroad.get_status()
        try:
            await self.send(msg)
        except Exception:
            pass


class ReceiveReport(PeriodicBehaviour):
    """
    Manager behaviour for receiving report
    """

    async def run(self):
        msg = await self.receive()
        if msg:
            self.agent.reports[msg.sender] = msg.body


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
