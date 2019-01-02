# Aktualne skrzyzowanie - numery w srodku to numery agentow - ca1 = crossroad_agent_1 itd.
# nastawione szybkosci sa takie, ze oba skrzyzowania po lewej szybciej przepuszczaja i generuja auta niz te po prawo
#
#    N        N
#    |        |
# -W--1--E--W--2--E
#    |        |
#    S        S
#    |        |
# -W--3--E--W--4--E
#    |        |
#    S        S

import os, sys
#os.environ['PYTHONASYNCIODEBUG'] = '1'

from agents.crossroad_agent import CrossroadAgent
from agents.manager_agent import ManagerAgent
from agents.simulator_agent import SimulationAgent
import time
from web.web import Web
from utils.agents_generator import AgentsGenerator

if __name__ == '__main__':
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sim = SimulationAgent("sim@jabbim.pl", "simulator")

    ma1 = ManagerAgent("ma1@jabbim.pl", "manageragent1", topology='simulation/generators/topology.json')
    agents = AgentsGenerator.generate_agents('simulation/generators/topology.json', 'ma1@jabbim.pl')
    AgentsGenerator.start_agents(agents)

    sim.start()
    ma1.start()


    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for agent in agents:
                agent.stop()
            ma1.stop()
            sim.stop()
            break
