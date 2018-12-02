from spade.agent import Agent
from spade.template import Template
from behaviours.reporting import ReportSituation, ReceiveReport
from behaviours.topology import ManagingTopology


class ManagerAgent(Agent):
    def __init__(self, jid, password, topology, verify_security=False, use_container=True, loop=None):
        super().__init__(jid, password, verify_security, use_container, loop)
        self.topology_src = topology
        self.reports = {}
        self._cached_stamp = 0

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")
        # FSM managing topology behaviour
        self.add_behaviour(ManagingTopology())

        # Reporting behaviours
        template_msg = Template()
        template_msg.set_metadata = ('performative', 'inform')
        self.add_behaviour(ReceiveReport(period=1), template=template_msg)
        self.add_behaviour(ReportSituation(period=5))
