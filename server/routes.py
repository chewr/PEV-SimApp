## TODO a utility for routefinding through Googlemaps
## TODO create a more useful, space-efficient data type for the routes

import googlemaps
import cPickle as pickle
import atexit

class RouteFinder:
	def __init__(self, keyfile, cache_file):
		api_key = None
		with open(keyfile, 'r') as f:
			api_key = f.read().rstrip()
		self.client = googlemaps.Client(key=api_key)
		try:
        		with open(cache_file, "rb") as c:
				self.cache = pickle.load(c)
		except IOError:
			self.cache = {}

	def get_dirs(self, origin, dest):
		## TODO make cache more space efficient
		## TODO dynamic programming + graph algos for more cache hits?
		if (origin, dest) in self.cache:
			return self.cache[(origin,dest)]
		else:
			dirs = self.client.directions(origin, dest, mode="bicycling")
			self.cache[(origin, dest)] = dirs
			return dirs

	def save_cache(self, cache_file):
		pickle.dump(self.cache, open(cache_file, "wb"))

def getRouteDistance(rte):
	dist = 0
	for l in rte["legs"]:
		dist += l["distance"]["value"]
	return dist

finder = RouteFinder("google_api_key", ".routes_cache")

@atexit.register
def goodbye():
	print "exiting..."
	finder.save_cache(".routes_cache")
