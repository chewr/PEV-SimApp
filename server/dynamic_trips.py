import random
import time
import cPickle as pickle
import csv
from sets import Set
import trip

import sim_util

loc_file = ".loc_file"
locs = Set([])

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
		
def generateTripsOverInterval(frequency, maxDist, start, end, is_human):
	tripTimes = getRandomTripTimes(frequency, start, end)
	out = []
	ct = 0
	for t in tripTimes:
		(start, dest) = getTripLocation(maxDist)
		out.append(trip.Pickup(ct, t, start, dest, is_human))
		ct += 1
			
	print len(out)	

def randomizedPreprocessedTrips(filename, frequency, maxDist, start, end, is_human):
	trips = []
	try:
		with open(filename, 'rb') as c:
			trips = pickle.load(c)
	except:
		return []
	tripTimes = getRandomTripTimes(frequency, start, end)
        out = []
        idx = 0
	for t in trips:
		idx =+ 1
		if t.dist > maxDist:
			break
	random.seed()
	subset = random.sample(trips[:idx], len(tripTimes))
	for i in xrange(len(tripTimes)):
		out.append(trip.Pickup(i, subset[i].start, subset[i].dest, is_human))
		

try:
	with open(loc_file, "rb") as l:
		locs = pickle.load(l)
except IOError:
	for i in xrange(24):
		locsFromFile("../dataprocessing/bucketsamples/Hour_" + str(i) + "_100.csv")

