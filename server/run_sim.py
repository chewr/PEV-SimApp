import dynamic_trips

def Run(fleet, maxDist, freq, start, end):
	pickups = dynamic_trips.TripRandomizer().assembleTripSim(maxDist, freq, maxDist, freq, start, end)
	return pickups
