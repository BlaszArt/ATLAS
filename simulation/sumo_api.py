import re
from enum import Enum

import traci

from .enums import traffic_ligth_colors as tlc
from .exceptions import lane_control_exception as lce


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SumoApi(metaclass=Singleton):
    def __init__(self):
        pattern = re.compile('[A-Z][0-9][A-Z][0-9]_0')
        self.simulation = traci.getConnection("simulation")
        self.lanes = [lane for lane in self.simulation.lane.getIDList() if pattern.match(lane)]
        self.vehicles_on_lanes_dict = {lane: 0 for lane in self.lanes}

    def change_light_duration(self, agent_jid, change_by):
        trafficlight_id = self._trafficlight_id_from_agent_jid(agent_jid)
        new_remaining = change_by + self._get_phase_remaining_sec(trafficlight_id)
        self.simulation.trafficlight.setPhaseDuration(trafficlight_id, new_remaining)

    def get_cars_on_lane(self, lane_id):
        return self.vehicles_on_lanes_dict[lane_id]

    def get_light_on_lane(self, agent_jid, lane_id):
        trafficlight_id = self._trafficlight_id_from_agent_jid(agent_jid)
        if lane_id not in self.lanes:
            raise lce.LaneControlException('Lane with id {} does not exist'.format(lane_id))
        if not self._is_lane_controlled_by_selected_trafficlight(lane_id, trafficlight_id):
            raise lce.LaneControlException('Lane with id {} not controlled traffic light with id {}'.format(lane_id, trafficlight_id))
        controlled_lanes = self._get_lanes_controlled_by_trafficligth(trafficlight_id)
        segregated_lanes = self._segregate_lanes_clockwise_by_names(controlled_lanes, trafficlight_id)
        red_yellow_green_state = self.simulation.trafficlight.getRedYellowGreenState(trafficlight_id)
        lane_pos_in_segregated = segregated_lanes.index(lane_id)
        return tlc.TrafficLightColors.get_light_color(
            red_yellow_green_state[4 * lane_pos_in_segregated: 4 * (lane_pos_in_segregated + 1)])

    def simulation_step(self):
        self.simulation.simulationStep()
        self._refresh_vehicles_number_on_lanes()

    def get_simulation_time(self):
        return self.simulation.simulation.getTime()

    def _get_phase_next_switch(self, trafficlight_id):
        return self.simulation.trafficlight.getNextSwitch(trafficlight_id)

    def _get_phase_remaining_sec(self, trafficlight_id):
        return self._get_phase_next_switch(trafficlight_id) - self.get_simulation_time()

    def _refresh_vehicles_number_on_lanes(self):
        for lane_id in self.vehicles_on_lanes_dict.keys():
            self.vehicles_on_lanes_dict[lane_id] = self.vehicles_on_lanes_dict[
                                                       lane_id] + self._get_lane_vehicles_change(lane_id)

    def _get_lane_vehicles_change(self, lane_id):
        vehicles_at_start_of_lane = self.simulation.inductionloop.getVehicleData(lane_id + 'a')
        vehicles_at_end_of_lane = self.simulation.inductionloop.getVehicleData(lane_id + 'b')
        vehicles_arrived = sum([vehicle[3] != -1 for vehicle in vehicles_at_start_of_lane])
        vehicles_left = sum([vehicle[3] != -1 for vehicle in vehicles_at_end_of_lane])
        return vehicles_arrived - vehicles_left

    def _is_lane_controlled_by_selected_trafficlight(self, lane_id, trafficlight_id):
        lane_to = lane_id[2:4]
        return lane_to == trafficlight_id

    def _get_lanes_controlled_by_trafficligth(self, trafficlight_id):
        return [lane for lane in self.lanes if self._is_lane_controlled_by_selected_trafficlight(lane, trafficlight_id)]

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

    def _trafficlight_id_from_agent_jid(self, agent_jid):
        return agent_jid[:2].upper()


class Directions(Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4
