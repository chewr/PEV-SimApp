import csv
import server
from sets import Set
import cPickle as pickle
from geopy.distance import great_circle
import random
import matplotlib.pyplot as plt

print "Starting up"
server.routes.RouteFinder("google_api_key", "route_cache")

print "Opening csv..."
srd = csv.reader(open("hubway/hubway_stations.csv", 'rb'))

fld = srd.next()
print fld

stations = {}

print "Reading stations..."
nodes = Set([])
for row in srd:
	latlng = (float(row[4]), float(row[5]))
	stations[row[0]] = latlng
	nodes.add(latlng)

print "Writing stations to file..."
pickle.dump(stations, open("hubway_stations.pkl", "wb"))

## dists = []
## for a in stations:
## 	for b in stations:
## 		if b == a:
## 			continue
## 		dist = great_circle(stations[a], stations[b]).meters
## 		dists.append(dist)
## mindist = min(dists)
## maxdist = max(dists)
## num_bkts = 20
## bkt_size = (float(maxdist) - float(mindist)) / num_bkts
## bkts = []
## for i in xrange(num_bkts + 1):
## 	bkts.append(bkt_size * i)
## 
## #plt.hist(dists, bkts)
## plt.hist(dists)
## plt.show()
## exit()

media_lab = (42.3492699,-71.0900377)

all_fuzzed_locs = None
hubway_loc_file = "hubway_locs.pkl"
try:
	with open(hubway_loc_file, "rb") as f:
		all_fuzzed_locs = pickle.load(f)	
except:
	all_fuzzed_locs = Set([])

print "Fuzzing stations..."
fuzzy_stations = {}
for s in stations:
	fuzzball = Set([])
	ctr = stations[s]
	for i in xrange(10):
		lat = ctr[0] + random.gauss(0, .005) ## roughly adjusted for Boston's latitude
		lng = ctr[1] + random.gauss(0, .0005)
		pt = (lat, lng)
		# print "Checking", pt
		if server.routes.RouteFinder().get_dirs(pt, media_lab):
			# print "route to", pt, "found"
			if server.routes.RouteFinder().get_dirs(media_lab, pt):
				# print "route from", pt, "found"
				fuzzball.add(pt)
				all_fuzzed_locs.add(pt)
	
	fuzzy_stations[s] = fuzzball

print "Writing fuzzed stations to file"
pickle.dump(fuzzy_stations, open("fuzzed_stations.pkl", "wb"))
pickle.dump(all_fuzzed_locs, open(hubway_loc_file, "wb"))
