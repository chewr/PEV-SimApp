import random
import time
import cPickle as pickle
import routes
import csv
from sets import Set

import sim_util
import trip

loc_file = ".loc_file"
locs = Set([])

class Ride:
	def __init__(self, start, dest, dist, route):
		self.start = start
		self.dest = dest
		self.dist = dist
		self.route = route
	def __repr__(self):
		return repr((self.dist, self.start, self.dest))

def locsFromFile(loc_csv):
	with open(loc_csv, 'r') as c:
		reader = csv.reader(c)
		for row in reader:
			try:
				locs.add((float(row[4]), float(row[3])))
				locs.add((float(row[8]), float(row[7])))
			except ValueError:
				pass
	pickle.dump(locs, open(loc_file, 'wb'))


def getRandomTripTimes(frequency, start, end):
	random.seed()
	mu = frequency * float(end - start) / 3600
	num_trips = int(random.gauss(mu, mu / 10))
	out = []
	for i in xrange(num_trips):
		out.append(random.randint(start, end))
	out.sort()
	return out

def getTripLocation(maxDist):
	random.seed()
	if maxDist is None or maxDist <= 0:
		return random.sample(locs, 2)
	scaleFactor = 4
	pulledPoints = random.sample(locs, scaleFactor)

	## low-overhead O(n^2) algorithm with some
	## intelligence to reduce duplicated work
	## Probably somewhat fast for large maxDist
	checked = 0
	while True:
		## invariant: no pairs (pp[i], pp[j]) for i, j < checked qualify (are nearer than maxDist)
		for i in xrange(checked, len(pulledPoints)):
			for j in xrange(len(pulledPoints)):
				if i != j and sim_util.ll_dist_m(pulledPoints[i], pulledPoints[j]) <= maxDist:
					return (pulledPoints[i], pulledPoints[j])
		checked = len(pulledPoints)
		pulledPoints.extend(random.sample(locs, scaleFactor))

def genRides(maxDist, total):
	f = routes.finder
	trips = []
	ridesFile = '.rides_def'
	try:
		with open(ridesFile, 'rb') as c:
			trips = pickle.load(c)
	except:
		trips = []

	tn = total / (maxDist / 800)
	
	for rideDist in xrange(0, maxDist, 800):
		for i in xrange(tn):
			(start, dest) = getTripLocation(rideDist)
			rte = f.get_dirs(start, dest)
			if rte is not None:
				trips.append(Ride(start, dest, sim_util.ll_dist_m(start, dest), rte))
	
	trips.sort(key=lambda x: x.dist)
	
	pickle.dump(trips, open(ridesFile, 'wb'))
		
def randomizedPreprocessedRides(filename, frequency, maxDist, start, end):
	trips = []
	try:
		with open(filename, 'rb') as c:
			trips = pickle.load(c)
		trips.sort(key=lambda x: x.dist)
	except Exception as e:
		print "couldn't load trips file '" + filename + "'"
		print "Encountered exception: " + str(e)
		return []
	print "trips loaded: " + str(len(trips))
	tripTimes = getRandomTripTimes(frequency, start, end)
	print "generating trips for " + str(len(tripTimes)) + " times"
        idx = 0
	for t in trips:
		idx += 1
		if t.dist > float(maxDist):
			break
	print "found " + str(idx - 1) + " trips shorter than " + str(maxDist)
	random.seed()
	if idx - 1 < len(tripTimes):
		rides = [random.sample(trips[:idx], 1) for i in xrange(len(tripTimes))]
		return zip(tripTimes, rides)
	else:
		return zip(tripTimes, random.sample(trips[:idx], len(tripTimes)))
	

def assembleTripSim(hMaxDist, hFreq, pMaxDist, pFreq, start, end):
	humanRiders = randomizedPreprocessedRides('.rides_def', hFreq, hMaxDist, start, end)
	parcels = randomizedPreprocessedRides('.rides_def', pFreq, pMaxDist, start, end)
	pickups = []
	ids = 0
	for h in humanRiders:
		pickups.append(trip.Pickup(ids, h[0], h[1].start, h[1].dest, True, route=h[1].route))
		ids += 1
	for p in parcels:
		pickups.append(trip.Pickup(ids, p[0], p[1].start, p[1].dest, True, route=p[1].route))
		ids += 1
	pickups.sort(key=lambda x: x.getTimeOrdered())
	return pickups

try:
	with open(loc_file, "rb") as l:
		locs = pickle.load(l)
except IOError:
	print "couldn't find locations file. Importing new..."
	for i in xrange(24):
		locsFromFile("../dataprocessing/bucketsamples/Hour_" + str(i) + "_100.csv")

