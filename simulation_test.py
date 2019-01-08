from __future__ import absolute_import
from __future__ import print_function

import optparse
import os
import sys

import traci
from sumolib import checkBinary

from simulation.sumo_api import SumoApi

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

def run():
    """execute the TraCI control loop"""
    sumo_api = SumoApi()
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        sumo_api.simulation_step()
        step += 1
        print(step)
        print('C2C3_0 : ' + str(sumo_api.vehicles_on_lanes_dict['C2C3_0']))
        print(sumo_api.get_light_on_lane('C2', 'C3C2_0'))


        if step == 6:
            sumo_api.change_light_duration('D3', 1)

    traci.close()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "configuration/simulation.sumo.cfg"], label="simulation")
    run()
