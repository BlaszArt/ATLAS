import traci
import re

from enum import Enum

from exceptions import lane_control_exception as lce
from enums import traffic_ligth_colors as tlc


class SumoApi:
    def __init__(self):
        pattern = re.compile('[A-Z][0-9][A-Z][0-9]_0')
        self.lanes = [lane for lane in traci.lane.getIDList() if pattern.match(lane)]
        self.vehicles_on_lanes_dict = {lane: 0 for lane in self.lanes}

    def change_light_duration(self, agent_jid, remain_seconds):
        traci.trafficlight.setPhaseDuration(agent_jid, remain_seconds)

    def get_cars_on_lane(self, lane_id):
        return self.vehicles_on_lanes_dict[lane_id]

    def get_light_on_lane(self, agent_jid, lane_id):
        if lane_id not in self.lanes:
            raise lce.LaneControlException('Lane with that id does not exist')
        if not self._is_lane_controlled_by_selected_trafficlight(lane_id, agent_jid):
            raise lce.LaneControlException('Lane not controlled by that traffic light')
        controlled_lanes = self._get_lanes_controlled_by_trafficligth(agent_jid)
        segregated_lanes = self._segregate_lanes_clockwise_by_names(controlled_lanes, agent_jid)
        red_yellow_green_state = traci.trafficlight.getRedYellowGreenState(agent_jid)
        lane_pos_in_segregated = segregated_lanes.index(lane_id)
        return tlc.TrafficLightColors.get_light_color(
            red_yellow_green_state[4 * lane_pos_in_segregated: 4 * (lane_pos_in_segregated + 1)])

    def simulation_step(self):
        traci.simulationStep()
        self._refresh_vehicles_number_on_lanes()

    def _refresh_vehicles_number_on_lanes(self):
        for lane_id in self.vehicles_on_lanes_dict.keys():
            self.vehicles_on_lanes_dict[lane_id] = self.vehicles_on_lanes_dict[
                                                       lane_id] + self._get_lane_vehicles_change(lane_id)

    def _get_lane_vehicles_change(self, lane_id):
        vehicles_at_start_of_lane = traci.inductionloop.getVehicleData(lane_id + 'a')
        vehicles_at_end_of_lane = traci.inductionloop.getVehicleData(lane_id + 'b')
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
        segregated_list = filter(lambda lane_id: lane_id is not None, segregated_list)
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


class Directions(Enum):
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4
