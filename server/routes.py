import googlemaps
import datetime

api_key = None
with open("google_api_key", 'r') as f:
	api_key = f.read().rstrip()

gmaps = googlemaps.Client(key=api_key)

# Request directions via public transit
now = datetime.datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

print directions_result
