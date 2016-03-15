#TODO random trip generation
#TODO allow user to supply trip file
import csv

def readNewburyTestData():
	path = "../dataprocessing/filtered-street.csv"
	## TODO pop out into method
	trips = []
	with open(path, 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			## Row format: (for this one file)
			## ID
			## Pickup time
			## Pickup address
			## Pickup latitude
			## Pickup Longitude	
			## Dropoff Time
			## Dropoff address
			## Dropoff Latitude
			## Dropoff Longitude
			try:
				trips.append(trip.Pickup(
					row[1], ## TODO time-ify
					(float(row[3]), float(row[4])), ## lat-long ify
					(float(row[7]), float(row[8])), ## lat-log ify
					None, ## TODO get duration
					None, ## TODO get route
					True) ## TODO packages?
				)
			except ValueError:
				pass
	return trips
