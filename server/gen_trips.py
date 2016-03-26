import cPickle as pickle
import dynamic_trips as gen
import routes
import sim_util

f = routes.finder

class Trip:
	def __init__(self, start, dest, dist, route):
		self.start = start
		self.dest = dest
		self.dist = dist
		self.route = route
trips = []
tripfile = '.trips_def'
try:
	with open(tripfile, 'rb') as c:
		trips = pickle.load(c)
except:
	trips = []

for maxDist in xrange(0, 8000, 250):
	for i in xrange(10):
		(start, dest) = gen.getTripLocation(maxDist)
		rte = f.get_dirs(start, dest)
		if rte is not None:
			trips.append(Trip(start, dest, sim_util.ll_dist_m(start, dest), rte))

trips.sort(lambda x: x.dist)

pickle.dump(trips, open(tripfile, 'wb'))
