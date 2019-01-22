from numpy import mean, var
from app.adaptation import Knowledge

class Adaptation(object):

    overheads_index = 0
    streets_index = 0

    @classmethod
    def sense_and_adapt(cls, tick):

        average_trip_overhead = cls.__calculate_average_trip_overhead()
        average_street_utilization, variance_of_street_utilization = cls.__calculate_average_street_utilization()
        print "*******************"
        print "MONITOR"
        print "*******************"
        print "Adaptation triggered at tick " + str(tick)
        print "Average trip overhead: " + str(average_trip_overhead)
        print "Average street utilization: " + str(average_street_utilization)
        print "Variance of street utilization: " + str(variance_of_street_utilization)

        print "*******************"
        print "ANALYSIS"
        print "*******************"
        print "placeholder"

        print "*******************"
        print "PLANNING"
        print "*******************"
        print "placeholder"

        print "*******************"
        print "EXECUTION"
        print "*******************"
        Knowledge.planning_steps = 4
        Knowledge.beta = 1
        print "Changing planning steps to: " + str(Knowledge.planning_steps)
        print "*******************"


    @classmethod
    def __calculate_average_trip_overhead(cls):
        data = []
        with open("data/overheads.csv", 'r') as results:
            for i, line in enumerate(results):
                if i >= cls.overheads_index:
                    data.append(float(line.split(",")[6]))

            overheads_index_increment = len(data)
            cls.overheads_index += overheads_index_increment
        return mean(data)

    @classmethod
    def __calculate_average_street_utilization(cls):
        utilizations = []
        with open("data/streets.csv", 'r') as results:
            for i, line in enumerate(results):
                line = line.split(",")
                line[len(line)-1] = line[len(line)-1].replace('\r', '').replace('\n', '')
                if i == 0:
                    streets = line
                else:
                    if i > cls.streets_index:
                        utilizations.append([float(u) for u in line[1:]])
            streets_index_increment = len(utilizations)
            cls.streets_index += streets_index_increment

        streets_data = {}
        for i in range(len(streets)):
            streets_data[streets[i]] = [utilization[i] for utilization in utilizations]

        streets_data_means = [mean(value) for key, value in streets_data.iteritems()]

        return mean(streets_data_means), var(streets_data_means)