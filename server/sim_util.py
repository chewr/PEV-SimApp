## TODO utility functions for the simulation
from geopy.distance import great_circle
from time import strptime

def center_of(bounds):
	raise(NotImplementedError)

def ll_dist_m(a, b):
	return great_circle(a, b).meters

def timeify(s):
	return strptime(s, "%m/%d/%y %I:%M %p") 
