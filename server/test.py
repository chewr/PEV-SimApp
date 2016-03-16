#!/usr/bin/env python
## TODO a test case

import tripgen
import pprint

testdata = tripgen.readNewburyTestData()

for t in testdata:
	print " ".join(["Trip", str(t.getID()), "Time", str(t.getTimeOrdered()), "Pickup:", str(t.getPickupLoc()), "Dropoff", str(t.getDest())])
