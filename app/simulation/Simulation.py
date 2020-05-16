import json
import traci
import traci.constants as tc
from app.network.Network import Network

from app.streaming import RTXForword
from colorama import Fore

from app import Config
from app.entitiy.CarRegistry import CarRegistry
from app.logging import info
from app.routing.CustomRouter import CustomRouter
from app.streaming import RTXConnector
import time

import random

# get the current system time
from app.routing.RoutingEdge import RoutingEdge

current_milli_time = lambda: int(round(time.time() * 1000))


class Simulation(object):
    """ here we run the simulation in """

    # the current tick of the simulation
    tick = 0

    # last tick time
    lastTick = current_milli_time()

    @classmethod
    def applyFileConfig(cls):
        """ reads configs from a json and applies it at realtime to the simulation """
        try:
            config = json.load(open('./knobs.json'))
            CustomRouter.explorationPercentage = config['explorationPercentage']
            CustomRouter.averageEdgeDurationFactor = config['averageEdgeDurationFactor']
            CustomRouter.maxSpeedAndLengthFactor = config['maxSpeedAndLengthFactor']
            CustomRouter.freshnessUpdateFactor = config['freshnessUpdateFactor']
            CustomRouter.freshnessCutOffValue = config['freshnessCutOffValue']
            CustomRouter.reRouteEveryTicks = config['reRouteEveryTicks']
        except:
            pass

    @classmethod
    def start(cls):
        """ start the simulation """
        info("# Start adding initial cars to the simulation", Fore.MAGENTA)
        # apply the configuration from the json file
        cls.applyFileConfig()
        CarRegistry.applyCarCounter()
        cls.loop()

    @classmethod
    # @profile
    def loop(cls):
        """ loops the simulation """

        counter = 1
        road_closed = False
        dissallowed_classes = ['private','emergency','army','vip','passenger','hov','taxi','bus','coach',
        'delivery','truck','trailer','tram','rail_urban','rail','rail_electric','motorcycle','moped','bicycle',
        'pedestrian','evehicle','ship','custom1','custom2']

        # start listening to all cars that arrived at their target
        traci.simulation.subscribe((tc.VAR_ARRIVED_VEHICLES_IDS,))
        while 1:
            # Do one simulation step
            cls.tick += 1
            traci.simulationStep()

            # Log tick duration to kafka
            duration = current_milli_time() - cls.lastTick
            cls.lastTick = current_milli_time()
            msg = dict()
            msg["duration"] = duration
            RTXForword.publish(msg, Config.kafkaTopicPerformance)

            # Check for removed cars and re-add them into the system
            for removedCarId in traci.simulation.getSubscriptionResults()[122]:
                # x = traci.vehicle.getIDCount()
                CarRegistry.findById(removedCarId).setArrived(cls.tick)


            timeBeforeCarProcess = current_milli_time()
            # let the cars process this step
            CarRegistry.processTick(cls.tick)
            # log time it takes for routing
            msg = dict()
            msg["duration"] = current_milli_time() - timeBeforeCarProcess
            RTXForword.publish(msg, Config.kafkaTopicRouting)

            # if we enable this we get debug information in the sumo-gui using global traveltime
            # should not be used for normal running, just for debugging
            # if (cls.tick % 10) == 0:
            # for e in Network.routingEdges:
            # 1)     traci.edge.adaptTraveltime(e.id, 100*e.averageDuration/e.predictedDuration)
            #     traci.edge.adaptTraveltime(e.id, e.averageDuration)
            # 3)     traci.edge.adaptTraveltime(e.id, (cls.tick-e.lastDurationUpdateTick)) # how old the data is

            # real time update of config if we are not in kafka mode
            if (cls.tick % 10) == 0:
                if Config.kafkaUpdates is False and Config.mqttUpdates is False:
                    # json mode
                    cls.applyFileConfig()
                else:
                    # kafka mode
                    newConf = RTXConnector.checkForNewConfiguration()
                    if newConf is not None:
                        if "exploration_percentage" in newConf:
                            CustomRouter.explorationPercentage = newConf["exploration_percentage"]
                            print("setting victimsPercentage: " + str(newConf["exploration_percentage"]))
                        if "route_random_sigma" in newConf:
                            CustomRouter.routeRandomSigma = newConf["route_random_sigma"]
                            print("setting routeRandomSigma: " + str(newConf["route_random_sigma"]))
                        if "max_speed_and_length_factor" in newConf:
                            CustomRouter.maxSpeedAndLengthFactor = newConf["max_speed_and_length_factor"]
                            print("setting maxSpeedAndLengthFactor: " + str(newConf["max_speed_and_length_factor"]))
                        if "average_edge_duration_factor" in newConf:
                            CustomRouter.averageEdgeDurationFactor = newConf["average_edge_duration_factor"]
                            print("setting averageEdgeDurationFactor: " + str(newConf["average_edge_duration_factor"]))
                        if "freshness_update_factor" in newConf:
                            CustomRouter.freshnessUpdateFactor = newConf["freshness_update_factor"]
                            print("setting freshnessUpdateFactor: " + str(newConf["freshness_update_factor"]))
                        if "freshness_cut_off_value" in newConf:
                            CustomRouter.freshnessCutOffValue = newConf["freshness_cut_off_value"]
                            print("setting freshnessCutOffValue: " + str(newConf["freshness_cut_off_value"]))
                        if "re_route_every_ticks" in newConf:
                            CustomRouter.reRouteEveryTicks = newConf["re_route_every_ticks"]
                            print("setting reRouteEveryTicks: " + str(newConf["re_route_every_ticks"]))
                        if "total_car_counter" in newConf:
                            CarRegistry.totalCarCounter = newConf["total_car_counter"]
                            CarRegistry.applyCarCounter()
                            print("setting totalCarCounter: " + str(newConf["total_car_counter"]))
                        if "edge_average_influence" in newConf:
                            RoutingEdge.edgeAverageInfluence = newConf["edge_average_influence"]
                            print("setting edgeAverageInfluence: " + str(newConf["edge_average_influence"]))

            # print status update if we are not running in parallel mode
            if (cls.tick % 100) == 0 and Config.parallelMode is False:
                print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                    traci.vehicle.getIDCount()) + "/" + str(
                    CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                    CarRegistry.totalTripAverage) + "(" + str(
                    CarRegistry.totalTrips) + ")" + " # avgTripOverhead: " + str(
                    CarRegistry.totalTripOverheadAverage))
           
            
            if (cls.tick % 5000) == 0 and Config.parallelMode is False:
                x = counter / 6
                counter += 1
                if x < 1:
                    n = 450
                elif x >= 1 and x < 2:
                    n = 520               
                elif x >= 2 and x < 3:
                    n =	600
                elif x >= 3 and x < 4:
                    n = 350
                elif x >= 4 and x < 5:
                    n = 200
                elif x >= 5 and x < 6:
                    n = 50
                elif x >= 6 and x < 7:
                    n = 200
                elif x >= 7 and x < 8:
                    n = 50
                elif x >= 8 and x < 9:
                    n = 150
                elif x >= 9 and x <10:
                    n = 500
                elif x >= 10 and x < 11:
                    n = 550
                elif x >= 11 and x < 12:
                    n = 620
                elif x >= 12 and x < 13:
                    n = 500
                elif x >= 13 and x < 14:
                    n = 300
                elif x >= 14 and x < 15:
                    n = 100
                elif x >= 15 and x < 16:
                    n = 100
                elif x >= 16 and x < 17:
                    n = 550
                elif x >= 17 and x < 18:
                    n = 500
                elif x >= 18 and x < 19:
                    n = 600
                elif x >= 19 and x < 20:
                    n = 720
                elif x >= 20 and x < 21:
                    n = 350
                elif x >= 21 and x < 22:
                    n = 200
                elif x >= 22 and x < 23:
                    n = 70
                elif x >= 23 and x < 24:
                    n = 500
                else:
                    n = 450
                    # change lane avilibility if not already closed
                    if road_closed == False:
                        traci.lane.setMaxSpeed('-2748_0', 0.1)
                        traci.lane.setMaxSpeed('-2748_1', 0.1)
                        traci.lane.setMaxSpeed('2748_0', 0.1)
                        traci.lane.setMaxSpeed('2748_1', 0.1)

                        traci.lane.setMaxSpeed('-2808_0', 0.1)
                        traci.lane.setMaxSpeed('-2808_1', 0.1)
                        traci.lane.setMaxSpeed('2808_0', 0.1)
                        traci.lane.setMaxSpeed('2808_1', 0.1)

                        traci.lane.setMaxSpeed('-2954_0', 0.1)
                        traci.lane.setMaxSpeed('-2954_1', 0.1)
                        traci.lane.setMaxSpeed('2954_0', 0.1)
                        traci.lane.setMaxSpeed('2954_1', 0.1)
                        road_closed = True
                    # reset counter to start a new 'day'
                    counter = 1

                CarRegistry.totalCarCounter = n
                CarRegistry.applyCarCounter()
                

            if (cls.tick % 10) == 0:
                msg = dict()
                msg["tick"] = cls.tick 
                RTXForword.publish(msg, Config.kafkaTopicTicks)
                # print("setting totalCarCounter: " + str(newConf["total_car_counter"]))

                # @depricated -> will be removed
                # # if we are in paralllel mode we end the simulation after 10000 ticks with a result output
                # if (cls.tick % 10000) == 0 and Config.parallelMode:
                #     # end the simulation here
                #     print(str(Config.processID) + " -> Step:" + str(cls.tick) + " # Driving cars: " + str(
                #         traci.vehicle.getIDCount()) + "/" + str(
                #         CarRegistry.totalCarCounter) + " # avgTripDuration: " + str(
                #         CarRegistry.totalTripAverage) + "(" + str(
                #         CarRegistry.totalTrips) + ")" + " # avgTripOverhead: " + str(
                #         CarRegistry.totalTripOverheadAverage))
                #     return
