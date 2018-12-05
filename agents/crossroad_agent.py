from spade.agent import Agent
from spade.template import Template
from behaviours.environment import GetCars, ChangeLights
from behaviours.topology import UpdateTopology
from behaviours.reporting import SendReportForSubscribers, Subscribe
from models import crossroad


class CrossroadAgent(Agent):
    def __init__(self, manager_jid, cars_speed, *args, **kwargs):
        super(CrossroadAgent, self).__init__(*args, **kwargs)
        self.manager_jid = manager_jid
        self.crossroad = crossroad.Crossroad()
        self.subscribers =[]
        self.neighbours = {}
        self.neighbours_jid = {}
        self.cars_speed = cars_speed

    def __str__(self):
        return "Agent: {}".format(self.jid)

    def start(self, neighbours, auto_register=True):
        self.neighbours = neighbours
        super().start()

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")

        # Update topology - waiting for request from manager
        template_msg = Template()
        template_msg.sender = self.manager_jid
        template_msg.metadata = {'performative': 'request'}
        self.add_behaviour(UpdateTopology(period=1), template_msg)

        # Handler for subscribe request
        template_msg = Template()
        template_msg.metadata = {'performative': 'subscribe'}
        self.add_behaviour(Subscribe(), template_msg)

        # Reporting to manager
        self.add_behaviour(SendReportForSubscribers(period=1))

        # Get data from sensors
        self.add_behaviour(GetCars())

        # Control lights
        self.add_behaviour(ChangeLights())
