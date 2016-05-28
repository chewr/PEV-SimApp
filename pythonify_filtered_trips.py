import cPickle as pickle
from datetime import datetime
import csv

## get a slice of hubway data -- pick a summer week
## say May
filtered = csv.reader(open("hubway/filtered_tripsthrough2012.csv", 'rb'))

## consume field line
fields = filtered.next()

trips = []

## pythonify
for row in filtered:
	trip = {
		"seq_id" : int(row[0]),
		"hubway_id" : int(row[1]),
		"status" : row[2],
		"duration" : int(row[3]),
		"start_date" : datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
		"strt_statn" : int(row[5]),
		"end_date" : datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
		"end_statn" : int(row[7]),
		"bike_nr" : row[8],
		"subsc_type" : row[9],
		"zip_code" : row[10],
		"birth_date" : row[11],
		"gender" : row[12],
	}
	trips.append(trip)

pickle.dump(trips, open("filtered_tripsthrough2012.pkl", "wb"))
