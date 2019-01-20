#
# Config file for SUMOS
#

# should use kafka for config changes (else it uses json file)
kafkaUpdates = False

mqttUpdates = False
mqttHost = "localhost"
mqttPort = "1883"

# True if we want to use the SUMO GUI (always of in parallel mode)
sumoUseGUI = False  # False

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# Initial wait time before publishing overheads
initialWaitTicks = 1

# the total number of cars we use in our simulation
totalCarCounter = 600

# percentage of cars that are smart
smartCarPercentage = 1



# runtime dependent variable
processID = 0
parallelMode = False

epos_mode_read = True
epos_mode_write = True

random_seed = 1

epos_jar_path = "/Users/gerostat/Documents/research/EPOS CROWDNAV/release-0.0.1/epos-tutorial.jar"

vehicle_length = 5
