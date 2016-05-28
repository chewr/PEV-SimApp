import cPickle as pickle
import server
from datetime import datetime
import csv
import random
from sets import Set

print "Connecting to server"
server.routes.RouteFinder("google_api_key", "route_cache")

print "Opening stations"
stations = pickle.load(open("hubway/hubway_stations.pkl", 'rb'))

start_locs = list(stations)

print "Opening pickups"
pickups = pickle.load(open("filtered_pickupsthrough2012.pkl", "rb"))

print "Beginning simulation"

## test one at a time
size = 200 ## because if I over-automate it I'll blow through the google API cap

for i in [size]:
	env = server.pev_sim.Sim_env(i, None, start_locs)
	env.scheduleAll(pickups)
	outfile = "env-hubway_sim_all-fs-" + str(i) + ".pkl"

	print "Writing to outfile " + outfile

	pickle.dump(env, open(outfile, 'wb'))
