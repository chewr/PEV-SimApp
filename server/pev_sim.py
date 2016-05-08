## TODO run simulation of a fleet of PEVs carrying out a
## a set of pickup/dropoff tasks

import fleet as pev
import os
import hashlib

class Sim_env:
	def __init__(self, fleet_size, bounds, start_loc):
		self.bounds = bounds
		self.fleet_size = fleet_size
		self.start_loc = start_loc
		self.fleet = pev.Fleet(fleet_size, bounds, start_loc)

		self.sim_start = 0
		self.sim_end = 0

		## time series data bucketed by 10 minutes
		self.util = []
		self.emissions = []
		self.wait_times = []

		self.trips = []
	
		self.sim_uid = str(hashlib.sha224(os.urandom(160)).hexdigest())

	def getSegment(self, start, end):
		sgmnt = Sim_env(self.fleet_size, self.bounds, self.start_loc)
		sgmnt.fleet = self.fleet.getSegment(start, end)
		sgmnt.sim_start = start
		sgmnt.sim_end = end
		sgmnt.sim_uid = self.sim_uid

		## sgmnt.util = self.fleet.getUtilization(start, end)
		sgmnt.util = self.fleet.getUtilization()

		## sgmnt.emissions = self.fleet.getEmissions(start, end)
		sgmnt.emissions = self.fleet.getEmissions()

		## filter trips by time ordered
		sgmnt.trips = []
		for trip in self.trips:
			if start <= trip.getTimeOrdered() and trip.getTimeOrdered() < end:
				sgmnt.trips.append(trip)
		return sgmnt	

	def schedule(self, trips):
		print "Assigning tasks..."
		## trips is a sorted list of Trip objects,
		## sorted by pickup time
		for t in trips:
			self.fleet.assign_task(t)
		print "Assigned!"
		self.fleet.finishUp() ## TODO don't "finish up" if we want to stream
		print "Closed simulation!"

		self.trips.extend(trips);

		print "extended data and logs!"

		## TODO update sim_end
		## TODO time series statistics

		## Fleet implementation:
		## for each vehicle, call the statistics method over the whole time range
		## Merge the results that each vehicle produces (mean of utilization, sum of emissions)

		## Vehicle implementation
		## given a time range:
		## create a set of 30-minute buckets
		## iterate over history
		## for each trip in history, apply to relevant buckets
		## utilization should be passengers or parcels * minutes of trip / bucket size
		## emissions should be total distance of any sort. For trips that span multiple buckets,
		## the distance should be prorated into each bucket

		## For getting wait times:
		## TODO: strategerize this one?

