from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import traci
from sumolib import checkBinary

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


def get_lane_traffic(lane_name):
    res_a = traci.inductionloop.getLastStepVehicleNumber(lane_name + 'a')
    res_b = traci.inductionloop.getLastStepVehicleNumber(lane_name + 'b')
    return res_a - res_b


def run():
    """execute the TraCI control loop"""
    step = 0
    balance = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1

        res = get_lane_traffic('A3A2_0')
        if res != 0:
            balance += res
            print('\nSimilation step %d' % step)
            print('A3A2_0 vehicles change: %d' % res)
            print('Balance: %d' % balance)
            sys.stdout.flush()

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

    traci.start([sumoBinary, "-c", "configuration/simulation.sumo.cfg"])
    run()
