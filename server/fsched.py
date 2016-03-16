## TODO an algorithm for assigning a task to a fleet
## Should run on-line (that is, without knowledge of
## upcoming tasks)
import fleet

def assign(time, task, fleet):
	## strawman - assign task to soonest free member
	assignee = None
	for pev in fleet:
		if assignee is None:
			assignee = pev
		elif pev.soonestFreeAfter(time) < assignee.soonestFreeAfter(time):
			assignee = pev
	assignee.assign(task, time)
