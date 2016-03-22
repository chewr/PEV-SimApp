## TODO a model for a fleet of PEVs in a city

import sim_util as util
import trip
import fsched
import routes

class Dispatch:
	def __init__(self, start, end, kind, route, dest, wait_time):
		self.start = start
		self.end = end
		self.kind = kind
		self.route = route
		self.dest = dest
		self.wait_time = wait_time
		if not route is None:
			self.route_distance = route.getDistance()
		else:
			self.route_distance = 0

	def getStartTime(self):
		return self.start

	def getEndTime(self):
		return self.end

	def getWaitTime(self):
		return self.wait_time

	def getDistance(self):
		return self.route_distance

def create_dispatch(time, start, dest):
	rte = routes.finder.get_dirs(start, dest)
	dur = rte.getDuration()
	return Dispatch(time, time+dur, "NAV", rte, dest, None)

def dispatch_from_task(task, start_time):
	return Dispatch(start_time, start_time + task.getDuration(),
		task.getType(), task.getRoute(), task.getDest(), start_time - task.getTimeOrdered())

def idle_dispatch(time, loc):
	return Dispatch(time, -1, "IDLE", None, loc, None)

class Vehicle:
	def __init__(self, uid, is_pev, loc):
		self.uid = uid
		self.is_pev = is_pev
		self.spawn = loc
		self.loc = loc

		self.history = [idle_dispatch(0, loc)]
		self.current = 0

		## TODO representation here

	def update(self, time):
		## The purpose of this method is to set the current loc (in case we use it in the future)
		## and to ensure that IDLE is appended if we finish everything.
		while len(self.history) > self.current and self.history[self.current].end <= time:
			if self.history[self.current].end == -1:
				break
			self.loc = self.history[self.current].dest ## TODO care about partial completion
			self.current += 1
		if self.current == len(self.history):
			self.history.append(idle_dispatch(self.history[-1].end, self.loc))
		## self.check_valid()

	def assign(self, task, time):
		if self.history[-1].kind == "IDLE":
			self.history[-1].end = time
		self.history.append(create_dispatch(self.soonestFreeAfter(time), self.history[-1].dest, task.getPickupLoc()))

		wait_time = self.soonestFreeAfter(time) - task.getTimeOrdered()
		self.history.append(dispatch_from_task(task, self.soonestFreeAfter(time)))
		return wait_time

	def check_valid(self):
		for i in xrange(len(self.history) - 1):
			errstring = "[" + str(i) + "].end " + self.history[i].kind + "= " + str(self.history[i].end) + " != [" + str(i + 1) + "].start (" + self.history[i+1].kind + " = " + str(self.history[i + 1].start)
			assert(self.history[i].end == self.history[i + 1].start), errstring
			
		

	def soonestFreeAfter(self, t):
		## return the soonest time that the PEV will
		## be free after time t
		if self.history[-1].end <= t:
			return t
		else:
			return self.history[-1].end

	def getUID(self):
		return self.uid

	def getActionAt(self, time_window):
		## TODO return PASSENGER, PARCEL, BOTH, or NONE depending
		## on what the vehicle is being used for in that window
		passenger = False
		parcel = False
		## TODO binary search for efficiency (?)
		for d in self.history:
			if d.start > time_window[1]:
				break
			elif d.end >= time_window[0]:
				if d.kind == "PASSENGER":
					passenger = True
				elif d.kind == "PARCEL":
					parcel = True
		if passenger and parcel:
			return "BOTH"
		elif passenger:
			return "PASSENGER"
		elif parcel:
			return "PARCEL"
		else:
			return None
			

class Fleet:
	def __init__(self, fleet_size, bounds, start_loc):
		self.vehicles = []
		start_loc = start_loc
		for i in xrange(fleet_size):
			self.vehicles.append(
				Vehicle(i, True, start_loc))		

		
	def assign_task(self, trip):
		## TODO args, return?
		t = trip.getTimeOrdered()
		for v in self.vehicles:
			v.update(t)
		(vid, wait) = fsched.assign(t, trip, self)
		print "task " + str(trip.getID()) + " assigned to vehicle " + str(vid) + " with wait of " + str(wait)

	## returns the utilization (Passengers/packages) at time t
	def getUtilization(self, time_window):
		## TODO make more efficient by just bisecting the fleet history
		denom = len(self.vehicles)
		passengers = 0
		parcels = 0
		for v in vehicles:
			action = v.getActionAt(time_window)
			if action == "PASSENGER":
				passengers += 1
			elif action == "PARCEL":
				parcels += 1
			elif action == "BOTH":
				passengers += 1
				parcels += 1
		return (float(passengers) / denom, float(parcels) / denom)

	def __getitem__(self, key):
		return self.vehicles[key]
