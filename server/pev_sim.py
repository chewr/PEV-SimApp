## TODO run simulation of a fleet of PEVs carrying out a
## a set of pickup/dropoff tasks

import fleet as pev

class Sim_env:
	def __init__(self, fleet_size, bounds, start_loc):
		self.bounds = bounds
		self.fleet = pev.Fleet(fleet_size, bounds, start_loc)

	def schedule(self, start_time, trips):
		## trips is a sorted list of Trip objects,
		## sorted by pickup time
		for t in trips:
			self.fleet.assign_task(t)
