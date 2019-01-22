#
# Config file for SUMOS
#

# should use kafka for config changes (else it uses json file)
# TODO delete those
###############################
kafkaUpdates = False
mqttUpdates = False
mqttHost = "localhost"
mqttPort = "1883"
# Initial wait time before publishing overheads
initialWaitTicks = 1
# percentage of cars that are smart
smartCarPercentage = 1

epos_mode_read = True
epos_mode_write = True

# runtime dependent variable
processID = 0
parallelMode = False

######################################
####### GENERAL CONFIGURATION ########
######################################
# True if we want to use the SUMO GUI (always of in parallel mode)
sumoUseGUI = False  # False

random_seed = 1

vehicle_length = 5

epos_jar_path = "/Users/gerostat/Documents/research/EPOS CROWDNAV/release-0.0.1/epos-tutorial.jar"
######################################

######################################
#### CONFIGURATION OF SIMULATION #####
######################################

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# the total number of cars we use in our simulation
totalCarCounter = 600

simulation_horizon = 299

######################################
##### CONFIGURATION OF PLANNING ######
######################################
start_with_epos_optimization = False

planning_period = 100
planning_steps = 3
planning_step_horizon = 100

# double from [0, 1], unfairness + selfishness <= 1, unfairness
alpha = 0
# double from [0, 1], unfairness + selfishness <= 1, selfishness or local objective
beta = 0

######################################
##### CONFIGURATION OF PLANNING ######
######################################

adaptation_period = 150

