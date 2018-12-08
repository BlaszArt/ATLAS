from spade.behaviour import PeriodicBehaviour, CyclicBehaviour, OneShotBehaviour
from spade.message import Message
import asyncio
import datetime


class SendReportForSubscribers(PeriodicBehaviour):
    """
    Crossroad behaviour for sending report to subscribers
    """

    async def on_start(self):
        await asyncio.sleep(10)

    async def run(self):
        # send report
        
        for subscriber in self.agent.subscribers:
            msg = Message(to=str(subscriber))
            msg.set_metadata("performative", "inform")
            msg.body = self.agent.crossroad.get_status()
            try:
                await self.send(msg)
            except Exception:
                pass


class Subscribe(CyclicBehaviour):
    """
    Crossroad behaviour for handling subscribe request
    """
    async def run(self):
        msg = await self.receive()
        if msg and msg.sender not in self.agent.subscribers:
            self.agent.subscribers.append(msg.sender)
        await asyncio.sleep(1)

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
