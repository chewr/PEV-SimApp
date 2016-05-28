import cPickle as pickle
from datetime import datetime
import csv

## get a slice of hubway data -- pick a summer week
## say May
trips = csv.reader(open("hubway/tripsthrough2012.csv", 'rb'))

fields = trips.next()
field_to_idx = {}
i = 0
for f in fields:
	field_to_idx[f] = i
	i += 1
	
w = csv.writer(open("hubway/filtered_tripsthrough2012.csv", 'wb'))
w.writerow(fields)

interval_start = datetime.strptime('2012-07-06 00:00:00', '%Y-%m-%d %H:%M:%S')
interval_end = datetime.strptime('2012-07-13 00:00:00', '%Y-%m-%d %H:%M:%S')

for trip in trips:
	start_dt = datetime.strptime(trip[field_to_idx['start_date']], '%Y-%m-%d %H:%M:%S')
	if interval_start <= start_dt and start_dt < interval_end:
		w.writerow(trip)

