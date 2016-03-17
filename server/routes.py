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
		## TODO dynamic programming + graph algos for more cache hits?
		## TODO do we need to do multiple modes? (bicycling vs driving)?
		
		if (origin, dest) not in self.cache:
			self.cache[(origin, dest)] = Route(self.client.directions(origin, dest, mode="bicycling"))
		return self.cache[(origin,dest)]

	def save_cache(self, cache_file):
		pickle.dump(self.cache, open(cache_file, "wb"))

class Route:
	## TODO make more space efficient
	def __init__(self, route):
		self.route = route[0] ## TODO handle the alternate routes?
		dist = 0
		dur = 0
		for l in route[0]["legs"]:
			dist += l["distance"]["value"]
			dur += l["duration"]["value"]
		self.distance = dist
		self.duration = dur

	def getDistance(self):
		return self.distance

	def getDuration(self):
		return self.duration
		
finder = RouteFinder("google_api_key", ".routes_cache")

@atexit.register
def goodbye():
	print "exiting..."
	finder.save_cache(".routes_cache")
