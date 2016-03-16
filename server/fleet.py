## TODO a model for a fleet of PEVs in a city

import sim_util as util
import trip

class Vehicle:
	def __init__(self, is_pev, loc):
		self.is_pev = is_pev
		self.loc = loc

		self.route = []
		self.task = None
		self.free_at = 0
		## TODO representation here

	def update(self, time):
		## TODO implement - update task,
		## set location if necessary
		raise(NotImplementedError)

	def assign(self, task):
		raise(NotImplementedError)

class Fleet:
	def __init__(self, fleet_size, bounds):
		self.vehicles = []
		start_loc = util.center_of(bounds)
		for i in xrange(fleet_size):
			self.vehicles.append(
				Vehicle(True, start_loc))		

		
	def assign_task(trip):
		## TODO args, return?
		t = trip.getTimeOrdered()
		for v in vehicles:
			v.update(t)
		fsched.assign(t, trip, fleet)

	def __getitem__(self, key):
		return self.vehicles[key]
