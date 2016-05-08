import dynamic_trips
import pev_sim
import sim_util
import json

environs = {}

def Run(sim_uid, fleet, maxDist, freq, dur):
	start = 0
	end = start + dur
	pickups = dynamic_trips.TripRandomizer().assembleTripSim(maxDist, freq, maxDist, freq, start, end)
	if sim_uid in environs:
		env = environs[sim_uid]
	else:
		env = pev_sim.Sim_env(fleet, None, (42.3602595,-71.0873766))
		environs[env.sim_uid] = env
	env.schedule(pickups)
	return json.dumps(env.getSegment(start, end), default=sim_util.default_json, separators=(',', ':'), indent=4)
