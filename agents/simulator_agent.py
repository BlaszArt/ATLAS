from spade.agent import Agent
from simulation.sumo_api import SumoApi
from spade.behaviour import PeriodicBehaviour
import traci


class SimulationAgent(Agent):

    def __init__(self, jid, password):
        Agent.__init__(self, jid, password)
        traci.start(["sumo-gui", "-c", "simulation/configuration/simulation.sumo.cfg"], label="simulation")

    class RunSimulator(PeriodicBehaviour):
        async def on_start(self):
            self.sumo_api = SumoApi()

        async def run(self):
            self.sumo_api.simulation_step()
            print('{}{}'.format('simulation step: ', int(self.sumo_api.get_simulation_time())))

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")
        self.add_behaviour(self.RunSimulator(period=1))
