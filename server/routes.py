## TODO a utility for routefinding through Googlemaps
## TODO create a more useful, space-efficient data type for the routes

import googlemaps

class RouteFinder:
	def __init__(self, keyfile):
		api_key = None
		with open(keyfile, 'r') as f:
			api_key = f.read().rstrip()
		
		self.client = googlemaps.Client(key=api_key)
		self.cache = {}

	def get_dirs(origin, dest):
		## TODO make cache persistent
		## TODO make cache more space efficient
		## TODO dynamic programming + graph algos for more cache hits?
		## TODO veify cache is useful?
		if (origin, dest) in self.cache:
			return self.cache[(origin,dest)]
		else:
			dirs = client.directions(origin, dest, mode="bicycling")
			self.cache[(origin, dest)] = dirs
			return dirs

finder = RouteFinder("google_api_key")
