import cPickle as pickle
import server
from datetime import datetime
import csv
import random
from sets import Set

server.routes.RouteFinder("google_api_key", "route_cache")

locs = pickle.load(open("fuzzed_stations.pkl", 'rb'))

## "seq_id" 	: int(row[0]),
## "hubway_id" 	: int(row[1]),
## "status" 	: row[2],
## "duration" 	: int(row[3]),
## "start_date" : datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),
## "strt_statn" : int(row[5]),
## "end_date" 	: datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S'),
## "end_statn" 	: int(row[7]),
## "bike_nr" 	: row[8],
## "subsc_type" : row[9],
## "zip_code" 	: row[10],
## "birth_date" : row[11],
## "gender" 	: row[12],

trips = pickle.load(open("filtered_tripsthrough2012.pkl", "rb"))

start_dt = datetime.strptime("2012-07-06 00:00:00", '%Y-%m-%d %H:%M:%S')

pickups = []

ct = 0

for trip in trips:
	uid = trip["seq_id"]
	td = trip["start_date"] - start_dt
	time_sec = int(td.total_seconds())
	start = random.sample(locs[str(trip["strt_statn"])], 1)[0]
	dest = random.sample(locs[str(trip["end_statn"])], 1)[0]
	is_human = True
	pickup = server.trip.Pickup(uid, time_sec, start, dest, is_human)
	pickups.append(pickup)
	ct += 1
	if ct % 10 == 0:
		print "completed:", ct

pickle.dump(pickups, open("filtered_pickupsthrough2012.pkl", "wb"))
