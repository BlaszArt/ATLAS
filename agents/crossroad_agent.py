from spade.agent import Agent
from spade.template import Template
from behaviours.environment import GetCars, ChangeLights
from behaviours.topology import UpdateTopology
from behaviours.reporting import SendReportToManager
from models import crossroad, messages_body_labels
from behaviours.crossroads_communication import CrossroadsMessanger
import config


class CrossroadAgent(Agent):
    def __init__(self, manager_jid, cars_speed, *args, **kwargs):
        super(CrossroadAgent, self).__init__(*args, **kwargs)
        self.manager_jid = manager_jid
        self.crossroad = crossroad.Crossroad()
        self.neighbours = {} #todo czy to jest potrzebne?
        self.neighbours_jid = {}
        self.cfp = {messages_body_labels.direction: None, # because of which direction we wanna change lights
                    messages_body_labels.to_change: None, # if we wanna last green longer (false) or change it quicker (true)
                    messages_body_labels.change_by: None} # how much we wanna change lights remaining duration
        self.cars_speed = cars_speed
        self.directions_max_cars = {'NS': None, 'WE': None} # directions and max cars on their streets

    def __str__(self):
        return "Agent: {}".format(self.jid)

    def get_actual_green_lights_direction(self):
        if self.crossroad.lights['N'] == 1:
            return 'NS'
        else:
            return 'EW'

    def start_crossroad(self, neighbours, auto_register=True):
        self.neighbours = neighbours
        super().start(auto_register)

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")

        # Update topology - waiting for request from manager
        template_msg = Template()
        template_msg.sender = self.manager_jid
        template_msg.set_metadata = ('performative', 'request')
        self.add_behaviour(UpdateTopology(period=config.UPDATE_TOPOLOGY_FREQ), template_msg)

        # Reporting to manager
        self.add_behaviour(SendReportToManager(period=5))

        # Get data from sensors
        self.add_behaviour(GetCars(period=config.GET_CARS_FREQ))

        # Control lights
        self.add_behaviour(ChangeLights(config.CHANGE_LIGHTS_FREQ))

        # Answering protocol
        self.add_behaviour(CrossroadsMessanger.NegotiatingProtocolParticipant())