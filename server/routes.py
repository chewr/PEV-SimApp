## TODO a utility for routefinding through Googlemaps
## TODO create a more useful, space-efficient data type for the routes

import googlemaps
import cPickle as pickle
import atexit
import sys

class RouteFinder:
	def __init__(self, keyfile, cache_file):
		api_key = None
		try:
			with open(keyfile, 'r') as f:
				api_key = f.read().rstrip()
		except:
			print "It looks like you need a google api key"
			sys.exit(1)
		self.client = googlemaps.Client(key=api_key)
		try:
        		with open(cache_file, "rb") as c:
				self.cache = pickle.load(c)
		except IOError:
			self.cache = {}

	def get_dirs(self, origin, dest):
		## TODO dynamic programming + graph algos for more cache hits?
		## TODO do we need to do multiple modes? (bicycling vs driving)?
		route = None
		try:
			route = self.client.directions(origin, dest, mode="bicycling")
		except googlemaps.exceptions.Timeout:
			print "Request timed out for " + str(origin) + " to " + str(dest)
			return None
		except Exception as e:
			print "Routefinding failed for " + str(origin) + " to " + str(dest)
			print "Encountered Exception: " + str(type(e)) + str(e.args)
			return None
		if route:
			if (origin, dest) not in self.cache:
				self.cache[(origin, dest)] = Route(route)
			return self.cache[(origin,dest)]
		else:
			print "Couldn't find route from " + str(origin) + " to " + str(dest)
			return None

	def save_cache(self, cache_file):
		pickle.dump(self.cache, open(cache_file, "wb"))

class Route:
	## TODO make more space efficient
	## TODO: must delete .routes_cache when this data structure is
	## updated
	def __init__(self, route):
		self.rte = route[0]
		## clean route
		removals = ["warnings", "waypoint_order", "summary", "copyrights"]
		for r in removals:
			del self.rte[r]

		## clean legs
		leg_removals = ["end_address", "via_waypoint", "start_address"]
		step_removals = ["html_instructions", "maneuver"]
		for l in self.rte["legs"]:
			for r in leg_removals:
				del l[r]
			for s in l["steps"]:
				for r in step_removals:
					try:
						del s[r]
					except:
						pass

		self.path = route[0]["overview_polyline"] ## TODO handle the alternate routes?
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
