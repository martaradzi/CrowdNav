#
# Config file for SUMOS
#

# should use kafka for config changes (else it uses json file)
kafkaUpdates = True
# the kafka host we want to send our messages to
kafkaHost = "localhost:9092"

mqttUpdates = False
mqttHost = "localhost"
mqttPort = "1883"

# the topic we send the kafka messages to
kafkaTopicTrips = "crowd-nav-trips"
kafkaTopicPerformance = "crowd-nav-performance"
kafkaTopicRouting = "crowd-nav-routing"
kafkaTopicTicks = "crowd-nav-ticks"

# where we receive system changes
kafkaCommandsTopic = "crowd-nav-commands"

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# Initial wait time before publishing overheads
initialWaitTicks = 200

# the total number of cars we use in our simulation
totalCarCounter = 450

# percentage of cars that are smart
smartCarPercentage = 0.2

sumoUseGUI = True

# runtime dependent variable
processID = 0
parallelMode = False
