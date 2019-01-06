from os import path
from config import ROOT_DIR_PATH
import xml.etree.ElementTree as ET
import json

NET_XML_PATH_NAME = "simulation/configuration/simulation.net.xml"


def generate_topology():
    document_tree = ET.parse(path.join(ROOT_DIR_PATH, NET_XML_PATH_NAME))
    root = document_tree.getroot()

    topology_entries = {}

    traffic_light_junctions_ids = [child.get('id') for child in root if is_traffic_light_junction(child)]
    for child in root:
        if is_traffic_light_junction(child):
            entry_id, entry_data = create_topology_entry(child, traffic_light_junctions_ids)
            topology_entries[entry_id] = entry_data
    with open('topology.json', 'w') as outfile:
        json.dump(topology_entries, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def is_traffic_light_junction(child):
    return child.tag == 'junction' and child.attrib.get('type') == 'traffic_light'


def create_topology_entry(junction_element, traffic_light_junctions_ids):
    entry_id = junction_element.get('id') + '@jabb.im'
    lanes = junction_element.attrib.get('incLanes').split()
    roads = create_roads_entry(lanes)
    neighbours = create_neighbours_entry(lanes, traffic_light_junctions_ids)
    entry_data = {'roads': roads, 'neighbours': neighbours}
    return entry_id, entry_data


def create_roads_entry(lanes):
    vertical_road = {'streets': [lanes[0], lanes[2]], 'weight': 1}
    horizontal_road = {'streets': [lanes[1], lanes[3]], 'weight': 1}
    roads = {'vertical': vertical_road, 'horizontal': horizontal_road}
    return roads


def create_neighbours_entry(lanes, traffic_light_junctions_ids):
    neighbours = {}
    for lane in lanes:
        if is_lane_to_traffic_ligth_juntion(lane, traffic_light_junctions_ids):
            neighbours[lane] = lane[0:2] + '@jabb.im'
    return neighbours


def is_lane_to_traffic_ligth_juntion(lane, traffic_light_junctions_ids):
    return lane[0:2] in traffic_light_junctions_ids


if __name__ == "__main__":
    generate_topology()
