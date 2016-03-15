## TODO a model for a request for pickup and delivery of a person or
## package

import routes
import sim_util

class Pickup:
	def __init__(self, time, start, dest, is_human):
		self.time_ordered = time
		self.start_loc = start
		self.dest_loc = dest
		self.is_human = is_human
		## TODO: differing fare priority
		## TODO: arrival time for packages

	def approx_dur(self):
		## based on 10 mph, gives as-bird-flies in seconds
		return sim_util.ll_dist_m(self.start_loc, self.dest_loc) / 4.47 
		
	def routefind(self):
		route = routes.finder.get_dirs(start, dest)[0]
		dur = 0
		for l in route["legs"]:
			dur += l["duration"]["value"]
		self.duration = dur
		self.route = route

