import sys
import random
import argparse
import os

os.environ["CROWDNAV"] = '/home/erik/research/DARTS-CORRECTBRANCH/CrowdNav'
from app import Boot

# Handle arguments
parser = argparse.ArgumentParser(description='Executes CrowdNav application.')
parser.add_argument('--seed', help='Initializes random seed. Random seed if left blank.', type=int)
parser.add_argument('--process_id', help='Process ID to use.', type=int, default=0)
parser.add_argument('--gui', help='Use SUMO GUI.', action='store_true')

# this starts the simulation (int parameters are used for parallel mode)
if __name__ == "__main__":
    args = parser.parse_args()

    # Check for parallel mode
    parallelMode = False
    if args.process_id > 0:
      parallelMode = True

    # Start application
    Boot.start(args.process_id, parallelMode, args.gui, args.seed)
