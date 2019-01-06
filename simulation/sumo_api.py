from enum import Enum
from threading import Lock

import traci

from .exceptions import lane_control_exception as lce


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

lock = Lock()

class SumoApi(metaclass=Singleton):
    SUMO_COLORS_ENCODED = {"GGgg": 1, "rrrr": 0,
                           "yyyy": 2}

    def __init__(self):
        self.simulation = traci.getConnection("simulation")
        trafficlight_ids = self.simulation.trafficlight.getIDList()
        self.controlled_lanes = []
        for trafficlight_id in trafficlight_ids:
            self.controlled_lanes = self.controlled_lanes + list(
                set(self.simulation.trafficlight.getControlledLanes(trafficlight_id)))
        self.vehicles_on_lanes_dict = {lane: 0 for lane in self.controlled_lanes}
        self.lanes_lights_dict = {}
        self.change_light_request_dict = {}
        self.simulation_step_ = 0
        with open('simulation.csv', 'w') as f:
            f.write('STEP;' + ';'.join(self.vehicles_on_lanes_dict.keys()) + '\n')


    def simulation_step(self):
        self.simulation.simulationStep()
        self._get_simulation_step()
        self._refresh_vehicles_number_on_lanes()
        self._refresh_lights_on_lanes()
        self._execute_light_changes_reguests()
        print(self.vehicles_on_lanes_dict)
        with open('simulation.csv', 'a') as f:
            f.write(str(int(self.simulation_step_)) + ';' + ';'.join([str(x) for x in self.vehicles_on_lanes_dict.values()]) + '\n')


    def get_cars_on_lane(self, lane_id):
        return self.vehicles_on_lanes_dict[lane_id]

    def get_light_on_lane(self, lane_id):
        return self.lanes_lights_dict[lane_id]

    def _get_light_on_lane(self, lane_id):
        if lane_id not in self.controlled_lanes:
            raise lce.LaneControlException('Lane with id {} does not controlled by traffic lights'.format(lane_id))
        trafficlight_id = lane_id[2:4]
        controlled_lanes = list(set(self.simulation.trafficlight.getControlledLanes(trafficlight_id)))
        segregated_lanes = self._segregate_lanes_clockwise_by_names(controlled_lanes, trafficlight_id)
        red_yellow_green_state = self.simulation.trafficlight.getRedYellowGreenState(trafficlight_id)
        lane_pos_in_segregated = segregated_lanes.index(lane_id)
        return self.SUMO_COLORS_ENCODED.get(
            red_yellow_green_state[4 * lane_pos_in_segregated: 4 * (lane_pos_in_segregated + 1)])

    def _refresh_lights_on_lanes(self):
        for lane_id in self.controlled_lanes:
            self.lanes_lights_dict[lane_id] = self._get_light_on_lane(lane_id)

    def _get_lane_vehicles_change(self, lane_id):
        vehicles_at_start_of_lane = self.simulation.inductionloop.getVehicleData(lane_id + 'a')
        vehicles_at_end_of_lane = self.simulation.inductionloop.getVehicleData(lane_id + 'b')
        vehicles_arrived = sum([vehicle[3] != -1 for vehicle in vehicles_at_start_of_lane])
        vehicles_left = sum([vehicle[3] != -1 for vehicle in vehicles_at_end_of_lane])
        return vehicles_arrived - vehicles_left

    def _refresh_vehicles_number_on_lanes(self):
        for lane_id in self.controlled_lanes:
            self.vehicles_on_lanes_dict[lane_id] = self.vehicles_on_lanes_dict[
                                                       lane_id] + self._get_lane_vehicles_change(lane_id)

    def get_simulation_time(self):
        return self.simulation_step_

    def _get_simulation_step(self):
        self.simulation_step_ = self.simulation.simulation.getTime()

    def _segregate_lanes_clockwise_by_names(self, lanes, trafficlight_id):
        segregated_list = [self._get_north_lane(lanes, trafficlight_id), self._get_east_lane(lanes, trafficlight_id),
                           self._get_south_lane(lanes, trafficlight_id), self._get_west_lane(lanes, trafficlight_id)]
        segregated_list = [lane_id for lane_id in segregated_list if lane_id is not None]
        return segregated_list

    def _get_north_lane(self, lanes, trafficlight_id):
        for lane in lanes:
            if ord(lane[0]) == ord(trafficlight_id[0]) and int(lane[1]) == int(trafficlight_id[1]) + 1:
                return lane
        return None

    def _get_east_lane(self, lanes, trafficlight_id):
        for lane in lanes:
            if ord(lane[0]) == ord(trafficlight_id[0]) + 1 and int(lane[1]) == int(trafficlight_id[1]):
                return lane
        return None

    def _get_south_lane(self, lanes, trafficlight_id):
        for lane in lanes:
            if ord(lane[0]) == ord(trafficlight_id[0]) and int(lane[1]) == int(trafficlight_id[1]) - 1:
                return lane
        return None

    def _get_west_lane(self, lanes, trafficlight_id):
        for lane in lanes:
            if ord(lane[0]) == ord(trafficlight_id[0]) - 1 and int(lane[1]) == int(trafficlight_id[1]):
                return lane
        return None

    def change_light_duration(self, agent_jid, change_by):
        lock.acquire()
        self.change_light_request_dict[agent_jid] = change_by
        lock.release()

    def _change_light_duration(self, agent_jid, change_by):
        trafficlight_id = self._trafficlight_id_from_agent_jid(agent_jid)
        new_remaining = max(change_by + self._get_phase_remaining_sec(trafficlight_id), 1)
        self.simulation.trafficlight.setPhaseDuration(trafficlight_id, new_remaining)

    def _trafficlight_id_from_agent_jid(self, agent_jid):
        return agent_jid[:2].upper()

    def _get_phase_next_switch(self, trafficlight_id):
        return self.simulation.trafficlight.getNextSwitch(trafficlight_id)

    def _get_phase_remaining_sec(self, trafficlight_id):
        return self._get_phase_next_switch(trafficlight_id) - self.simulation.simulation.getTime()

    def _execute_light_changes_reguests(self):
        lock.acquire()
        for agent_jid, change_by in self.change_light_request_dict.items():
            self._change_light_duration(agent_jid, change_by)
        self.change_light_request_dict = {}
        lock.release()


class Directions(Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4
