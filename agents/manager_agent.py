from spade.agent import Agent

from behaviours import report_situation
from behaviours.topology import ManagingTopology


class ManagerAgent(Agent):
    def __init__(self, jid, password, topology, verify_security=False, use_container=True, loop=None):
        super().__init__(jid, password, verify_security, use_container, loop)
        self.topology_src = topology
        self._cached_stamp = 0

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")
        # FSM managing topology behaviour
        self.add_behaviour(ManagingTopology())

        # Reporting behaviour
        #self.add_behaviour(report_situation.ReportSituation())
