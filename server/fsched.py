## TODO an algorithm for assigning a task to a fleet
## Should run on-line (that is, without knowledge of
## upcoming tasks)
import fleet

def assign(task, fleet):
	## strawman - assign task to soonest free member
	assignee = None
	soonest_free = None
	for v in fleet.vehicles:
		if v.task is None:
			assignee = v
			break
		if v.free_at < soonest_free or soonest_free is None: ## totally ignores distance
			assignee = v
			soonest_free = v.free_at
	
	assignee.assign(task)
