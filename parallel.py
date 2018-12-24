from __future__ import print_function

from subprocess import Popen

import sys
import argparse
import os

os.environ["CROWDNAV"] = '/home/erik/research/DARTS-CORRECTBRANCH/CrowdNav'
from app import Boot

# Handle arguments
parser = argparse.ArgumentParser(description='Executes CrowdNav application.')
parser.add_argument('--seed', help='Initializes random seed. Random seed if left blank.', type=int)
parser.add_argument('--processor_count', help='Number of processors to use.', type=int, default=4)

# this script is used to run CrowdNav on multiple processes
# call it with >parallel.py --processor_count #threads
if __name__ == "__main__":
    args = parser.parse_args()

    for i in range(0, args.processor_count):
        if args.seed is not None:
          simulation = Popen(["python", "./run.py", "--process_id", str(i), "--seed", str(args.seed)])
          print("Simulation " + str(i) + " started - seed [%d]..." % args.seed)
        else:
          simulation = Popen(["python", "./run.py", "--process_id", str(i)])
          print("Simulation " + str(i) + " started - random seed...")
