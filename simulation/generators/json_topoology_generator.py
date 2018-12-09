from os import path
from config import ROOT_DIR_PATH
import xml.etree.ElementTree as ET
import json

NET_XML_PATH_NAME = "simulation\\configuration\\simulation.net.xml"


def generate_topology():
    document_tree = ET.parse(path.join(ROOT_DIR_PATH, NET_XML_PATH_NAME))
    root = document_tree.getroot()

    topology_entries = {}

    for child in root:
        if child.tag == 'junction' and child.attrib.get('type') == 'traffic_light':
            entry_id, entry_data = create_topology_entry(child)
            topology_entries[entry_id] = entry_data
    with open('topology.json', 'w') as outfile:
        json.dump(topology_entries, outfile, sort_keys=True, indent=4, separators=(',', ': '))

def create_topology_entry(junction_element):
    entry_id = junction_element.get('id') + '@jabbim.pl'
    lanes = junction_element.attrib.get('incLanes').split()
    roads = create_roads_entry(lanes)
    neighbours = create_neighbours_entry(lanes)
    entry_data = {'roads': roads, 'neighbours': neighbours}
    return entry_id, entry_data


def create_roads_entry(lanes):
    vertical_road = {'streets': [lanes[0], lanes[2]], 'weight': 1}
    horizontal_road = {'streets': [lanes[1], lanes[3]], 'weight': 1}
    roads = {'vertical': vertical_road, 'horizontal': horizontal_road}
    return roads


def create_neighbours_entry(lanes):
    neighbours = {}
    for lane in lanes:
        neighbours[lane] = lane[0:2] + '@jabbim.pl'
    return neighbours


if __name__ == "__main__":
    generate_topology()
