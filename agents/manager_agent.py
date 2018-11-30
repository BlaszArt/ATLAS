from spade.agent import Agent

from behaviours import report_situation


class ManagerAgent(Agent):
    def __init__(self, jid, password, agents, verify_security=False, use_container=True, loop=None):
        super().__init__(jid, password, verify_security, use_container, loop)
        self.agents = agents;

    def setup(self):
        self.add_behaviour(report_situation.ReportSituation(self.agents))
