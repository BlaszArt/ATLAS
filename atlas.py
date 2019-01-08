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

import os
import sys
import time

# os.environ['PYTHONASYNCIODEBUG'] = '1'
from agents.manager_agent import ManagerAgent
from agents.simulator_agent import SimulationAgent
from utils.agents_generator import AgentsGenerator
from config import CROSSROAD_AGENTS_ON

if __name__ == '__main__':
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    sim = SimulationAgent("sim@jabbim.pl", "simulator")

    if CROSSROAD_AGENTS_ON:
        ma1 = ManagerAgent("ma1@jabbim.pl", "manageragent1", topology='simulation/generators/topology.json')
        agents = AgentsGenerator.generate_agents('simulation/generators/topology.json', 'ma1@jabbim.pl')
        AgentsGenerator.start_agents(agents)

    sim.start()

    if CROSSROAD_AGENTS_ON:
         ma1.start()

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for agent in agents:
                agent.stop()
            sim.stop()
            ma1.stop()

            break
