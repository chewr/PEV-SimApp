## TODO a model for a fleet of PEVs in a city

import sim_util as util
import trip
from collections import deque

class Dispatch:
	def __init__(self, start, end, kind, route, dest):
		self.start = start
		self.end = end
		self.kind = kind
		self.route = route
		self.dest = dest

	def getEndTime(self):
		return self.end

def create_dispatch(time, start, dest):
	rte = routes.finder.get_dirs(start, dest)
	dur = 0 ## TODO account for non-instant pickups?
	for l in rte["legs"]:
		dur += l["duration"]["value"]
	return Dispatch(time, time+dur, "NAV", rte, dest)

def dispatch_from_task(task, start_time):
	return Dispatch(start_time, start_time + task.getDuration(),
		task.getType(), task.getRoute(), task.getDest())

class Vehicle:
	def __init__(self, is_pev, loc):
		self.is_pev = is_pev
		self.loc = loc

		self.history = []
		self.todo = deque([])

		## TODO representation here

	def update(self, time):
		while self.todo:
			if self
			
		## TODO implement - update task,
		## set location if necessary
		raise(NotImplementedError)

	def assign(self, task, time):
		## TODO create the arrival Dispatch
		## and add to todo
		## create the passenger/fare dispatch
		## and add to todo
		if not self.todo:
			self.todo.append(create_dispatch(time, self.loc, task.getPickupLoc())
		else:
			self.todo.append(create_dispatch(self.soonestFreeAfter(time), self.todo[-1].dest, task.getPickupLoc())
		self.todo.append(dispatch_from_task(task, self.soonestFreeAfter(time)

	def soonestFreeAfter(self, t):
		## return the soonest time that the PEV will
		## be free after time t
		if not self.todo:
			return t
		else:
			return self.todo[-1].getEndTime()
			

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
		vid = fsched.assign(t, trip, fleet)
		print "task " + trip.getID() + " assigned to vehicle " + vid

	def __getitem__(self, key):
		return self.vehicles[key]
