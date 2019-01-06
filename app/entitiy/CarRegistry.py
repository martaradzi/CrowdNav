from app import Config

from app.entitiy.Car import Car


class NullCar:
    """ a car with no function used for error prevention """
    def __init__(self):
        pass

    def setArrived(self, tick):
        pass


class CarRegistry(object):
    """ central registry for all our cars we have in the sumo simulation """

    # the total amount of cars that should be in the system
    totalCarCounter = Config.totalCarCounter
    # always increasing counter for carIDs
    carIndexCounter = 0
    # list of all cars
    cars = {}  # type: dict[str,app.entitiy.Car]
    # counts the number of finished trips
    totalTrips = 0
    # average of all trip durations
    totalTripAverage = 0
    # average of all trip overheads (overhead is TotalTicks/PredictedTicks)
    totalTripOverheadAverage = 0

    # @todo on shortest path possible -> minimal value

    @classmethod
    def selectOptimalRoutes(cls, output_folder_for_latest_run):

        with open(output_folder_for_latest_run + '/selected-plans.csv', 'r') as results:
            line_id = 1
            for line in results:
                if line_id == 41:
                    res = [int(x) for x in line.split(",")[2:]]
                    break
                line_id += 1

        for i in range(0, cls.carIndexCounter):
            c = cls.cars["car-" + str(i)]
            with open('./data/routes/agent_' + str(i) + '.routes', 'r') as plans_file:
                plans=plans_file.readlines()
            selected_route = plans[res[i]].replace('\r', '').replace('\n', '').split(",")
            c.change_route(selected_route)
            c.change_preference(res[i])

    @classmethod
    def applyCarCounter(cls):
        """ syncs the value of the carCounter to the SUMO simulation """
        while len(CarRegistry.cars) < cls.totalCarCounter:
            # to less cars -> add new
            c = Car("car-" + str(CarRegistry.carIndexCounter))
            cls.carIndexCounter += 1
            cls.cars[c.id] = c
            c.addToSimulation(0)
        while len(CarRegistry.cars) > cls.totalCarCounter:
            # to many cars -> remove cars
            (k, v) = CarRegistry.cars.popitem()
            v.remove()

    @classmethod
    def findById(cls, carID):
        """ returns a car by a given carID """
        try:
            return CarRegistry.cars[carID]  # type: app.entitiy.Car
        except:
            return NullCar()

    @classmethod
    def processTick(cls, tick):
        """ processes the simulation tick on all registered cars """
        for key in CarRegistry.cars:
            CarRegistry.cars[key].processTick(tick)
