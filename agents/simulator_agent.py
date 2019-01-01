from spade.agent import Agent
from simulation.sumo_api import SumoApi
from spade.behaviour import PeriodicBehaviour
import traci


class SimulationAgent(Agent):
    class RunSimulator(PeriodicBehaviour):
        async def on_start(self):
            self.sumo_api = SumoApi()

        async def run(self):
            self.sumo_api.simulation_step()

    def setup(self):
        print(f"[{self.jid}] Hello World! I'm agent {self.jid}")
        traci.start(["sumo-gui", "-c", "simulation/configuration/simulation.sumo.cfg"], label="simulation")
        self.add_behaviour(self.RunSimulator(period=1))
