from app import Boot
import sys
import random
import argparse

# Handle arguments
parser = argparse.ArgumentParser(description='Executes CrowdNav application.')
parser.add_argument('--seed', help='Initializes random seed. Random seed if left blank.', type=int)
parser.add_argument('--parallel', help='Runs CrowdNav in parallel mode.', action='store_true')
parser.add_argument('--num_parallel', help='Number of parallel CrowdNav instances.', type=int, default=1)
parser.add_argument('--gui', help='Use SUMO GUI.', action='store_true')

# this starts the simulation (int parameters are used for parallel mode)
if __name__ == "__main__":
    args = parser.parse_args()
    useGUI = args.gui
    output = ""

    # In parallel mode
    if args.parallel:
      parallelMode = True
      processID    = int(args.num_parallel)
      output = "Starting CrowdNav in parallel mode with [%d] processes" % processID
    # In serial mode
    else:
      parallelMode = False
      processID    = 0
      output = "Starting CrowdNav in serial mode"

    # Debug string for seed
    if args.seed is not None:
      output += " and seed [%d]." % args.seed
    else:
      output += " and a random seed."
    print(output)


    # Start application
    Boot.start(processID, parallelMode, useGUI, args.seed)
