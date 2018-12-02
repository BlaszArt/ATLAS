from spade.behaviour import OneShotBehaviour, PeriodicBehaviour, FSMBehaviour, State
from spade.message import Message
import asyncio, os, json


class SubscribeManager(OneShotBehaviour):
    """
    Crossroad agent behaviour for starting subscribing manager
    """
    async def run(self):
        self.agent.presence.subscribe(self.agent.manager_jid)


class UpdateTopology(PeriodicBehaviour):
    """
    Crossroad agent behaviour to update own topology based on manager status
    """
    async def run(self):
        msg = await self.receive()
        if msg:
            print(f"[{self.agent.jid}] Got message with new topology")
            msg_dict = json.loads(msg.body)
            self.agent.crossroad.roads = msg_dict['roads']
            self.agent.neighbours_jid = msg_dict['neighbours']
            for street in msg_dict['streets']:
                self.agent.crossroad.cars[street] = 0 if street not in self.agent.crossroad.cars else self.agent.crossroad.cars[street]
                self.agent.crossroad.lights[street] = 0
            self.agent.presence.set_available()


class ManagingTopology(FSMBehaviour):
    """
    Manager final state machine behaviour for managing topology in system
    """
    class CheckTopology(State):
        """
        FSM state for checking if topology changed
        """
        def has_stamp_changed(self):
            stamp = os.stat(self.agent.topology_src).st_mtime
            if stamp != self.agent._cached_stamp:
                self.agent._cached_stamp = stamp
                return True
            else:
                return False

        async def run(self):
            self.set_next_state("broadcast_topology") if self.has_stamp_changed() else self.set_next_state("no_changes")

    class NoTopologyChanges(State):
        """
        FSM state executed when topology not changed
        """
        async def run(self):
            self.set_next_state("check_topology")
            await asyncio.sleep(10)

    class BroadcastTopology(State):
        """
        FSM state executed when topology changed
        """
        def read_topology(self):
            with open(self.agent.topology_src, "r") as f:
                topology = json.load(f)
            return topology

        async def run(self):
            print(f"[{self.agent.jid}] There were changes in topology")
            for agent, topology in self.read_topology().items():
                # broadcast new topology
                msg = Message(to=agent)
                msg.set_metadata("performative", "request")
                msg.body = json.dumps(topology)
                await self.send(msg)
                # subscribe new agent
                if agent not in self.agent.presence.get_contacts():
                    self.agent.presence.subscribe(agent)

            self.set_next_state("check_topology")

    async def on_start(self):
        print(f"[{self.agent.jid}] FSM Managing topology starting at initial state {self.current_state}")
        self.add_state(name="check_topology", state=self.CheckTopology(), initial=True)
        self.add_state(name="no_changes", state=self.NoTopologyChanges())
        self.add_state(name="broadcast_topology", state=self.BroadcastTopology())
        self.add_transition(source="check_topology", dest="no_changes")
        self.add_transition(source="no_changes", dest="check_topology")
        self.add_transition(source="check_topology", dest="broadcast_topology")
        self.add_transition(source="broadcast_topology", dest="check_topology")

    async def on_end(self):
        print(f"[{self.agent.jid}] FSM Managing topology finished at state {self.current_state}")
