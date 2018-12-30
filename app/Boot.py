import os, sys

from app.streaming import RTXConnector

sys.path.append(os.path.join(os.environ.get("SUMO_HOME"), "tools"))

from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.network.Network import Network
from app.simulation.Simulation import Simulation
from app.entitiy.CarRegistry import CarRegistry
from streaming import RTXForword
from colorama import Fore
from sumo import SUMOConnector, SUMODependency
import Config
import traci, sys, os
import thread
import time
import random


# uuid4()
def start(processID, parallelMode,useGUI,seed, configuration, car_count):
    """ main entry point into the application """

    # Seed application
    if (seed == None):
      random.seed()
    else:
      random.seed(seed)

    Config.processID = processID
    Config.parallelMode = parallelMode
    Config.sumoUseGUI = useGUI

    Config.kafkaTopicTrips = "crowd-nav-trips-" + str(processID)
    Config.kafkaCommandsTopic = "crowd-nav-commands-" + str(processID)
    Config.kafkaTopicRouting = Config.kafkaTopicRouting + "-" + str(processID)

    info('#####################################', Fore.CYAN)
    info('#      Starting CrowdNav v0.2       #', Fore.CYAN)
    info('#####################################', Fore.CYAN)
    info('# Configuration:', Fore.YELLOW)
    info('# Kafka-Host    -> ' + Config.kafkaHost, Fore.YELLOW)
    info('# Publishing to -> ' + Config.kafkaTopicTrips, Fore.YELLOW)
    info('# Publishing to -> ' + Config.kafkaTopicRouting, Fore.YELLOW)
    info('# Listening on  -> ' + Config.kafkaCommandsTopic, Fore.YELLOW)

    apply_car_count(car_count)
    apply_starting_configuration(configuration)

    # init sending updates to kafka and getting commands from there
    if Config.kafkaUpdates or Config.mqttUpdates:
        RTXForword.connect()
        RTXConnector.connect()

    # Check if sumo is installed and available
    SUMODependency.checkDeps()
    info('# SUMO-Dependency check OK!', Fore.GREEN)

    # Load the sumo map we are using into Python
    Network.loadNetwork()
    info(Fore.GREEN + "# Map loading OK! " + Fore.RESET)
    info(Fore.CYAN + "# Nodes: " + str(Network.nodesCount()) + " / Edges: " + str(Network.edgesCount()) + Fore.RESET)

    # After the network is loaded, we init the router
    CustomRouter.init()
    # Start sumo in the background
    SUMOConnector.start()
    info("\n# SUMO-Application " + str(processID) + " started OK!", Fore.GREEN)
    # Start the simulation
    Simulation.start()
    # Simulation ended, so we shutdown
    info(Fore.RED + '# Shutdown' + Fore.RESET)
    traci.close()
    sys.stdout.flush()
    return None


def apply_starting_configuration(conf):
    if "exploration_percentage" in conf:
        CustomRouter.explorationPercentage = conf["exploration_percentage"]
        info("# Setting victimsPercentage: " + str(conf["exploration_percentage"]), Fore.YELLOW)
    if "route_random_sigma" in conf:
        CustomRouter.routeRandomSigma = conf["route_random_sigma"]
        info("# Setting routeRandomSigma: " + str(conf["route_random_sigma"]), Fore.YELLOW)
    if "max_speed_and_length_factor" in conf:
        CustomRouter.maxSpeedAndLengthFactor = conf["max_speed_and_length_factor"]
        info("# Setting maxSpeedAndLengthFactor: " + str(conf["max_speed_and_length_factor"]), Fore.YELLOW)
    if "average_edge_duration_factor" in conf:
        CustomRouter.averageEdgeDurationFactor = conf["average_edge_duration_factor"]
        info("# Setting averageEdgeDurationFactor: " + str(conf["average_edge_duration_factor"]), Fore.YELLOW)
    if "freshness_update_factor" in conf:
        CustomRouter.freshnessUpdateFactor = conf["freshness_update_factor"]
        info("# Setting freshnessUpdateFactor: " + str(conf["freshness_update_factor"]), Fore.YELLOW)
    if "freshness_cut_off_value" in conf:
        CustomRouter.freshnessCutOffValue = conf["freshness_cut_off_value"]
        info("# Setting freshnessCutOffValue: " + str(conf["freshness_cut_off_value"]), Fore.YELLOW)
    if "re_route_every_ticks" in conf:
        CustomRouter.reRouteEveryTicks = conf["re_route_every_ticks"]
        info("# Setting reRouteEveryTicks: " + str(conf["re_route_every_ticks"]), Fore.YELLOW)


def apply_car_count(car_count):
    info("# Car count is " + str(car_count), Fore.YELLOW)
    CarRegistry.totalCarCounter = car_count