from spade.agent import Agent
from spade.template import Template
from behaviours import change_lights, get_cars, report_situation, topology
from models import crossroad
from models.directions import Directions


class CrossroadAgent(Agent):
    def __init__(self, manager_jid, *args, **kwargs):
        super(CrossroadAgent, self).__init__(*args, **kwargs)
        self.manager_jid = manager_jid
        self.crossroad = crossroad.Crossroad()
        self.neighbours = {}
        self.cars_speed = 0

    def init_crossroad(self, neighbours):
        self.crossroad.topology['NS'] = []
        self.crossroad.topology['WE'] = []
        self.neighbours = neighbours
        for i in range(0, 4):
            street = Directions(i).name
            if i % 2:
                self.crossroad.topology['NS'].append(street)
            else:
                self.crossroad.topology['WE'].append(street)
            self.crossroad.cars[street] = 0
            self.crossroad.lights[street] = 1 if i % 2 else 0

    def __str__(self):
        return "Agent: {}".format(self.jid)

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")
        self.presence.set_unavailable()
        self.presence.set_presence(status='No topology')

        # Update topology - waiting for request from manager
        template_msg = Template()
        template_msg.sender = self.manager_jid
        template_msg.set_metadata = {'performative': 'request'}
        self.add_behaviour(topology.UpdateTopology(period=1), template_msg)

        #self.add_behaviour(get_cars.GetCars(self, self.cars_speed))
        #self.add_behaviour(report_situation.ReportSituation([self]))
        #self.add_behaviour(change_lights.ChangeLights(self))
