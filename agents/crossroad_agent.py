from spade.agent import Agent
from behaviours import change_lights, get_cars, report_situation
from models import crossroad


class CrossroadAgent(Agent):
    def __init__(self, *args, **kwargs):
        super(CrossroadAgent, self).__init__(*args, **kwargs)
        self.crossroad = crossroad.Crossroad()

    def init_crossroad(self):
        for i in range(0,4):
            street = 'street' + str(i)
            self.crossroad.cars[street] = 0
            self.crossroad.lights[street] = 1 if i % 2 else 0

        self.crossroad.topology['road0'] = ['street0', 'street2']
        self.crossroad.topology['road1'] = ['street1', 'street3']

    def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        self.init_crossroad()
        self.add_behaviour(get_cars.GetCars(self))
        self.add_behaviour(report_situation.ReportSituation(self))
        self.add_behaviour(change_lights.ChangeLights(self))
