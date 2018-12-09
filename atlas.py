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
os.environ['PYTHONASYNCIODEBUG'] = '1'

from agents.crossroad_agent import CrossroadAgent
from agents.manager_agent import ManagerAgent
import time
from web.web import Web
from utils.agents_generator import AgentsGenerator

if __name__ == '__main__':
    # ca1 = CrossroadAgent(jid="ca1@jabbim.pl", password="crossroad1", manager_jid="ma1@jabbim.pl", cars_speed=2)
    # ca2 = CrossroadAgent(jid="ca2@jabbim.pl", password="crossroad2", manager_jid="ma1@jabbim.pl", cars_speed=1)
    # ca3 = CrossroadAgent(jid="ca3@jabbim.pl", password="crossroad3", manager_jid="ma1@jabbim.pl", cars_speed=2)
    # ca4 = CrossroadAgent(jid="ca4@jabbim.pl", password="crossroad4", manager_jid="ma1@jabbim.pl", cars_speed=1)
    M1 = ManagerAgent("M1@localhost", "manageragent1", topology='simulation/generators/topology.json')
    # ca1.start_crossroad(neighbours={'S': ca4, 'W': ca1})
    # ca2.start_crossroad(neighbours={'S': ca4, 'W': ca1})
    # ca3.start_crossroad(neighbours={'N': ca1, 'E': ca4})
    # ca4.start_crossroad(neighbours={'N': ca2, 'W': ca3})

    agents = AgentsGenerator.generate_agents('simulation/generators/topology.json', 'M1@localhost')
    AgentsGenerator.start_agents(agents)
    print(agents)

    M1.start()

    agents.append(M1)

    time.sleep(5)
    Web.generate_web(agents, open_tab=True)

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            AgentsGenerator.stop_agents(agents)
            break
