import shelve
import cPickle as pickle

class RouteCache:
	
	def __init__(self, filename):
		self.shelf = shelve.open(filename)

	def hasRoute(self, ori, dst):
		strkey = getKeyString((ori, dst))
		return self.shelf.has_key(strkey)

	def getRoute(self, ori, dst):
		strkey = getKeyString((ori, dst))
		return self.shelf[strkey]

	def setRoute(self, ori, dst, rte):
		strkey = getKeyString((ori, dst))
		self.shelf[strkey] = rte

	def save(self):
		self.shelf.sync()

	def close(self):
		self.shelf.close()

def getKeyString(a):
	out = pickle.dumps(a)
	assert(pickle.loads(out) == a)
	return out
