#TODO random trip generation
#TODO allow user to supply trip file
import csv
import trip

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
				start = (float(row[4]), float(row[3]))
				dest = (float(row[8]), float(row[7]))
				trips.append(trip.Pickup(
					row[1], ## TODO time-ify
					start, 
					dest,
					True) ## TODO packages?
				)
			except ValueError:
				pass
	return trips

testdata = readNewburyTestData()
for t in testdata:
	print t.approx_dur()
