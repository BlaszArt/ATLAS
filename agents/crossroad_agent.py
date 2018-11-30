from spade.agent import Agent
from behaviours import change_lights, get_cars, report_situation
from models import crossroad
from models.directions import Directions


class CrossroadAgent(Agent):
    def __init__(self, *args, **kwargs):
        super(CrossroadAgent, self).__init__(*args, **kwargs)
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

    def start(self, neighbours, cars_speed, auto_register=True):
        self.cars_speed = cars_speed
        self.init_crossroad(neighbours)
        super().start(auto_register)
        print("Hello World! I'm agent {}".format(str(self.jid)))

    def __str__(self):
        return "Agent: {}".format(self.jid)

    def setup(self):
        self.add_behaviour(get_cars.GetCars(self, self.cars_speed))
        self.add_behaviour(report_situation.ReportSituation([self]))
        self.add_behaviour(change_lights.ChangeLights(self))
