

class Pickup:
	def __init__(self, time, start, dest, duration, route, is_human):
		self.time_ordered = time
		self.start_loc = start
		self.dest_loc = dest
		self.duration = duration
		self.route = route
		self.is_human = is_human
		## TODO: differing fare priority

