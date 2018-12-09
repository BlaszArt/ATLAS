import json

from agents.crossroad_agent import CrossroadAgent


class AgentsGenerator:
    @staticmethod
    def generate_agents(file, manager_jid):
        agents = []
        with open(file, "r") as f:
            topology = json.load(f)

            for agent_jid, value in topology.items():
                neighbours = value['neighbours']
                agents.append(
                    CrossroadAgent(jid=agent_jid, neighbours=neighbours, password='crossroad' + agent_jid.split('@')[0],
                                   manager_jid=manager_jid, cars_speed=2))
        return agents

    @staticmethod
    def start_agents(agents):
        for agent in agents:
            agent.start()

    @staticmethod
    def stop_agents(agents):
        for agent in agents:
            agent.stop()
